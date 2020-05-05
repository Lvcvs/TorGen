#!/usr/bin/python
# -*- coding: utf-8 -*-
# Autore: LS1911 (https://www.github.com/LS1911)

import os, sys, random, platform, socket, time

try:   
    from bs4 import BeautifulSoup # ispezione
    from urllib.request import urlopen
    import requests, socks, psutil
except ImportError as e:
    print("[-] Errore: %s"%(e))
    print("[-] Esegui 'python3 install.py' prima di procedere.")
    sys.exit(1)


# All'uscita, disattiva tor
def exit(code):
    # ferma Tor
    if platform.system() != "Windows":
        os.system("service tor stop > /dev/null")
    else:
        # psutil: windows non è d'aiuto. Ritorna l'eccezione psutil.AccessDenied o simile.
        #         solamente nel leggere le informazioni del servizio.

        # Non è comunque possibile fermare il servizio Tor senza avere i permessi di amministratore,
        # il ché non è positivo per un semplice programma che testa i suoi stessi link :/
        pass

    sys.exit(code)


def save_link(links_list,type="links"):
    if len(links_list) != 0:
        # assegna il nome appropriato al file di output in base a type
        file_id = 0
        output = "links/%s_%s.txt"%(type, file_id)

        # verifica che il file non esista, se il contrario assegna un id differente al file
        while os.path.isfile(output) == True:
            file_id += 1
    
            # riassegna il nome al file
            output = "links/%s_%s.txt"%(type, file_id)


        # apre il file e salva il contenuto
        save_file = open(output, "a")

        for link in links_list:
            save_file.write(link)

        save_file.close()

        print("[i] File: %s"%(output))


# Crea la connessione a Tor
def connectTor():
    try:
        global pure_ip

        ipcheck_url = 'https://wtfismyip.com/text'
        pure_ip = requests.get(ipcheck_url).text.replace('\n','')

        socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
        socket.socket = socks.socksocket

        def create_connection(address, timeout=None, source_address=None):
            sock = socks.socksocket()
            sock.connect(address)
            return sock

        socket.create_connection = create_connection

        tor_ip = requests.get(ipcheck_url).text.replace('\n','')
        if pure_ip == tor_ip: 
            raise Exception

    except Exception:
        print("\n[-] Connessione a Tor non riuscita.\n    Verifica che Tor sia attivo e riprova.")
        print("\n[-] Uscita...\n")
        exit(1)
    except KeyboardInterrupt:
        print("\n[-] Interrotto")
        print("[-] Uscita...\n")
        exit(1)

# Verifica se esiste ed ispeziona il titolo
def check_link(link):
    try:
        ipcheck_url = 'https://locate.now.sh/ip'
        check_ip = requests.get(ipcheck_url).text.replace('\n','')
    except KeyboardInterrupt:
        print("\n[-] Interrotto")
        print("[-] Uscita...\n")
        exit(1)
    
    if check_ip != pure_ip:
        code = "-"
        title = "-"

        try:
            code = urlopen(link, data=None, timeout=15).getcode()

            if code == 200:
                try:
                    soup = BeautifulSoup(urlopen(link), 'lxml')
                    title = soup.title.string

                except Exception:
                    # errore nell'ottenere il titolo
                    title = '-'
            else:
                code = str(code).strip().replace(':','')
                title = '-'

                if len(code) >= 4:
                    code = "-"
                
        except (KeyboardInterrupt, Exception):
            pass

        return code, title

    else:
        print("\n[-] Connessione a Tor persa")
        print("[-] Uscita...\n")
        exit(1)


