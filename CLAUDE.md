# onlinePresence-cli

Python CLI that prints a full online presence report for a domain: WHOIS registration, hosting provider, SSL certificate details, MX records, and NS records.

## Commands

### Setup
```bash
mkvirtualenv onlinePresence
pip install -r requirements.txt
chmod +x main.py
```

### Run
```bash
./main.py google.com
```

## Output Sections (in order)

1. **Domain Registration** — registrar, created, expires (via WHOIS)
2. **A record + Hosting Provider** — resolved IP and provider name from RDAP
3. **SSL Certificate** — subject, issuer, validity dates, all SANs
4. **Mail Exchanger** — all MX records
5. **Name Servers** — all NS records

## Architecture

Single-file script (`main.py`). No database. All lookups are live network calls:

- WHOIS: `python-whois`
- DNS (A, MX, NS): `dnspython`
- IP/ASN hosting lookup: `ipwhois` (RDAP)
- SSL: stdlib `ssl` + `pyOpenSSL`

## Error Handling

- WHOIS failure or unregistered domain → prints message and exits
- Missing A record → prints message and exits
- SSL timeout → prints manual `openssl` command as fallback and exits

## Notes

- `checkApex` and `checkSslCertificate` are guard functions that exit early so downstream functions can assume success.
- EDU domains may not work with `python-whois` (commented-out guard exists in `main`).
