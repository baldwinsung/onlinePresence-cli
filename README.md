# onlinePresence-cli

Figure out the online presence for a company or academic institution. Starting point is usually their internet domain name.

Displays general information about the domain and SSL certificate.

Pay close attention to the expiration dates for both the domain and SSL certificates.

## Getting Started
Install the dependencies. Use a virtual environment.

```
mkvirtualenv onlinePresence
pip install -r requirements.txt
```

Test the code with google.
```
./main.py google.com
```

Output should be similar to...
```
Domain Registration information
-------------------------------
Registrar:         MarkMonitor, Inc.
Created:           1997-09-15 07:00:00+00:00
Expires:           2028-09-13 07:00:00+00:00
A aka APEX Record: 142.251.40.238
Hosting Provider:  Google LLC


SSL Certificate information
---------------------------
Domain Name:       google.com
Not Before:        2023-12-11 08:03:31
Not After:         2024-03-04 08:03:30
Total SANs      :  136
                   DNS:*.2mdn-cn.net
                   DNS:*.admob-cn.com
                   DNS:*.ampproject.net.cn
                   DNS:*.ampproject.org.cn
                   DNS:*.android.com
```

# Credits

Richard Penman ( https://github.com/richardpenman ) for python-whois