# Testa i link
def link_tester(url_list):

    # tiene presente quanti testati e quanti funzionanti
    tested = 0
    working = []

    # crea una lista da riempire con link 'puliti'
    links = []

    # trova e sostituisce possibili "fastidi" e aggiunge i link alla lista 'links'
    for link in url_list:

        if "\n" in link:
            link = link.replace("\n","")

        if "http://" not in link:
            if "https://" in link:
                pass
            else:
                link = "http://" + link

        # aggiunge il link 'pulito' alla lista "links[]"
        links.append(link)

    print("\n[i] Testo URL(s)...\n")

    # Crea la sessione Tor
    try:

        # avvia i servizi richiesti
        if platform.system() != "Windows":
            os.system("service tor start > /dev/null")
        else:
            os.system("cd tor && tor.exe")

        connectTor()

    except (KeyboardInterrupt):
        save_link(working,type="working")
        print("\n[-] Interrotto")
        print("[-] Uscita...\n")
        exit(1)

    except:
        save_link(working,type="working")
        print("\n[-] Tor offline: assicurati che Tor sia attivo")
        print("[-] Uscita...\n")
        exit(1)    
        

    # testa URL contenuti in links
    for link in links:

        tested += 1
        print("[ %s ][i] URL >> %s/%s"%(time.strftime(r"%H:%M:%S"), tested, len(links)))
        print(" >> %s"%(link))

        # testa URL e salva codice di risposta e possibile titolo del sito:
        code, title = check_link(str(link))

        # se il link esiste viene aggiunto nella lista "working"
        if code == 200:
            working.append(str(link) + " >> %s \n"%(title))
            print(" >> %s >> %s"%(code, title))

        else:
            print(" >> %s"%(code))

        print("")

    # se almeno 1 url dovesse esistere, lo salva
    if len(working) != 0:
        save_link(working,type="working")
        if len(url_list) == 1:
            print("[+] URL salvato")

    print("[i] URL Testati attivi: %s\n"%(len(working)))


# Genera i link
def GenLinks(max_links):
    # lista lettere
    char = [
        "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
        "0","1","2","3","4","5","6","7","8","9"
        ] 

    # lista link generati
    links = [] 

    # lunghezza link
    length = 16

    for link in range(1, max_links + 1):

        # crea la variabile di salvataggio dei caratteri del link
        link = ""

        # pesca a caso 16 lettere e le unisce
        for lecter in range(1, length + 1):
            lecter = random.choice(char)
            link += str(lecter)

        # aggiunge .onion e salva il link in lista 'links'
        link += ".onion\n"
        links.append(str(link))

    return links


if __name__ == "__main__":
    version = 1.1

    print("")
    print("~# TorGen v%s // LS1911 (https://www.github.com/LS1911/TorGen)"%(version))
    print("~# .onion URL generator and tester")

    # verifica sistema
    if platform.system() == "Windows":
        print("\n[-] Spiacente, TorGen non è compatibile con Windows.\n")
        exit(1)

    # verifica l'installazione
    if not os.path.isfile("tgen_files/installed"):
        print("\n[-] Usa 'python3 installer.py' prima di avviare TorGen.\n")
        exit(1)

    # verifica che la major release di python sia pari o superiore a 3
    if int(sys.version.split()[0].split(".")[0]) < 3:
        print("\n[-] Usa 'python3 torgen.py' per avviare TorGen.\n")
        sys.exit(1)

    # verifica dei permessi di root
    if platform.system() != "Windows":
        if os.geteuid() != 0:
            print("\n[-] Avvia torgen.py come utente root.\n")
            exit(1)


    if len(sys.argv) == 1 or sys.argv[1] in ["-h","--help"]:
        print("""
~# ARGOMENTI:

    -h, --help          // Questa schermata
    --notest            // Non testare i link generati
    
    --file      [FILE]  // Testa URL da un FILE
    --check     [URL]   // Verifica che URL esista

~# USO:

    $ python3 torgen.py [NUM] [--notest]

    $ python3 torgen.py --file [FILE]
    $ python3 torgen.py --check [URL]
        """)
        exit(0)

    # impostazioni programma
    max_links = 0

    # ottiene la posizione di "-f" e aggiunge 1 
    if "--file" in sys.argv:
        try:
            file_index = sys.argv.index("--file") + 1
            file = sys.argv[file_index]

            if os.path.isfile(file):

                f = open(file, "r").readlines()
                link_tester(f)

            else:
                print("\n[-] File non trovato o non valido: %s\n"%(file))
                exit(1)
            
        except IndexError:
            print("\n[-] Argomento mancante richiesto: FILE\n")
            exit(1)

    elif "--check" in sys.argv:
        try:

            check_index = sys.argv.index("--check") + 1
            url = sys.argv[check_index]

            # verifica l'esistenza di un URL
            url = [url]
            link_tester(url)

        except IndexError:
            print("\n[-] Argomento mancante richiesto: URL\n")
            exit(1)

    else:

        # ottiene il numero di link da generare, genera e testa
        try:
            generate = int(sys.argv[1])
            max_links = generate

            # Genera e salva URL
            links_list = GenLinks(max_links)
            print("\n[+] URL generati: %s"%(max_links))
            print("[+] URL salvati") # save_link stampa a schermo "[i] File: ..."
            save_link(links_list,type="links")

            print("")

            if "--notest" not in sys.argv:
                link_tester(links_list)

        except ValueError:
            print("\n[-] NUM non valido")
            exit(1)
