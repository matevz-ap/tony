import requests
from bs4 import BeautifulSoup

USELESS = ["Nasičene maščobne kisline", "Sladkorji", "Prehranske vlaknine", "Porcija"]


def table(data):
    # Calculate the maximum width of each column
    col_widths = [max(len(str(item)) for item in col) for col in zip(*data)]

    # Format each row with proper column alignment
    def format_row(row):
        return " | ".join(f"{item:<{col_widths[i]}}" for i, item in enumerate(row))

    header = format_row(["Dish", "Calries", "Fat", "Carbs", "Protein"])
    separator = " | ".join("-" * width for width in col_widths)
    rows = [format_row(row) for row in data]

    # Combine everything into a monospaced code block
    return f"```\n{header}\n{separator}\n" + "\n".join(rows) + "\n```"


def get_menu_dishes(date: str) -> list[str]:
    url = f"https://www.restavracija123.si/api/getDailyMenu/4698/{date}/"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "content-type": "application/json; charset=utf-8",
        "dnt": "1",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.restavracija123.si/?restaurantid=4698&cn-reloaded=1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.HTTPError as e:
        print(e)
        return []
    return response.json()["dnevna"]


def get_nutrients(food: str) -> list:
    url = f"https://www.restavracija123.si/foods/{food}/"
    headers = {
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.HTTPError as e:
        print(e)
        return {}

    table = BeautifulSoup(response.text, "html.parser").find_all("table")[0]
    data = []

    for tr in table.find_all("tr"):
        d = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(d) != 2 or d[0] in USELESS or "kJ" in d[1]:
            continue
        data.append(d[1])
    return data
