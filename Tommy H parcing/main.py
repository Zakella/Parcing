import requests
import json
from bs4 import BeautifulSoup


def parce():
    with open("headers.json") as file:
        headers = json.load(file)
        # print(headers)
    #
    # url = "https://usa.tommy.com/en/tommy-hilfiger-sale"
    # response = requests.session().get(url=url, headers=headers)
    # with open("index.html", "w") as file:
    #     file.write(response.text)
    #
    # print(response.text)

    with open("index.html") as file:
        soup = BeautifulSoup(file.read(), "lxml")
        all_refs = soup.find_all(class_="productImage focusParent")
        url_list = []
        for item in all_refs:
            products = item.find_all(class_="productThumbnail")
            for value in products:
                url_list.append(value.get("href"))

    for item in url_list:
        print(item)

        # print(item)
        response = requests.session().get(url=item, headers=headers)
        with open("index_inner.html", "w") as file:
            file.write(response.text)
            print(response.text)
        item_dict = {}
        with open("index_inner.html") as file:
            soup = BeautifulSoup(file.read(), "lxml")
            data = soup.find_all(class_="productView")
            for value in data:
                item_dict["name"] = "".join([name_value.text for name_value in value.find_all(class_="productNameInner")])

                item_dict["price"] = "".join([name_value.text for name_value in value.find_all(class_="price listPrice")])
                item_dict["sale_price"] = "".join(
                    [name_value.text for name_value in value.find_all(class_="price offerPrice2")])
                print(item_dict)

                a = value.find_all(class_="namePartPriceContainer")
                # for i in a:
                #     print(i.value.find_all(class_="namePartPriceContainer"))
                # print(value.find_all(class_="price offerPrice2"))
                # print(item_dict)


                # item_dict["name"] = "".join([name_value for name_value in value.find_all(class_="productNameInner")])
                prices = value.find_all(class_="namePartPriceContainer")
                # a = prices.find_all(class_="price offerPrice2")
                # for price in prices:
                #     print(price)
                # for b in a:
                #     print(b.text)
                # print(value.find_all(class_= "productNameInner").get("itemprop"))
                # item_dict["name"] = value.
                # print(value)

        break

        # print(f"Total items in page {i}")



if __name__ == '__main__':
    parce()

# https://usa.tommy.com/ProductListingView?includeLowStockIndicator=true&catalogId=10551&isHomeDepartment=false&pageSize=30&disableProductCompare=true&langId=-1&storeId=10151&categoryId=3074457345617404775&currentCategoryIdentifier=UNISEX_SALE_HID&imageBadgeIgnoreCategoryCodeParam=UNISEX_SALE_HID&beginIndex=30&minFacetCount=1&colorfacetselected=false&cache=true
