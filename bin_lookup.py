import requests

def get_bin_info(bin):
    try:
        res = requests.get(f"https://lookup.binlist.net/{bin}")
        if res.status_code == 200:
            data = res.json()
            return {
                "country_name": data["country"]["name"],
                "bank": data.get("bank", {}).get("name", "Desconocido")
            }
    except:
        pass
    return {"country_name": "Desconocido", "bank": "Desconocido"}
