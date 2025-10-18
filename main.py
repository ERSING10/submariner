import requests
from colorama import init, Fore, Style, Back
from queue import Queue, Empty
from threading import Thread, Lock
import time
import argparse
init()

q = Queue()



scanned_count = 0
total_count = 0
count_lock = Lock()

def scan_subdomain(subdomain, domain):
    global scanned_count
    with count_lock:
         scanned_count +=1
         current = scanned_count

    clear_string = subdomain.strip()
    url = f"https://{clear_string}.{domain}"
    try:
        requests.get(url,timeout=3)
    except requests.exceptions.RequestException:
        # print(Back.BLACK, Fore.RED + f"[-] {url} bulunamadı" + Style.RESET_ALL)
        pass
    else:
        print(Back.BLACK, Fore.GREEN + f"[{current}/{total_count}] [+] {url} bulundu" + Style.RESET_ALL)

def worker(domain):
    while True:
        try:
            subdomain = q.get(timeout=0.5)
            if subdomain is None:
                break
            scan_subdomain(subdomain,domain)
            q.task_done()
        except Empty:
            continue



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="basit subdomain tarayıcı")
    parser.add_argument('-d','--domain', required=True,help="Taranacak hedef alan adı (örn: google.com)")
    parser.add_argument('-w','--wordlist',required=True,help="kelime listesi dosyası")
    parser.add_argument('-t','--threads',default=50,type=int)
    args = parser.parse_args()

    try:
        for _ in range(args.threads):
            t = Thread(target=worker,args=(args.domain,))
            t.daemon = True
            t.start()

        with open(args.wordlist,"r") as file:
            wordlist = file.readlines()
            total_count = len(wordlist)
        print(Back.BLACK, Fore.CYAN + f"[*]{len(wordlist)} subdomain taranacak" + Style.RESET_ALL)
        for subdomain in wordlist:
            clear_string = subdomain.strip()
            q.put(clear_string)        
        
        for _ in range(args.threads):
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


