import requests
import json

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
    for page in range(1, 11):
        querystring = {"page":f"{page}","limit":"48","discount_types":"sale"}
        
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        page_data = response.json()
        data.extend(page_data["data"])

    return data


def get_articles(data):
    articles = {}
    counter = 0
    for item in data:
        for sale in item["sales"]:
            article_card = {
                f"{sale.get('id')}": 
                    {
                        "brand": item.get("producerName"),
                        "name": item.get("name"),
                        "model": item.get("model"),
                        "full_price": item.get("oldPrice"),
                        "normal_price": item.get("price"),
                        "sale_price": sale.get("price"),
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
    with open("sales_article.json", "w", encoding="utf-8") as file:
        json.dump(articles, file)


def main():
    data = get_json()
    articles = get_articles(data)
    write_to_json(articles)


if __name__ == '__main__':
    main()
