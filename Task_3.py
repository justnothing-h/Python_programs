orders = []

# Infinite loop for menu
while True:
    print("\nMenu:")
    print("1. Add Order")
    print("2. Show orders and totals")
    print("q. Quit")

    choice = input("Enter your choice: ")

    # Option 1: Add order
    if choice == "1":
        order_amount = input("Enter the order amount: ")

        # Validate input
        if order_amount.isdigit():
            orders.append(int(order_amount))
        else:
            print("Invalid input.")
            continue

    # Option 2: Show all orders with calculations
    elif choice == "2":
        total = 0
        print("\nOrder Summary:")

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

            # Calculate final amount with tax
            subtotal = order_amount - discount
            tax = subtotal * 0.05
            final_amount = subtotal + tax

            total += final_amount

            print("Order:", order_amount)
            print("Final Amount:", final_amount, "\n")

        print("Total:", total)

    # Option to exit program
    elif choice.lower() == "q":
        print("Exiting...")
        break

    # Handle invalid menu input
    else:
        print("Invalid choice.")
        continue