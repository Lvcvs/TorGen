#!/usr/bin/python
# -*- coding: utf-8 -*-
# Autore: Skull00 (https://www.github.com/Skull00)
import os # generatore
import sys # generatore
import random # generatore

from bs4 import BeautifulSoup # ispezione

end = '\033[0m'
red = '\033[1;31m'
bright_green = '\033[1;32m'
bright_yellow = '\033[1;33m'

try:
    import requests # ispezione
except ImportError:
    os.system("pip install requests && clear")
    print("\n\n[%s+%s] Pacchetti installati, riavvia il programma\n\n"%(bright_green,end))
    exit()

reload(sys)
sys.setdefaultencoding('utf8')


words = [
        "a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
        "0","1","2","3","4","5","6","7","8","9"
        ] # lista lettere

links = [] # link generati (temporanei)


Session = requests.session() # sessione Tor
Session.proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
    }

def link_tester(link):
    try:
        response = Session.get(link, timeout=20)
        code = response.status_code
        title = BeautifulSoup(response.text, features='lxml')
        title = title.title.text

        return code, title
    except KeyboardInterrupt:
        print("\r  \n[%s-%s] Interrotto\n"%(red,end))
        exit()
    except:# requests.exceptions.ConnectionError:
        return int(404), None


def save_link(link):
    save_file = open("links.txt","a")
    save_file.write(link)
    save_file.close()


def GenLinks(max_links):
    for e in range(1, max_links + 1):
        length = 16
        link = ""

        for e in words:
            if max_links != None:
                if len(links) == max_links:
                    break

            letter = random.choice(words)
            link += str(letter)

            if len(link) == length:
                link += ".onion\n"

                links.append(str(link))
                save_link(link)

    print("[%s+%s] Links generati\n"%(bright_green,end))


if __name__ == "__main__":
    if os.path.isfile("links.txt") == False:
        os.system("touch links.txt && chmod 777 links.txt")
    if os.path.isfile("working_links.txt") == False:
        os.system("touch working_links.txt && chmod 777 working_links.txt")

    print("""
[# TorGen v1.0 ]-[ .onion link generator (and tester) ]-[ ~ Skull00

[# I link generati saranno salvati in 'links.txt'
[# I link testati e funzionati saranno salvati in 'working_links.txt'
    """)

    arguments = sys.argv[1:]

    if len(arguments) != 2 or len(arguments) == 2:
        try:
            if int(arguments[0]):
                GenLinks(int(arguments[0]))
            else:
                print("[%s*%s] Uso: python torgen.py <N. LINKS> [-t,--test]\n"%(bright_yellow,end))
                exit()
        except IndexError:
            print("[%s*%s] Uso: python torgen.py <N. LINKS> [-t,--test]\n"%(bright_yellow,end))
            exit()
        except ValueError:
            print("[%s*%s] Uso: python torgen.py <N. LINKS> [-t,--test]\n"%(bright_yellow,end))
            exit()
        try:
            if arguments[1] in ["-t","--test"]:
                tested = 0
                working = 0

                for link in links:
                    if "http://" not in link:
                        link = "http://" + link
                    if "\n" in link:
                        link = link.replace("\n","")

                    tested += 1
                    print("[%s*%s] Testo link >> %s << %s/%s"%(bright_yellow,end, link, tested, len(links)))

                    code, title = link_tester(str(link))

                    if code == 200:
                        working += 1
                        working_writer = open("working_links.txt","a")
                        working_writer.write(str(link) + " >> %s \n"%(title))
                        working_writer.close()

                        print("[%s+%s] %s >> %s"%(bright_green,end, code, bright_green + title + end))
                    else:
                        print("[%s-%s] %s"%(red,end, code))

                    print("")

                if working != 0:
                    print("[%s+%s] Link attivi: %s\n"%(bright_green,end, working))
                else:
                    print("[%s-%s] Link attivi: %s\n"%(red,end, working))
            else:
                print("[%s*%s] Uso: python torgen.py <N. LINKS> [-t,--test]\n"%(bright_yellow,end))

        except IndexError:
            pass

    exit()
