# Task 2: Process Multiple Orders

orders = [1200, 2500, 800, 1750, 3000]

total_revenue = 0
discount_items_count = 0

print("Order Summary:\n")

# Loop through each order
for order_amount in orders:

    # Apply discount rules
    if order_amount >= 2000:
        discount = order_amount * 0.15
    elif order_amount >= 1500:
        discount = order_amount * 0.10
    elif order_amount >= 1000:
        discount = order_amount * 0.07
    else:
        discount = 0

    # Calculate amounts
    subtotal = order_amount - discount
    tax = subtotal * 0.05
    final_amount = subtotal + tax

    # Update totals
    total_revenue += final_amount
    if discount > 0:
        discount_items_count += 1

    # Print details
    print("Order Amount:", order_amount)
    print("Discount:", discount)
    print("Subtotal:", subtotal)
    print("Tax:", tax)
    print("Final Amount:", final_amount, "\n")

# Final summary
print("Total Revenue:", total_revenue)
print("Discounted Orders:", discount_items_count)