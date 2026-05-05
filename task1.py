# List of products 
products = ["School bag", "Water bottle", "Laptop", "Pencil case", "Notebook", "Shoes"]

# Tuple for a sample product
sample_product = ("School bag", 800, "Stationery")

print("Second product:", products[1])
print("Last product:", products[-1])

# Add two new products
products.append("Calculator")
products.append("Lunch box")
print("Updated product list:", products)

sample_product_list = list(sample_product)
sample_product_list[1] = 850  # update price
sample_product = tuple(sample_product_list)

print("Updated sample product:", sample_product)