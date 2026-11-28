using System;
using System.Data.Common;
using System.Linq;
using System.Net;
using System.Net.Sockets;
using System.Threading;
using Newtonsoft.Json;
using Npgsql;
using StackExchange.Redis;

namespace Worker
{
    public class Program
    {
        // Max consecutive failed redis connection attempts before exiting
        private const int MaxRedisRetries = 5;

        public static int Main(string[] args)
        {
            try
            {
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

                    // Reconnect redis if down
                    if (redisConn == null || !redisConn.IsConnected) {
                        Console.WriteLine("Reconnecting Redis");
                        redisConn?.Dispose();
                        redisConn = OpenRedisConnection("redis");
                        redis = redisConn.GetDatabase();
                    }

                    string json;
                    try
                    {
                        json = redis.ListLeftPop("votes");
                    }
                    catch (Exception ex) when (IsRedisConnectionError(ex))
                    {
                        // Redis dropped mid-run: nothing was popped, so no vote is lost.
                        // Force a reconnect (with backoff) on the next iteration.
                        Console.Error.WriteLine($"Lost connection to redis: {ex.GetType().Name}: {ex.Message}");
                        redisConn.Dispose();
                        redisConn = null;
                        continue;
                    }

                    if (json != null)
                    {
                        var vote = JsonConvert.DeserializeAnonymousType(json, definition);
                        Console.WriteLine($"Processing vote for '{vote.vote}' by '{vote.voter_id}'");
                        // Reconnect DB if down
                        if (!pgsql.State.Equals(System.Data.ConnectionState.Open))
                        {
                            Console.WriteLine("Reconnecting DB");
                            pgsql = OpenDbConnection("Server=db;Username=postgres;Password=postgres;");
                            keepAliveCommand = pgsql.CreateCommand();
                            keepAliveCommand.CommandText = "SELECT 1";
                        }
                        // Normal +1 vote requested
                        UpdateVote(pgsql, vote.voter_id, vote.vote);
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

        private static NpgsqlConnection OpenDbConnection(string connectionString)
        {
            NpgsqlConnection connection;

            for (var attempt = 1; ; attempt++)
            {
                try
                {
                    connection = new NpgsqlConnection(connectionString);
                    connection.Open();
                    break;
                }
                catch (Exception ex) when (ex is SocketException || ex is DbException)
                {
                    var delay = RetryDelay(attempt);
                    Console.Error.WriteLine($"Waiting for db: attempt {attempt} failed ({ex.GetType().Name}: {ex.Message}), retrying in {delay.TotalSeconds:0.#}s");
                    Thread.Sleep(delay);
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
            for (var attempt = 1; ; attempt++)
            {
                try
                {
                    // Resolve on every attempt: the redis container may come back with a new IP.
                    // Use IP address to workaround https://github.com/StackExchange/StackExchange.Redis/issues/410
                    var ipAddress = GetIp(hostname);
                    Console.WriteLine($"Found redis at {ipAddress}");
                    Console.Error.WriteLine($"Connecting to redis (attempt {attempt})");
                    var connection = ConnectionMultiplexer.Connect(ipAddress);
                    Console.Error.WriteLine("Connected to redis");
                    return connection;
                }
                catch (Exception ex) when (ex is SocketException || ex is InvalidOperationException || IsRedisConnectionError(ex))
                {
                    if (attempt >= MaxRedisRetries)
                    {
                        Console.Error.WriteLine($"Giving up on redis: attempt {attempt} failed ({ex.GetType().Name}: {ex.Message}), reached max of {MaxRedisRetries} attempts, exiting");
                        Environment.Exit(1);
                    }
                    var delay = RetryDelay(attempt);
                    Console.Error.WriteLine($"Waiting for redis: attempt {attempt} failed ({ex.GetType().Name}: {ex.Message}), retrying in {delay.TotalSeconds:0.#}s");
                    Thread.Sleep(delay);
                }
            }
        }

        // Exponential backoff for redis and db retries: 0.5s, 1s, 2s, 4s, ... capped at 30s
        private static TimeSpan RetryDelay(int attempt)
            => TimeSpan.FromMilliseconds(Math.Min(500 * Math.Pow(2, Math.Min(attempt - 1, 16)), 30000));

        private static bool IsRedisConnectionError(Exception ex)
            => ex is RedisConnectionException
                || ex is RedisTimeoutException
                || ex is ObjectDisposedException
                || (ex is AggregateException agg && agg.InnerExceptions.Any(IsRedisConnectionError));

        private static string GetIp(string hostname)
            => Dns.GetHostEntry(hostname)
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