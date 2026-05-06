# Task 1: Discount Rules

user_input = input("Enter the order amount: ")

# Check if input is numeric
if user_input.isdigit():
    order_amount = int(user_input)

    # Apply discount rules
    if order_amount >= 2000:
        discount = order_amount * 0.15
    elif order_amount >= 1500:
        discount = order_amount * 0.10
    elif order_amount >= 1000:
        discount = order_amount * 0.07
    else:
        discount = 0

    # Calculate final amounts
    subtotal = order_amount - discount
    tax = subtotal * 0.05
    final_amount = subtotal + tax

    # Print results
    print("Discount:", discount)
    print("Subtotal:", subtotal)
    print("Tax:", tax)
    print("Final Amount:", final_amount)

else:
    print("Invalid input. Please enter a valid number.")