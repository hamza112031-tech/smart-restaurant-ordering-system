# 1- load_menu *
# 2-search_menu *
# 3-get_best_selling_item *
# 4-save_order *
# 5-validate_order *
# 6-calculate_total * 
# 7-apply_discount * 
# 8-get_available_tables *

#1-register_customer *
# 2-estimate_preparation_time *
# 3-add_menu_item *
# 4-remove_menu_item *
# 5-notify_low_stock
# 6-export_daily_sales _to_csv
# 7-generate_daily_report

#function 1 (load menu)
def load_menu():
    menu = {}
    file_client_menu = open('menu_from_clients.txt', 'r')
    for linec in file_client_menu:
        print('\t\t*this the items from clients*\n if you like any of them, add them to the order:')
        print(linec)
    file_client_menu.close()
    filename = open('menu2.txt', 'r')
    for line in filename:
        if '-' in line:
            item, price = line.strip().split('-', 1)
            menu[item.strip()] = float(price.strip())
    filename.close()
    print('this available items')
    for item, price in menu.items():
        print(f'-{item}:{price}')
    return menu

# Function 7
def search_menu():
    while True:
        keyword = input("Enter the name of the item to search in the menu: ").strip().lower()
        found = False
        file = open("menu2.txt", "r")
        print("\nMatching items:")
        for line in file:
            if '-' in line:
                item, price = line.strip().split('-', 1)
                if keyword in item.lower():
                    print(f"{item}: {price} EGP")
                    found = True
        file.close()
        if found:
            return
        else:
            print("Sorry, no items match your keyword. Please try again.")

#Function 8
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
                if item in sales:
                    sales[item] += quantity
                else:
                    sales[item] = quantity
    if not sales:
        print("No orders found.")
        return
    best_item = max(sales, key=sales.get)
    print(f"The best selling item is: {best_item}")

#Function 2 Save Order
def save_order():
        menu = load_menu()
        orders = {}
        menu_lower = {item.lower(): item for item in menu}
        while True:
            user_input = input("\nEnter your order: ").strip().lower()
            matches = []
            for key in menu_lower:
                if user_input in key:
                    matches.append(menu_lower[key])
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
            print("Ok thanks,The Order added successfully")

# Function 9
def validate_order():
    menu = load_menu()
    file = open('saved_orders.txt', 'r')
    lines = file.readlines()
    file.close()
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
        if item not in menu:
            print(item, "is not in the menu")
            return False
        if quantity <= 0:
            print("Invalid quantity for", item)
            return False
        correct_total = menu[item] * quantity
        if correct_total != total:
            print("Price error in", item)
            return False
    print("Order is valid successfully")
    return True

#func 3 calc total moneeeeeeeeeeey:)
def calculate_total(order,menu):
    total=0
    for item in order:
        price=menu[item]
        quantity=order[item]
        total=total+(price*quantity)
    return total

#func 4 discount :(
def appley_discount(total,percent):
    first_come=input('if that first come to here tell me (yes)')
    if first_come.lower()=='yes':
        percent = 0.30
        final_price=total*(1-percent)
        print('total after discount:',final_price)
        return final_price
    else:
        print('not every time take discount, but dont cry i a big generous,unfortunately \n you will get a discount by random\n take a number between 0 to 50')
        codes={
            7:0.35,
            11:0.22,
            22:0.15,
            33:0.10,
            44:0.20
        }
        disc_code=int(input('enter number:'))
        if disc_code in codes:
            percent=codes[disc_code]
            final_price=total*(1-percent)
            print(f'congrats! your discount {percent*100}%')
            print('total after discount:',final_price)
            return final_price
        else:
            print('no discount hahahaha for this , try again next time , have a good day')
        return total

# function 11
def get_available_tables(tables: dict) -> list:
    available = []
    for table_id, is_reserved in tables.items():
        if not is_reserved:
            available.append(table_id)
    return available
