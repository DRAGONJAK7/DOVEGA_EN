#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import requests
import dns.resolver
import json
import time
import sys
from datetime import datetime
from colorama import Fore, Style, init

# تفعيل الألوان في ويندوز
init(autoreset=True)

# ================== بانر سايبربانك ==================
BANNER = Fore.MAGENTA + r"""
   ____                               _   _             
  |  _ \ ___  ___  ___ ___   ___   __| | | |__  _   _   
  | | | / _ \/ __|/ __/ _ \ / _ \ / _` | | '_ \| | | |  
  | |_| \__/\__ \ (_| (_) | (_) | (_| | | |_) | |_| |_ 
  |____/(_) |___/\___\___/ \___/ \__,_| |_.__/ \__, (_)
                                               |___/    
""" + Fore.CYAN + """
        [+] Recon Hunter by DOVEGA_EN [+]
"""

print(BANNER)

# ================== سبينر لودر ==================
def spinner(text, delay=0.05, duration=1):
    spin = ['|', '/', '-', '\\']
    sys.stdout.write(Fore.YELLOW + text + " ")
    for _ in range(int(duration / delay)):
        for frame in spin:
            sys.stdout.write(Fore.CYAN + frame)
            sys.stdout.flush()
            time.sleep(delay)
            sys.stdout.write("\b")
    print("✓")


# ================== دوال الفحص ==================
def dns_lookup(domain):
    results = {}
    try:
        answers = dns.resolver.resolve(domain, 'A')
        results["A Records"] = [str(rdata) for rdata in answers]
    except Exception:
        results["A Records"] = []

    try:
        answers = dns.resolver.resolve(domain, 'MX')
        results["MX Records"] = [str(rdata.exchange) for rdata in answers]
    except Exception:
        results["MX Records"] = []

    try:
        answers = dns.resolver.resolve(domain, 'NS')
        results["NS Records"] = [str(rdata) for rdata in answers]
    except Exception:
        results["NS Records"] = []
    return results


def subdomain_scan(domain):
    subdomains = ["www", "mail", "ftp", "test", "dev", "api", "blog"]
    found = []
    for sub in subdomains:
        try:
            host = f"{sub}.{domain}"
            socket.gethostbyname(host)
            found.append(host)
        except Exception:
            pass
    return found


def port_scan(domain):
    open_ports = []
    common_ports = [21, 22, 25, 53, 80, 110, 143, 443, 3306, 8080]
    try:
        ip = socket.gethostbyname(domain)
        for port in common_ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()
    except Exception:
        pass
    return open_ports


def http_headers(domain):
    headers_data = {}
    try:
        url = f"http://{domain}"
        r = requests.get(url, timeout=3)
        headers_data = dict(r.headers)
    except Exception:
        headers_data = {"Error": "Could not fetch headers"}
    return headers_data


# ================== حفظ النتائج ==================
def save_results(domain, data):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename_json = f"Recon_{domain}_{timestamp}.json"
    filename_txt = f"Recon_{domain}_{timestamp}.txt"

    with open(filename_json, "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    with open(filename_txt, "w") as f:
        f.write("=== Recon Report ===\n")
        f.write(json.dumps(data, indent=4, ensure_ascii=False))

    print(Fore.GREEN + f"[+] النتائج تم حفظها في الملف: {filename_json} و {filename_txt}")


# ================== MAIN ==================
if __name__ == "__main__":
    target = input(Fore.CYAN + "[?] أدخل الدومين (مثال: example.com): ").strip()

    spinner("[*] جاري فحص DNS ...", duration=1.5)
    dns_data = dns_lookup(target)

    spinner("[*] جاري فحص Subdomains ...", duration=1.5)
    subs = subdomain_scan(target)

    spinner("[*] جاري فحص البورتات ...", duration=1.5)
    ports = port_scan(target)

    spinner("[*] جاري جلب HTTP Headers ...", duration=1.5)
    headers = http_headers(target)

    results = {
        "Domain": target,
        "DNS": dns_data,
        "Subdomains": subs,
        "Open Ports": ports,
        "HTTP Headers": headers
    }

    # عرض النتائج بشكل ملون
    print(Fore.MAGENTA + "\n=== النتائج ===")
    print(Fore.YELLOW + "🌀 DNS Records:")
    for key, value in dns_data.items():
        print(Fore.CYAN + f"   {key}: {value}")

    print(Fore.YELLOW + "\n🌐 Subdomains:")
    for s in subs:
        print(Fore.CYAN + f"   - {s}")
    if not subs:
        print(Fore.RED + "   لا يوجد Subdomains مكتشفة")

    print(Fore.YELLOW + "\n🔌 Open Ports:")
    for p in ports:
        print(Fore.CYAN + f"   - Port {p} مفتوح")
    if not ports:
        print(Fore.RED + "   لا يوجد بورتات مفتوحة")

    print(Fore.YELLOW + "\n📥 HTTP Headers:")
    for k, v in headers.items():
        print(Fore.CYAN + f"   {k}: {v}")

    # حفظ النتائج
    save_results(target, results)
