import requests

target_domain = "github.com"

wordlist = [
    "docs",
    "status",
    "yokkkk",
    "api",
    "kelime5",
            ]

for subdomain in wordlist:
    url = f"https://{subdomain}.{target_domain}"
    try:
        requests.get(url)
    except requests.exceptions.RequestException as e:
        pass
    else:
        print(f"{url} bulundu")
