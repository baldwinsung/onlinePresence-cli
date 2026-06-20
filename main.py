#!/usr/bin/env python

from datetime import datetime
import argparse
import ssl
import sys
import dns.resolver
import OpenSSL
import whois
from ipwhois import IPWhois


def domainWhois(dn):
    try:
        w = whois.whois(dn)
        print("\n")
        print("Domain Registration information")
        print("-------------------------------")
        print("Domain Name:      ", dn)
        print("Registrar:        ", w.registrar)
        print("Created:          ", w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date)
        print("Expires:          ", w.expiration_date[0] if isinstance(w.expiration_date, list) else w.expiration_date)
    except Exception:
        print(f"\n{dn} does not exist or WHOIS lookup failed.")
        sys.exit(1)


def resolveApex(dn):
    """Resolve the first A record for dn, or exit on failure."""
    try:
        result = dns.resolver.resolve(dn, 'A')
        ips = [r.to_text() for r in result]
    except Exception:
        print(f"\nA record (APEX) for {dn} does not exist")
        sys.exit(1)
    if not ips:
        print(f"\nA record (APEX) for {dn} does not exist")
        sys.exit(1)
    return ips[0]


def hostingProvider(dn, ip_apex):
    print("A aka APEX Record:", ip_apex)
    try:
        lookup = IPWhois(ip_apex)
        p = lookup.lookup_rdap()
        if p['objects']:
            for x in p['objects']:
                name = p['objects'][x]['contact']['name']
                print("Hosting Provider: ", name)
                break
    except Exception:
        print("Hosting Provider:  (lookup failed)")


def mailExchanger(dn):
    try:
        result = dns.resolver.resolve(dn, 'MX')
        exchanges = [rdata.exchange for rdata in result]
        print("\n")
        print("Mail Exchanger information")
        print("--------------------------")
        print("Domain Name:      ", dn)
        print("Total MX:         ", len(exchanges))
        for exchange in exchanges:
            print("                  ", exchange)
    except Exception:
        print("\nMX lookup failed")
        sys.exit(1)


def nameServer(dn):
    try:
        result = dns.resolver.resolve(dn, 'NS')
        servers = list(result)
        print("\n")
        print("Name Server information")
        print("------------------------")
        print("Domain Name:      ", dn)
        print("Total NS:         ", len(servers))
        for rdata in servers:
            print("                  ", rdata)
    except Exception:
        print("\nNS lookup failed")
        sys.exit(1)


def sslCertificate(dn):
    try:
        c = ssl.get_server_certificate((dn, 443), timeout=5)
    except Exception:
        print(f"\nSSL certificate for {dn} timed out")
        print("Try this from the shell...")
        print(f"echo | openssl s_client -showcerts -connect {dn}:443 2>/dev/null | \\")
        print("openssl x509 -inform pem -noout -dates -ext subjectAltName")
        sys.exit(1)

    x = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, c)
    ir = x.get_issuer()
    cn = x.get_subject()
    nb = datetime.strptime(x.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ')
    na = datetime.strptime(x.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')

    ir_str = "".join(f"/{name.decode()}={value.decode()}" for name, value in ir.get_components())
    cn_str = "".join(f"/{name.decode()}={value.decode()}" for name, value in cn.get_components())

    print("\n")
    print("SSL Certificate information")
    print("---------------------------")
    print("Domain Name:      ", dn)
    print("Subject:          ", cn_str.split('/')[1])
    print("Issuer:           ", ir_str.split('/')[2])
    print("Not Before:       ", nb)
    print("Not After:        ", na)

    ec = x.get_extension_count()
    for i in range(ec):
        ge = x.get_extension(i)
        if 'subjectAltName' in str(ge.get_short_name()):
            s = sorted(ge.__str__().split(','))
            print("Total SANs:       ", len(s))
            for entry in s:
                print("                 ", entry)


def main():
    parser = argparse.ArgumentParser(description="Report online presence of a domain.")
    parser.add_argument("domain", help="Domain name to query (e.g. google.com)")
    args = parser.parse_args()
    dn = args.domain

    domainWhois(dn)
    ip = resolveApex(dn)
    hostingProvider(dn, ip)
    sslCertificate(dn)
    mailExchanger(dn)
    nameServer(dn)


if __name__ == '__main__':
    main()
