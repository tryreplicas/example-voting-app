# this creates urlencode-friendly files without EOL
import urllib.parse

with open('postb', 'w') as outfile:
    outfile.write(urllib.parse.urlencode({'vote': 'b'}))
with open('posta', 'w') as outfile:
    outfile.write(urllib.parse.urlencode({'vote': 'a'}))
