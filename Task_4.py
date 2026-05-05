daily = [200, 150, 0, 400, 50, -1, 300]

total_sales = 0

# Loop through daily sales
for amount in daily:

    # Check for corrupted data
    if amount == -1:
        print("Corrupted data found. Stopping...")
        break

    # Skip days with no sales
    if amount == 0:
        print("No sales today.")
        continue

    # Add valid sales to total
    total_sales += amount

    # Print running total
    print("Running total:", total_sales)
    print("Processing amount:", amount)

# Final total after loop
print("Total Sales:", total_sales)