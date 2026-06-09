# Main
from hamza import *
def hamza_main():
    first_floor_tables = {f"table_{i}": False for i in range(1,16)}
    first_floor_vips = {f"vip_{i}": False for i in range(1,6)}
    all_tables = {**first_floor_tables, **first_floor_vips}
    menu = load_menu()  # load menu once to use later
    while True:
        print("\n== Welcome to my luxurious restaurant ==")
        print("1. Agent login")
        print("2. Customer access")
        print("0. Exit")
        choice = input("Choose option: ").strip()

        if choice == '0':
            print("Goodbye!")
            break

        elif choice == '1':  # Agent
            password = input("Enter agent password: ")
            if password != '2025':
                print("Wrong password! Access denied.")
                continue
            print("Welcome Agent! You can manage the restaurant now.")

            while True:
                print("\n-- Agent Menu --")
                print("1. Register customer")
                print("2. Estimate preparation time")
                print("3. Add new item to menu")
                print("4. Remove item from menu")
                print("5. Notify low stock items")
                print("6. Export daily sales to CSV")
                print("7. Generate daily report")
                print("0. Logout")
                a_choice = input("Choose option: ").strip()

                if a_choice == '0':
                    break
                elif a_choice == '1':
                    register_customer(first_time=True)
                elif a_choice == '2':
                    all_orders = load_saved_orders()
                    if all_orders:
                        total_time = estimate_preparation_time(all_orders[-1])
                        print("Estimated preparation time:", total_time)
                    else:
                        print("No orders saved yet.")
                elif a_choice == '3':
                    new_item = input("Enter new item name: ")
                    price = input("Enter price: ")
                    orders = []
                    add_menu_item(menu, new_item, price, orders)
                    print("Item added successfully!")
                elif a_choice == '4':
                    remove_menu_item()
                elif a_choice == '5':
                    warehouse_inventory = {item: 50 for item in menu}  # example stock
                    low_stock_items = notify_low_stock_by_percentage_concise(warehouse_inventory)
                    if low_stock_items:
                        print("Low stock items:", low_stock_items)
                    else:
                        print("Stock is sufficient.")
                elif a_choice == '6':
                    daily_sales = {}
                    while True:
                        item_name = input("Enter item name (or type 'done'): ").strip()
                        if item_name.lower() == 'done':
                            break
                        quantity = int(input(f"Quantity sold for {item_name}: "))
                        daily_sales[item_name] = quantity
                    filename = input("Enter CSV filename: ")
                    export_daily_sales_to_csv(daily_sales, filename)
                    print("Sales exported successfully!")
                elif a_choice == '7':
                    all_orders = load_saved_orders()
                    report = generate_daily_report(all_orders, menu)
                    print("\nDaily Report:")
                    for item, data in report.items():
                        print(f"{item} - Total Sold: {data['quantity']}, Revenue: {data['revenue']} EGP")
                else:
                    print("Wrong choice! Try again.")
        elif choice == '2':
                print("Welcome Customer!")
                menu = load_menu()
                while True:
                    print("\n-- Customer Mode --")
                    print("1. Load the menu")
                    print("2. Search for item in menu")
                    print("3. Get best selling item")
                    print("4. make an order")
                    print("5. Validate your order")
                    print("6. Calculate the total")
                    print("7. take a discount")
                    print("8. ask for available tables")
                    print("0. Back to main menu")
                    c_choice = input("Choose option: ").strip()
                    if c_choice == '0':
                        break
                    elif c_choice == '1':
                        load_menu()
                    elif c_choice == '2':
                        search_menu()
                    elif c_choice == '3':
                        get_best_selling_item()
                    elif c_choice == '4':
                        save_order()
                    elif c_choice == '5':
                        validate_order()
                    elif c_choice == '6':
                        all_orders = load_saved_orders()
                        if all_orders:
                            total = calculate_total(all_orders[-1], menu)
                            print("Total:", total)
                        else:
                            print("No orders saved yet.")
                    elif c_choice == '7':
                        all_orders = load_saved_orders()
                        if all_orders:
                            total = calculate_total(all_orders[-1], menu)
                            appley_discount(total)
                        else:
                            print("No orders saved yet.")
                    elif c_choice == '8':
                        first_floor_tables = {f"table_{i}": False for i in range(1, 16)}
                        first_floor_vips = {f"vip_{i}": False for i in range(1, 6)}
                        all_tables = {**first_floor_tables, **first_floor_vips}
                        available = get_available_tables(all_tables)
                        print("Available tables:", available)
                    else:
                        print("Wrong choice! Please select a number from 0-8.")
hamza_main()