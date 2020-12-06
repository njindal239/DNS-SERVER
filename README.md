# DNS-SERVER

## How to Run Server
1. Clone the git repository using: `git clone url`
2. Go into the project directory: `cd DNS-Server`
3. Run the server: `python server.py`

## Sample Test Cases
Open another terminal tab and send DNS requests to the DNS Server using `dig` command line tool.
Here are a few sample cases that you can try:

1. `dig @127.0.0.1 -p 3000 google.com` (Query for IPv4 Address)

2. `dig AAAA @127.0.0.1 -p 3000 google.com` (Query for IPv6 Address)

3. `dig @127.0.0.1 -p 3000 google.com` (Find result in cache)

4. `dig @127.0.0.1 -p 3000 en.wikipedia.org` (Returns two answer records - CNAME record and A record)

5. `dig @127.0.0.1 -p 3000 microsoft.com`

6. Shut Down the server using `Ctrl+C`. The DNS cache gets saved to a file called `dns_cache.pickle`. Run the server again using: `python server.py`. Now,
try a test case: `dig @127.0.0.1 -p 3000 microsoft.com`. (The answer should still be cached provided the cache entry did not expire).
