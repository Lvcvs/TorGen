#!/usr/bin/python
# -*- coding: utf-8 -*-
# Autore: LS1911 (https://www.github.com/LS1911)
import os
import sys, platform

def install():

    print("\n~# TorGen Installer\n")

    if platform.system() != "Windows":
        pkgs = ["tor","python-socks","python3-pip"]
        for pkg in pkgs:
            os.system("apt install -y %s"%(pkg))

        # LINUX: crea il file "installed"
        os.system("touch tgen_files/installed")

        lbries = ["bs4","requests","pysocks","lxml","psutil"]
        for lbry in lbries:
            os.system("pip3 install %s"%(lbry))

    else:
        # WINDOWS: crea il file "installed"
        os.system("type nul > tgen_files/installed")


    print("\n[+] Installazione completata. Avvia TorGen con 'python3 torgen.py'.\n")

if __name__ == "__main__":

    # verifica sistema
    if platform.system() == "Windows":
        print("\n[-] Spiacente, TorGen non è compatibile con Windows.\n")
        exit(1)

    # verifica dei permessi di root
    if platform.system() != "Windows":
        if os.geteuid() != 0:
            print("\n[-] Avvia torgen.py come utente root.\n")
            exit(1)

    # verifica che la major release di python sia pari o superiore a 3
    if int(sys.version.split()[0].split(".")[0]) < 3:
        print("[-] Usa 'python3 installer.py' per avviare l'installer.")
        exit(1)

    install()