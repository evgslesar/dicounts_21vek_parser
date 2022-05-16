import requests
import json
import csv

def get_json():
    url = "https://gate.21vek.by/special-offers/api/products/list"
    payload = ""
    headers = {
        "Accept": "application/vnd.api+json",
        "Accept-Language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,de;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Type": "application/vnd.api+json",
        "Origin": "https://www.21vek.by",
        "Pragma": "no-cache",
        "Referer": "https://www.21vek.by/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"'
    }

    data = []
    for page in range(1, 16):
        querystring = {"page":f"{page}","limit":"48","discount_types":"sale"}
        
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        page_data = response.json()
        data.extend(page_data["data"])

    return data


def get_articles():
    data = get_json()
    articles = {}
    counter = 0
    for item in data:
        for sale in item["sales"]:
            if sale.get("promoDiscount") != 0:
                article_card = {
                    f"{sale.get('id')}": 
                        {
                            "sale_id": sale.get('id'),
                            "brand": item.get("producerName"),
                            "name": item.get("name"),
                            "model": item.get("model"),
                            "full_price": float(item.get("oldPrice")),
                            "normal_price": float(item.get("price")),
                            "sale_price": float(sale.get("price")),
                            "discount": sale.get("promoDiscount"),
                            "description": sale.get("description"),
                            "item_url": "https://www.21vek.by/" + item.get("url"),
                            "sale_picture": sale.get("image"),
                            "item_picture": item.get("picture")
                        }
                    }

                articles.update(article_card)
                counter += 1
    print(counter)

    return articles


def write_to_json(articles):
    with open("sales_articles.json", "w", encoding="utf-8") as file:
        json.dump(articles, file, indent=4, ensure_ascii=False)


def write_to_csv(articles):
    with open("sales_articles.csv", "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Артикул распродажи", "Наименование", "Бренд", 
                        "Модель", "Полная цена", "Обычная цена", "Цена распродажи", 
                        "Скидка в %", "Описание", "Ссылка на товар", 
                        "Изображение уцененного", "Обычное изображение"])
        for article in articles.values():
            writer.writerow(list(article.values()))



def main():
    articles = get_articles()
    write_to_json(articles)


if __name__ == '__main__':
    main()
