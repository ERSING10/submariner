import requests
from colorama import init, Fore, Style, Back
from queue import Queue, Empty
from threading import Thread, Lock
import time

init()

q = Queue()

target_domain = "github.com"

scanned_count = 0
total_count = 0
count_lock = Lock()

def scan_subdomain(subdomain):
    global scanned_count
    with count_lock:
         scanned_count +=1
         current = scanned_count

    clear_string = subdomain.strip()
    url = f"https://{clear_string}.{target_domain}"
    try:
        requests.get(url,timeout=3)
    except requests.exceptions.RequestException:
        # print(Back.BLACK, Fore.RED + f"[-] {url} bulunamadı" + Style.RESET_ALL)
        pass
    else:
        print(Back.BLACK, Fore.GREEN + f"[{current}/{total_count}] [+] {url} bulundu" + Style.RESET_ALL)

def worker():
    while True:
        try:
            subdomain = q.get(timeout=0.5)
            if subdomain is None:
                break
            scan_subdomain(subdomain)
            q.task_done()
        except Empty:
            continue

if __name__ == "__main__":
    try:
        for _ in range(50):
            t = Thread(target=worker)
            t.daemon = True
            t.start()

        with open('wordlist.txt','r') as file:
            wordlist = file.readlines()
            total_count = len(wordlist)
        print(Back.BLACK, Fore.CYAN + f"[*]{len(wordlist)} subdomain taranacak" + Style.RESET_ALL)
        for subdomain in wordlist:
            clear_string = subdomain.strip()
            q.put(clear_string)        
        
        for _ in range(50):
            q.put(None)
        
        while not q.empty():
            try:
                time.sleep(0.1)
            except KeyboardInterrupt:
                print(Back.BLACK, Fore.YELLOW + f"\n[] Tarama durduruluyor!" + Style.RESET_ALL)
                time.sleep(0.5)
                break
    except:
        print(Back.BLACK, Fore.YELLOW + f"\n[] Tarama durduruluyor!" + Style.RESET_ALL)
    finally:
        print(Back.BLACK, Fore.YELLOW + f"\n[] Tarama bitti!" + Style.RESET_ALL)


