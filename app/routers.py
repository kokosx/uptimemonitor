import requests

def check_url(url: str) -> int | str:
    try:
        res = requests.head(url, timeout=5)
        
        return res.status_code
        
    except requests.exceptions.RequestException as e:
        return f"{e}"
        