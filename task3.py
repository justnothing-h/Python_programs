price_dict = {
    "Apple": 100,
    "Banana": 48,
    "Mango": 200,
    "Grapes": 150,
    "Orange": 80,
    "Watermelon": 120,
    "Pineapple": 180,
    "Papaya": 90,
    "Kiwi": 110,
    "Strawberry": 250
}

# Add new product
price_dict["Litchi"] = 130

# Update price
price_dict["Banana"] = 50

# Remove product
removed_item = price_dict.pop("Grapes", "Not Found")

print("Updated price dictionary:", price_dict)

# Average price
average_price = sum(price_dict.values()) / len(price_dict)
print("Average price:", average_price)

# Max & Min priced products
max_product = max(price_dict, key=price_dict.get)
min_product = min(price_dict, key=price_dict.get)

print(f"Most expensive: {max_product} -> {price_dict[max_product]}")
print(f"Cheapest: {min_product} -> {price_dict[min_product]}")