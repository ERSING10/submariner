import requests
from colorama import init, Fore, Style, Back
from queue import Queue
from threading import Thread

init()

q = Queue()

target_domain = "github.com"

def scan_subdomain(subdomain):
    clear_string = subdomain.strip()
    url = f"https://{clear_string}.{target_domain}"
    try:
        requests.get(url)
    except requests.exceptions.RequestException as e:
        # print(Back.BLACK, Fore.RED + f"[-] {url} bulunamadı" + Style.RESET_ALL)
        pass
    else:
        print(Back.BLACK, Fore.GREEN + f"[+] {url} bulundu" + Style.RESET_ALL)

def worker():
    while True:
        subdomain = q.get()
        if subdomain is None:
            break
        scan_subdomain(subdomain)
        q.task_done()

if __name__ == "__main__":
    try:
        for _ in range(50):
            t = Thread(target=worker)
            t.daemon = True
            t.start()

        with open('wordlist.txt','r') as file:
            for subdomain in file:
                clear_string = subdomain.strip()
                q.put(clear_string)        
        
        for _ in range(50):
            q.put(None)
        
        q.join()
    except:
        print(Back.BLACK, Fore.YELLOW + f"\n[] Tarama durduruluyor!" + Style.RESET_ALL)
    finally:
        print(Back.BLACK, Fore.YELLOW + f"\n[] Tarama bitti!" + Style.RESET_ALL)


