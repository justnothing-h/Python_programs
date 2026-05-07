# Making the categopries set 
categories_set = {"Stationery", "Electronics", "Retail"}

# Add duplicate (should not change set)
categories_set.add("Electronics")

print("Categories:", categories_set)

# Check existence
print("Is 'Retail' present?", "Retail" in categories_set)

# Total unique categories
print("Total categories:", len(categories_set))