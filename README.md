# onlinePresence-cli

CLI tool to report the full online presence of a domain — WHOIS registration, hosting provider, SSL certificate, MX records, and name servers.

## Getting Started

```bash
mkvirtualenv onlinePresence
pip install -r requirements.txt
chmod +x main.py
```

## Usage

```bash
./main.py <domain>
```

Example:
```bash
./main.py google.com
```

## Example Output

```
Domain Registration information
-------------------------------
Domain Name:       google.com
Registrar:         MarkMonitor, Inc.
Created:           1997-09-15 07:00:00+00:00
Expires:           2028-09-13 07:00:00+00:00

A aka APEX Record: 142.251.40.238
Hosting Provider:  Google LLC


SSL Certificate information
---------------------------
Domain Name:       google.com
Subject:           CN=*.google.com
Issuer:            O=Google Trust Services LLC
Not Before:        2023-12-11 08:03:31
Not After:         2024-03-04 08:03:30
Total SANs:        136
                   DNS:*.2mdn-cn.net
                   DNS:*.admob-cn.com
                   ...


Mail Exchanger information
--------------------------
Domain Name:       google.com
Total MX:          5
                   alt1.aspmx.l.google.com.
                   ...


Name Server information
------------------------
Domain Name:       google.com
Total NS:          4
                   ns1.google.com.
                   ...
```

## Credits

[Richard Penman](https://github.com/richardpenman) for python-whois
