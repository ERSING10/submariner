import requests

target_domain = "github.com"

with open('wordlist.txt','r')as file:
    for subdomain in file:
        clear_string = subdomain.strip()
        url = f"https://{clear_string}.{target_domain}"
        try:
            requests.get(url)
        except requests.exceptions.RequestException as e:
            pass
        else:
            print(f"{url} bulundu")