if '_name_' == "_main_":
    first_floor_tables = {f"table_{i}": False for i in range(1, 16)}
    first_floor_vips = {f"vip_{i}": False for i in range(1, 6)}
    all_tables = {**first_floor_tables, **first_floor_vips}
    print("Welcome to the Restaurant Booking System!")
    floor_choice = ""
    while floor_choice.strip().lower() not in ["first floor", "second floor"]:
        floor_choice = input("Which floor would you like? (Type: First Floor or Second Floor): ")
    if floor_choice.strip().lower() == "first floor":
        current_floor_tables = all_tables
    else:
        print("The second floor is currently full. We have selected the first floor for you.")
        current_floor_tables = all_tables
    table_type_choice = ""
    while table_type_choice.strip().lower() not in ["table", "room"]:
        table_type_choice = input("Would you like a regular table or a VIP room? (Type: table or room): ")
    if table_type_choice.strip().lower() == "table":
        print("The price for a table is 200 EGP.")
    elif table_type_choice.strip().lower() == "room":
        print("The price for a VIP room is 1000 EGP.")
    available_tables = get_available_tables(current_floor_tables)
    final_options = []
    if table_type_choice.strip().lower() == "table":
        final_options = [t for t in available_tables if t.startswith("table_")]
    elif table_type_choice.strip().lower() == "room":
        final_options = [t for t in available_tables if t.startswith("vip_")]
    print("\n--- Available Options For You ---")
    if final_options:
        print(f"Available {table_type_choice}s on the {floor_choice}:")
        for option in final_options:
            print(f"- {option}")
    else:
        print(f"Unfortunately, there are no available {table_type_choice}s on the {floor_choice} at the moment.")
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

#function 13
def register_customer(first_time: bool):
    if first_time:
        print("Welcome to your first visit! Please enter your information to register.")
        name = input("Full Name: ")
        email = input("Email Address: ")
        while True:
            phone = input("Phone Number (11 digits, starting with 010/011/012/015): ")
            if len(phone) != 11:
                print("Error: The phone number must be exactly 11 digits long. Please try again.")
                continue
            if not phone.startswith(('010', '011', '012', '015')):
                print(
                    "Error: The phone number must start with one of the following prefixes: 010, 011, 012, or 015. Please try again.")
                continue
            break
        customer_info = {
            "name": name,
            "phone": phone,
            "email": email,
            "status": "new_customer"
        }
        print("\nYour information has been registered successfully!")
        return customer_info
    else:
        customer_info = {
            "status": "returning_customer",
            "message": "Welcome back! We're happy to see you again."
        }
        return customer_info
register_customer(first_time=True)

#function 12
def estimate_preparation_time(order: dict) -> int:
    total_time = 0
    for item_name, quantity in order.items():
        if item_name in PREPARATION_TIMES:
            item_time = PREPARATION_TIMES[item_name]
            total_time += item_time * quantity
        else:
            print(f"Warning: Item '{item_name}' not found in the menu. Skipping.")
    return total_time
if '_name_' == "_main_":
    print("Welcome to the Restaurant Ordering System!")
    print("Type 'done' when you are finished with your order.")
    print("-" * 30)
    customer_order = {}
    while True:
        user_input = input("What would you like to order?: ").strip()
        if user_input.lower() == 'done':
            break
        if user_input in PREPARATION_TIMES:
            if user_input in customer_order:
                customer_order[user_input] += 1
            else:
                customer_order[user_input] = 1
            item_time = PREPARATION_TIMES[user_input]
            print(f"'{user_input}' has been added. Preparation time: {item_time} minutes.")
        else:
            print(f"Sorry, '{user_input}' is not available in our restaurant.")
    print("-" * 30)
    if customer_order:
        total_time = estimate_preparation_time(customer_order)
        print(f"Your final order is: {customer_order}")
        print(f"The estimated total preparation time for your order is: {total_time} minutes.")
    else:
        print("Maybe next time! You did not order anything.")

#func 5 add new item to menu from clients
def add_menu_item(menu, new_item, price_n_item,orders):
    with open('menu_from_clients.txt','a') as clientsfile:
        clientsfile.write(f'{new_item}:{price_n_item}\n')
        if new_item and price_n_item:
           menu[new_item]=price_n_item
           orders.append(new_item)
    return orders

