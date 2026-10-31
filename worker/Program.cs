using System;
using System.Collections.Generic;
using System.Data.Common;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using Newtonsoft.Json;
using Npgsql;
using StackExchange.Redis;

namespace Worker
{
    public class Program
    {
        private static volatile bool _redisUp;
        private static volatile bool _dbUp;
        private static long _lastLoopTicks = DateTime.UtcNow.Ticks;
        private static readonly TimeSpan LoopStallLimit = TimeSpan.FromSeconds(10);

        public static int Main(string[] args)
        {
            try
            {
                // Start first so /healthz answers while we wait for db and redis
                StartHealthListener();

                var pgsql = OpenDbConnection("Server=db;Username=postgres;Password=postgres;");
                var redisConn = OpenRedisConnection("redis");
                var redis = redisConn.GetDatabase();

                // Keep alive is not implemented in Npgsql yet. This workaround was recommended:
                // https://github.com/npgsql/npgsql/issues/1214#issuecomment-235828359
                var keepAliveCommand = pgsql.CreateCommand();
                keepAliveCommand.CommandText = "SELECT 1";

                var definition = new { vote = "", voter_id = "" };
                while (true)
                {
                    // Slow down to prevent CPU spike, only query each 100ms
                    Thread.Sleep(100);
                    Interlocked.Exchange(ref _lastLoopTicks, DateTime.UtcNow.Ticks);

                    // Reconnect redis if down
                    _redisUp = redisConn != null && redisConn.IsConnected;
                    if (!_redisUp) {
                        Console.WriteLine("Reconnecting Redis");
                        redisConn = OpenRedisConnection("redis");
                        redis = redisConn.GetDatabase();
                        _redisUp = true;
                    }
                    _dbUp = pgsql.State.Equals(System.Data.ConnectionState.Open);

                    string json = redis.ListLeftPopAsync("votes").Result;
                    if (json != null)
                    {
                        var vote = JsonConvert.DeserializeAnonymousType(json, definition);
                        Console.WriteLine($"Processing vote for '{vote.vote}' by '{vote.voter_id}'");
                        // Reconnect DB if down
                        if (!pgsql.State.Equals(System.Data.ConnectionState.Open))
                        {
                            Console.WriteLine("Reconnecting DB");
                            pgsql = OpenDbConnection("Server=db;Username=postgres;Password=postgres;");
                        }
                        else
                        { // Normal +1 vote requested
                            UpdateVote(pgsql, vote.voter_id, vote.vote);
                        }
                    }
                    else
                    {
                        keepAliveCommand.ExecuteNonQuery();
                    }
                }
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine(ex.ToString());
                return 1;
            }
        }

        private static void StartHealthListener()
        {
            var listener = new HttpListener();
            listener.Prefixes.Add("http://+:8081/");
            try
            {
                listener.Start();
            }
            catch (HttpListenerException ex)
            {
                Console.Error.WriteLine($"Health endpoint not started: {ex.Message}");
                return;
            }

            var thread = new Thread(() =>
            {
                while (true)
                {
                    var context = listener.GetContext();
                    try
                    {
                        HandleHealthRequest(context.Request, context.Response);
                    }
                    catch (Exception ex)
                    {
                        Console.Error.WriteLine(ex.ToString());
                    }
                    finally
                    {
                        context.Response.Close();
                    }
                }
            }) { IsBackground = true };
            thread.Start();
        }

        private static void HandleHealthRequest(HttpListenerRequest request, HttpListenerResponse response)
        {
            if (request.Url.AbsolutePath != "/healthz")
            {
                response.StatusCode = 404;
                return;
            }
            if (request.HttpMethod != "GET")
            {
                response.StatusCode = 405;
                return;
            }

            var failing = new List<string>();
            if (!_redisUp) failing.Add("redis");
            if (!_dbUp) failing.Add("db");
            // Only judge the loop when both connections are up, since reconnects block it
            if (failing.Count == 0 && DateTime.UtcNow.Ticks - Interlocked.Read(ref _lastLoopTicks) > LoopStallLimit.Ticks)
            {
                failing.Add("loop");
            }

            var healthy = failing.Count == 0;
            response.StatusCode = healthy ? 200 : 503;
            response.ContentType = "application/json";
            var bytes = Encoding.UTF8.GetBytes(JsonConvert.SerializeObject(new { status = healthy ? "ok" : "unavailable", failing }));
            response.ContentLength64 = bytes.Length;
            response.OutputStream.Write(bytes, 0, bytes.Length);
        }

        private static NpgsqlConnection OpenDbConnection(string connectionString)
        {
            NpgsqlConnection connection;

            while (true)
            {
                try
                {
                    connection = new NpgsqlConnection(connectionString);
                    connection.Open();
                    break;
                }
                catch (SocketException)
                {
                    Console.Error.WriteLine("Waiting for db");
                    Thread.Sleep(1000);
                }
                catch (DbException)
                {
                    Console.Error.WriteLine("Waiting for db");
                    Thread.Sleep(1000);
                }
            }

            Console.Error.WriteLine("Connected to db");

            var command = connection.CreateCommand();
            command.CommandText = @"CREATE TABLE IF NOT EXISTS votes (
                                        id VARCHAR(255) NOT NULL UNIQUE,
                                        vote VARCHAR(255) NOT NULL
                                    )";
            command.ExecuteNonQuery();

            return connection;
        }

        private static ConnectionMultiplexer OpenRedisConnection(string hostname)
        {
            // Use IP address to workaround https://github.com/StackExchange/StackExchange.Redis/issues/410
            var ipAddress = GetIp(hostname);
            Console.WriteLine($"Found redis at {ipAddress}");

            while (true)
            {
                try
                {
                    Console.Error.WriteLine("Connecting to redis");
                    return ConnectionMultiplexer.Connect(ipAddress);
                }
                catch (RedisConnectionException)
                {
                    Console.Error.WriteLine("Waiting for redis");
                    Thread.Sleep(1000);
                }
            }
        }

        private static string GetIp(string hostname)
            => Dns.GetHostEntryAsync(hostname)
                .Result
                .AddressList
                .First(a => a.AddressFamily == AddressFamily.InterNetwork)
                .ToString();

        private static void UpdateVote(NpgsqlConnection connection, string voterId, string vote)
        {
            var command = connection.CreateCommand();
            try
            {
                command.CommandText = "INSERT INTO votes (id, vote) VALUES (@id, @vote)";
                command.Parameters.AddWithValue("@id", voterId);
                command.Parameters.AddWithValue("@vote", vote);
                command.ExecuteNonQuery();
            }
            catch (DbException)
            {
                command.CommandText = "UPDATE votes SET vote = @vote WHERE id = @id";
                command.ExecuteNonQuery();
            }
            finally
            {
                command.Dispose();
            }
        }
    }
}