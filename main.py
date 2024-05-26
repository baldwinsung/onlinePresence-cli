#!/usr/bin/env python

from datetime import datetime
# import pprint
import ssl
import sys
import dns.resolver
import OpenSSL
import whois
from ipwhois import IPWhois


def domainWhois(dn):
    w = whois.whois(dn)
    # print(w)
    print("\n")
    print("Domain Registration information")
    print("-------------------------------")
    print("Registrar:        ", w.registrar)
    if type(w.creation_date) is list:
        print("Created:          ", w.creation_date[0])
    else:
        print("Created:          ", w.creation_date)

    if type(w.expiration_date) is list:
        print("Expires:          ", w.expiration_date[0])
    else:
        print("Expires:          ", w.expiration_date)


def checkApex(dn):
    try:
        result = dns.resolver.resolve(dn, 'A')
    except:
        print("\nA record aka APEX record for " + domain_name + " does not exist")
        sys.exit(1)


def hostingProvider(dn):
    result = dns.resolver.resolve(dn, 'A')
    for ipval in result:
        # print('IP', ipval.to_text())
        ip_apex = ipval.to_text()

    if ip_apex:
        print("A aka APEX Record:", ip_apex)
        lookup = IPWhois(ip_apex)
        p = lookup.lookup_rdap()
        # pprint.pprint(p)
        # print(p['network']['name'])
        if p['objects'] is not None:
            for x in p['objects']:
                hosting_provider = p['objects'][x]['contact']['name']
                print("Hosting Provider: ", hosting_provider)
                break


def checkSslCertificate(dn):
    try:
        c = ssl.get_server_certificate((dn, 443), timeout=5)
    except:
        print("\nSSL certificate for " + domain_name + " timed out")
        print("Try this from the shell...")
        print("echo | openssl s_client -showcerts -connect " + dn + ":443 2>/dev/null | \\")
        print("openssl x509 -inform pem -noout -dates -ext subjectAltName")
        sys.exit(1)


def sslCertificate(dn):
    c = ssl.get_server_certificate((dn, 443), timeout=5)
    x = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, c)
    ir = x.get_issuer()
    cn = x.get_subject()
    nb = datetime.strptime(x.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ')
    na = datetime.strptime(x.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')

    ir_str = "".join("/{:s}={:s}".format(name.decode(), value.decode())
                     for name, value in ir.get_components())
    cn_str = "".join("/{:s}={:s}".format(name.decode(), value.decode())
                     for name, value in cn.get_components())

    print("\n")
    print("SSL Certificate information")
    print("---------------------------")
    print("Domain Name:      ", dn)
    print("Subject:          ", cn_str.split('/')[1])
    print("Issuer:           ", ir_str.split('/')[2])
    print("Not Before:       ", nb)
    print("Not After:        ", na)

    ec = x.get_extension_count()
    for i in range(0, ec):
        ge = x.get_extension(i)
        if 'subjectAltName' in str(ge.get_short_name()):
            s = ge.__str__()
            s = s.split(',')
            s.sort()
            print("Total SANs:       ", len(s))
            minusOne = (len(s) - 1)
            for i in range(0, minusOne):
                print("                 ", s[i])
            print("                  ", s[minusOne])


if len(sys.argv) > 1:
    domain_name = sys.argv[1]

    # check if edu
    # tld = domain_name.split('.')
    # if tld[1] == 'edu':
    #    print("\ncannot lookup edu domains. educause is not in python-whois")
    #    print("\nJust checking SSL certificate...")
    #    sslCertificate(domain_name)
    #    sys.exit(1)

    domainWhois(domain_name)
    checkApex(domain_name)
    hostingProvider(domain_name)
    checkSslCertificate(domain_name)
    sslCertificate(domain_name)

else:
    print("\nPlease add the domain_name you want to query")
    print("For example: " + sys.argv[0] + " google.com\n")
