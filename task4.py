products = ["Laptop", "Shirt", "Phone", "Shoes", "Tablet", "Watch"]

price_dict = {
    "Laptop": 50000,
    "Shirt": 1500,
    "Phone": 20000,
    "Shoes": 3000,
    "Tablet": 25000,
    "Watch": 2000
}

categories = ["Electronics", "Clothing", "Electronics", "Footwear", "Electronics", "Accessories"]

catalog = []

for i in range(len(products)):
    product = products[i]
    price = price_dict[product]
    category = categories[i]
    catalog.append((product, price, category))

print("Catalog:")
for item in catalog:
    print(item)

category_to_products = {}

for item in catalog:
    product = item[0]
    category = item[2]

    if category not in category_to_products:
        category_to_products[category] = []

    category_to_products[category].append(product)

print("\nCategory to Products:")
print(category_to_products)

max_category = ""
max_count = 0

for category in category_to_products:
    count = len(category_to_products[category])
    
    if count > max_count:
        max_count = count
        max_category = category

print("\nCategory with maximum products:", max_category)

print("Products in that category:")
for product in category_to_products[max_category]:
    print(product)