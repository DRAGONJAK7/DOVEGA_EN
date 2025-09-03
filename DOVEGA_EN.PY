#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import sys
from colorama import Fore, init

init(autoreset=True)

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

# 🔹 دوال الأدوات
def run_sqlmap():
    target = input("Enter target URL: ")
    try:
        subprocess.call(["sqlmap", "-u", target, "--batch"])
    except FileNotFoundError:
        print(Fore.RED + "[!] sqlmap غير منصب، ثبته بالأمر: pkg install sqlmap")

def run_nikto():
    target = input("Enter target URL/IP: ")
    try:
        subprocess.call(["nikto", "-h", target])
    except FileNotFoundError:
        print(Fore.RED + "[!] nikto غير منصب، ثبته بالأمر: pkg install nikto")

def run_gobuster():
    target = input("Enter target URL: ")
    wordlist = input("Enter path to wordlist (مثال: /usr/share/wordlists/dirb/common.txt): ")
    try:
        subprocess.call(["gobuster", "dir", "-u", target, "-w", wordlist])
    except FileNotFoundError:
        print(Fore.RED + "[!] gobuster غير منصب، ثبته بالأمر: pkg install gobuster")

def run_zphisher():
    try:
        subprocess.call(["bash", "zphisher/zphisher.sh"])
    except FileNotFoundError:
        print(Fore.RED + "[!] سكربت zphisher غير موجود، نزلو بـ: git clone https://github.com/htr-tech/zphisher")

# 🔹 القائمة الرئيسية
def menu():
    banner()
    print(Fore.CYAN + """
[1] SQLMAP
[2] Nikto
[3] Gobuster
[4] Zphisher
[0] Exit
""")

    choice = input(Fore.YELLOW + "Select option: ")

    if choice == "1":
        run_sqlmap()
    elif choice == "2":
        run_nikto()
    elif choice == "3":
        run_gobuster()
    elif choice == "4":
        run_zphisher()
    elif choice == "0":
        print(Fore.RED + "Exiting...")
        sys.exit()
    else:
        print(Fore.RED + "Invalid choice!")

if __name__ == "__main__":
    menu()
