import requests
from fake_useragent import UserAgent
import vs_config

DOMEN = "https://www.victoriassecret.com/"
PICTDOMEN = "https://www.victoriassecret.com/p/280x373/"


def get_data(cat_name):
    headers = {"user-agent": UserAgent().chrome
               }

    url_list = vs_config.dict_url[cat_name]
    categories_id = []
    counter = 0
    item_list = []
    succes_times = 0
    for url in url_list["url"]:
        response = requests.session().get(url=url, headers=headers)
        if response.status_code == 200:
            succes_times += 1
            data = response.json()
            if isinstance(data, dict):
                stacks = data.get("stacks")
                for stack in stacks:
                    for item in stack.get("list"):
                        item_list.append(parce_data(item, categories_id))
                        counter += 1
            if isinstance(data, list):
                for item in data:
                    item_list.append(parce_data(item, categories_id))
                    counter += 1

    print(f"Total in {cat_name} {counter} items")
    if succes_times == len(url_list["url"]):
        return item_list
    else:
        return "Ups! Server is gone, try again later!"


def parce_data(list_item, list_id):
    item_card = {}
    masterStyleId = list_item.get("masterStyleId")
    if not masterStyleId in list_id:
        name = list_item.get("name")
        family = list_item.get("family")
        item_card["name"] = f" {family} {name}"
        item_card["family"] = family
        item_card["url"] = DOMEN + list_item.get("url")
        item_card["price"] = float(list_item.get("price").replace("$", ""))
        sale_price = list_item.get("salePrice").replace("$", "")
    item_card["images"] = []
    if not sale_price:
        item_card["sale_price"] = 0
    else:
        item_card["sale_price"] = float(sale_price)
    item_card["altPrices"] = list_item.get("altPrices")
    item_card["min_price"] = item_card["price"] if not item_card["sale_price"] else item_card[
        "sale_price"]
    item_card["alt_price1"] = 0
    item_card["alt_price2"] = 0
    if item_card["altPrices"] != None:
        for price in item_card['altPrices']:
            alt_price = price.split("/$")
            try:
                quant_1 = float(alt_price[0][-1])
                amount_1 = float(alt_price[1].split()[0].replace(",", ""))
                item_card["alt_price1"] = amount_1 / quant_1 if quant_1 != 0 else 0
            except Exception:
                pass

        try:
            quant_2 = alt_price[-2].replace(",", "")[-1]
            amount_2 = alt_price[-1]
            item_card["alt_price2"] = amount_2 / quant_2 if quant_2 != 0 else 0
        except Exception:
            pass

    item_card["min_price"] = min(
        filter(None, (item_card["min_price"], item_card["alt_price1"], item_card["alt_price2"])))

    main_image = list_item.get("productImages")[0]
    for image in list_item.get("swatches"):
        try:
            if main_image != image.get("productImage"):
                item_card["images"].append(PICTDOMEN + image.get("productImage") + ".jpg")

        except:
            item_card["images"].append(PICTDOMEN + list_item.get("productImages")[0] + ".jpg")

    item_card["main_image"] = PICTDOMEN + main_image + ".jpg"
    return item_card
    # counter += 1


#
# if __name__ == "__main__":
#     data = get_data("sale")
#     print(data)

