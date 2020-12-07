# DNS-SERVER

## Testing

Please follow the steps below in order to test the DNS Server.

### Pre-requisites
Python 3.7

### How to Run Server
1. Clone the git repository using: `git clone https://github.com/njindal239/DNS-SERVER.git`
2. Go into the project directory: `cd DNS-Server`
3. Run the server: `python server.py`

### Sample Test Cases
Open another terminal tab and send DNS requests to the DNS Server using `dig` command line tool.
Here are a few sample cases that you can try:

1. `dig @127.0.0.1 -p 3000 google.com` (Query for IPv4 Address)

![alt text](https://github.com/njindal239/DNS-SERVER/blob/main/images/sample-test-case-1.png)


2. `dig @127.0.0.1 -p 3000 google.com` (Find result in cache)

![alt text](https://github.com/njindal239/DNS-SERVER/blob/main/images/sample-test-case-2.png)


3. `dig AAAA @127.0.0.1 -p 3000 google.com` (Query for IPv6 Address)

![alt text](https://github.com/njindal239/DNS-SERVER/blob/main/images/sample-test-case-3.png)


4. `dig @127.0.0.1 -p 3000 en.wikipedia.org` (Returns two answer records - CNAME record and A record)

![alt text](https://github.com/njindal239/DNS-SERVER/blob/main/images/sample-test-case-4.png)


5. `dig @127.0.0.1 -p 3000 microsoft.com`

![alt text](https://github.com/njindal239/DNS-SERVER/blob/main/images/sample-test-case-5.png)


6. Shut Down the server using `Ctrl+C`. The DNS cache gets saved to a file called `dns_cache.pickle`. Run the server again using: `python server.py`. Now,
try a test case: `dig @127.0.0.1 -p 3000 microsoft.com`. (The answer should still be cached provided the cache entry did not expire).

![alt text](https://github.com/njindal239/DNS-SERVER/blob/main/images/sample-test-case-6.png)


7. `dig MX @127.0.0.1 -p 3000 microsoft.com` (Sends a Query for MX record)

![alt text](https://github.com/njindal239/DNS-SERVER/blob/main/images/sample-test-case-7.png)