#Function 6
def remove_menu_item():
    with open("menu2.txt", "r") as file:
        lines = file.readlines()
    print("\n\t*Current Menu*")
    for line in lines:
        print(line.strip())
    item_to_remove = input("\nEnter the item to remove: ").strip().lower()
    found = False
    updated_lines = []
    for line in lines:
        if '-' in line:
            item, price = line.strip().split('-', 1)
            if item_to_remove == item.lower():
                found = True
                print(f"\nItem '{item}' found and will be deleted.")
                print("\nWhy would you like to delete this item?")
                print("1. I do not prefer it")
                print("2. It is a bad item")
                print("3. It is too expensive")
                print("4. Other")
                reason_for_deletion = input("Choose your answer (1-4): ")
                if reason_for_deletion == "1":
                    print("Ok thanks (:")
                elif reason_for_deletion == "2":
                    reason = input("Write why it is a bad item: ")
                elif reason_for_deletion == "3":
                    recommended_cost = input("What is your recommended cost? ")
                else:
                    other_reason = input("Write your answer please: ")
                continue
        updated_lines.append(line)
    if found:
        with open("menu2.txt", "w") as file:
            file.writelines(updated_lines)
        print("\nItem removed successfully.")
    else:
        print("\nItem not found in the menu!")
    print("\n--- Updated Menu ---")
    if updated_lines:
        for line in updated_lines:
            print(line.strip())
    else:
        print("The menu is now empty.")

#function 14
def notify_low_stock_by_percentage_concise(inventory: dict) -> list:
    if not inventory:
        return []
    max_quantity = max(inventory.values())
    threshold = max_quantity * 0.25
    return [item for item, quantity in inventory.items() if quantity <= threshold]
if __name__ == "__main__":
    warehouse_inventory = {
        "Koshari Medium": 100,
        "Grilled Chicken Meal": 80,
        "Shish Tawook Sandwich": 25,
        "Beef Burger Combo": 15,
        "Margherita Pizza": 5,
        "Fattah with Chicken": 26,
        "Fried Shrimp Plate": 50,
        "Caesar Salad": 65,
        "Chicken Pasta Alfredo": 20,
        "Molokhia with Rice and Chicken": 66
    }
    low_stock_items = notify_low_stock_by_percentage_concise(warehouse_inventory)
    if low_stock_items:
        print(" Alert: Low Stock!")
        print(f"Items that need restocking: {', '.join(low_stock_items)}")
    else:
        print(" Stock is sufficient, no items are low.")
register_customer('first_time: bool')
get_available_tables('tables: dict')
estimate_preparation_time('order: dict')
notify_low_stock_by_percentage_concise('inventory: dict')

#Function 15
import csv
def export_daily_sales_to_csv(sales: dict, filename: str) -> None:
    header = ['Product', 'Quantity Sold']
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

        for item, quantity in sales.items():
            writer.writerow([item, quantity])

if __name__ == "__main__":

    print("--- Restaurant Daily Sales Exporter ---")

    daily_sales = {}
    while True:
        item_name = input("Enter item name (or type 'done' to finish): ").strip()
        if item_name.lower() == 'done':
            break
        quantity_str = input(f"Enter quantity sold for '{item_name}': ")

        try:
            quantity = int(quantity_str)
            daily_sales[item_name] = quantity
            print(f"Added: {item_name} - {quantity}\n")
        except ValueError:
            print("Invalid input. Please enter a whole number for the quantity.\n")
    if not daily_sales:
        print("No sales data was entered. Exiting program.")
    else:
        output_filename = input("Enter the desired filename for the CSV (e.g., daily_sales.csv): ").strip()
        if not output_filename.lower().endswith('.csv'):
            output_filename += '.csv'
        export_daily_sales_to_csv(daily_sales, output_filename)
        print(f"\nSuccess! Sales data has been exported to '{output_filename}'.")

#Additional Function
def load_saved_orders():
    all_orders = []
    current_order = {}
    file = open("saved_orders.txt", "r")
    for line in file:
        line = line.strip()
        if line == "New Order:":
            current_order = {}
        elif line.startswith("-"):
            if current_order:
                all_orders.append(current_order)
        elif "x" in line and "=" in line:
            item_part, rest = line.split("x")
            item = item_part.strip()
            quantity = int(rest.split("=")[0].strip())
            current_order[item] = quantity
    file.close()
    return all_orders
#Function 10
def generate_daily_report(orders, menu):
    report = {}
    for order in orders:
        for item, quantity in order.items():
            if item in menu:
                if item not in report:
                    report[item] = {
                        "quantity": quantity,
                        "revenue": quantity * menu[item]
                    }
                else:
                    report[item]["quantity"] += quantity
                    report[item]["revenue"] += quantity * menu[item]
    return report
menu = load_menu()
save_order()
all_orders = load_saved_orders()
report = generate_daily_report(all_orders, menu)
print("\nDaily Report:")
for item, data in report.items():
    print(f"{item} - Total Sold: {data['quantity']}, Revenue: {data['revenue']} EGP")


