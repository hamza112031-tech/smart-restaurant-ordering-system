import csv

PREPARATION_TIMES = {
    "Koshari Medium": 10,
    "Grilled Chicken Meal": 25, 
    "Shish Tawook Sandwich": 15,
    "Beef Burger Combo": 20,
    "Margherita Pizza Medium": 18,
    "Fatteh with Chicken": 22,
    "Fried Shrimp Plate": 15,
    "Caesar Salad": 8,
    "Chicken Pasta Alfredo": 20,
    "Molokhia with Rice and Chicken": 30
}

def load_menu():
    menu = {}
    with open('menu_from_clients.txt', 'r') as file_client_menu:
        for linec in file_client_menu:
            print('\t\t*this the items from clients*\n if you like any of them, add them to the order:')
            print(linec)
    with open('menu2.txt', 'r') as filename:
        for line in filename:
            if '-' in line:
                item, price = line.strip().split('-', 1)
                menu[item.strip()] = float(price.strip())
    print('this available items')
    for item, price in menu.items():
        print(f'-{item}:{price}')
    return menu

def search_menu():
    while True:
        keyword = input("Enter the name of the item to search in the menu: ").strip().lower()
        found = False
        with open("menu2.txt", "r") as file:
            print("\nMatching items:")
            for line in file:
                if '-' in line:
                    item, price = line.strip().split('-', 1)
                    if keyword in item.lower():
                        print(f"{item}: {price} EGP")
                        found = True
        if found:
            return
        else:
            print("Sorry, no items match your keyword. Please try again.")

def get_best_selling_item():
    sales = {}
    with open('saved_orders.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if 'x' in line and '=' in line:
                item_part, rest = line.split('x', 1)
                item = item_part.strip()
                quantity_part = rest.split('=', 1)[0]
                quantity = int(quantity_part.strip())
                sales[item] = sales.get(item, 0) + quantity
    if not sales:
        print("No orders found.")
        return
    best_item = max(sales, key=sales.get)
    print(f"The best selling item is: {best_item}")

def save_order():
    menu = load_menu()
    orders = {}
    menu_lower = {item.lower(): item for item in menu}
    while True:
        user_input = input("\nEnter your order: ").strip().lower()
        matches = [menu_lower[key] for key in menu_lower if user_input in key]
        if not matches:
            print("This item not found, please try again")
            continue
        if len(matches) == 1:
            confirm = input(f"Do you mean {matches[0]}? (yes/no): ").strip().lower()
            if confirm != 'yes':
                continue
            chosen_item = matches[0]
        else:
            print("Which one do you mean?")
            for i, item in enumerate(matches, 1):
                print(f"{i}. {item}")
            choice = int(input("Enter the number: "))
            if choice < 1 or choice > len(matches):
                print("Invalid choice, please try again")
                continue
            chosen_item = matches[choice - 1]
        if chosen_item in orders:
            print("You already ordered this item.")
            continue
        quantity = int(input(f"How many {chosen_item} do you want? "))
        orders[chosen_item] = quantity
        print("Item added successfully")
        again = input("Do you want to add another item? (yes/no): ").strip().lower()
        if again != 'yes':
            break
    with open('saved_orders.txt', 'a') as file:
        file.write("New Order:\n")
        for item, qty in orders.items():
            total = menu[item] * qty
            file.write(f"{item} x{qty} = {total}\n")
        file.write("-" * 30 + "\n")
    print("Ok thanks, The Order added successfully")

def validate_order():
    menu = load_menu()
    with open('saved_orders.txt', 'r') as file:
        lines = file.readlines()
    print("\nValidating order...\n")
    for line in lines:
        line = line.strip()
        if line == "" or line == "New Order:" or line.startswith("-"):
            continue
        parts = line.split("=")
        left_part = parts[0]
        total = float(parts[1])
        item_and_qty = left_part.split("x")
        item = item_and_qty[0].strip()
        quantity = int(item_and_qty[1].strip())
        if item not in menu or quantity <= 0 or menu[item]*quantity != total:
            print("Order invalid:", item)
            return False
    print("Order is valid successfully")
    return True

def calculate_total(order, menu):
    total = sum(menu[item] * qty for item, qty in order.items())
    return total

def appley_discount(total, percent=0):
    first_come = input('Is this your first visit? (yes/no): ').strip().lower()
    if first_come == 'yes':
        percent = 0.30
        final_price = total * (1 - percent)
        print('Total after discount:', final_price)
        return final_price
    else:
        codes = {7:0.35, 11:0.22, 22:0.15, 33:0.10, 44:0.20}
        disc_code = int(input('Enter discount code (0-50): '))
        if disc_code in codes:
            percent = codes[disc_code]
            final_price = total * (1 - percent)
            print(f"Congrats! Your discount: {percent*100}%")
            return final_price
        print('No discount applied')
        return total

def get_available_tables(tables: dict):
    return [t for t, reserved in tables.items() if not reserved]



def register_customer(first_time: bool):
    if first_time:
        print("Welcome to your first visit! Please enter your information to register.")
        name = input("Full Name: ")
        email = input("Email Address: ")
        while True:
            phone = input("Phone Number (11 digits, 010/011/012/015): ")
            if len(phone) == 11 and phone.startswith(('010','011','012','015')):
                break
            print("Invalid phone number. Try again.")
        print("Registration complete!")
        return {"name": name, "email": email, "phone": phone}
    else:
        print("Welcome back!")
        return {"status":"returning_customer"}

def estimate_preparation_time(order):
    total_time = 0
    for item, qty in order.items():
        total_time += PREPARATION_TIMES.get(item, 0) * qty
    return total_time

def add_menu_item(menu, new_item, price, orders):
    menu[new_item] = price
    orders.append(new_item)
    with open('menu_from_clients.txt','a') as f:
        f.write(f"{new_item}:{price}\n")
    print(f"{new_item} added successfully.")
    return orders

def remove_menu_item():
    with open('menu2.txt','r') as f:
        lines = f.readlines()
    item_to_remove = input("Enter item to remove: ").strip().lower()
    new_lines = []
    for line in lines:
        if '-' in line and line.split('-')[0].strip().lower() == item_to_remove:
            print(f"{line.split('-')[0]} removed.")
            continue
        new_lines.append(line)
    with open('menu2.txt','w') as f:
        f.writelines(new_lines)

def notify_low_stock_by_percentage_concise(inventory):
    threshold = max(inventory.values()) * 0.25
    low = [item for item, qty in inventory.items() if qty <= threshold]
    if low:
        print("Low stock items:", ', '.join(low))
    return low

def export_daily_sales_to_csv(sales, filename):
    header = ['Product','Quantity Sold']
    with open(filename,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for item, qty in sales.items():
            writer.writerow([item, qty])
    print(f"Sales exported to {filename}")

def generate_daily_report(orders, menu):
    report = {}
    for order in orders:
        for item, qty in order.items():
            if item in menu:
                if item not in report:
                    report[item] = {"quantity": qty, "revenue": qty*menu[item]}
                else:
                    report[item]["quantity"] += qty
                    report[item]["revenue"] += qty*menu[item]
    return report

def load_saved_orders():
    all_orders = []
    current_order = {}
    with open("saved_orders.txt",'r') as f:
        for line in f:
            line = line.strip()
            if line=="New Order:":
                current_order = {}
            elif line.startswith("-"):
                if current_order:
                    all_orders.append(current_order)
            elif "x" in line and "=" in line:
                item, rest = line.split("x")
                qty = int(rest.split("=")[0].strip())
                current_order[item.strip()] = qty
    return all_orders