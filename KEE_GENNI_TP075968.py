import datetime
import os
import re

ppe_path = "ppe.txt"
supp_path = "supplier.txt"
hosp_path = "hospital.txt"
dist_path = "distribution.txt"
receive_path = "receive_supply.txt"
user_info_path = 'user_info.txt'

# Main
def main():
    if os.path.exists(user_info_path):
        users = load_users(user_info_path)
        user_count = len(users)
    else:
        users = {}
        user_count = 0

    attempts = {}
    while True:
        user_input = str(input("Would you like to sign up or log in?\n1. Sign up\n2. Log in\n3. Quit Program\n"))
        if user_input == "1":
            user_count, sign_up_success = sign_up(users, user_count, user_info_path)
            if sign_up_success:
                home()
        elif user_input == "2":
            if login(users, user_info_path, attempts) == True:
                home()
        elif user_input == "3":
            print("Quitting program")
            return
        else:
            print("Please enter correct input")

# Sign Up
def sign_up(users, user_count, user_info_path):
    #Check if user count more than 4
    while True:
        if user_count >= 4:
            print("The maximum number of registered users has been reached.")
            return user_count, False #return exit whole function
        else:
            username = input("Please enter a username")
            if username in users:
                print("Username already exists. Please choose a different username.")
            else:
                password = input("Please enter your password")
                users[username] = password
                print(f"Your username is {username} \nYour password is {password}")
                print("Sign up successfully")

                user_count+=1
                content = f"{username}, {password}"
                append_file(user_info_path, content)

                print("You have logged in")
                print("Welcome to the home page")
                return user_count, True

# Log in
def load_users(user_info_path):
    users = {}
    try:
        user_content = readlines_file(user_info_path)
        for line in user_content:
            username, password = line.strip().split(', ')
            users[username] = password
    except FileNotFoundError:
        print(f"There are no users registered. Please sign up before logging in.")
    return users

def update_users_info(user_info_path, users):
    content = []
    for username, password in users.items():
        content.append(f"{username}, {password}\n")
    write_file(user_info_path, content)

def delete_user(user_info_path, username_to_delete):
    users = load_users(user_info_path)
    if username_to_delete in users:
        del users[username_to_delete]
        update_users_info(user_info_path, users)

def login(users, user_info_path, attempts, max_attempts=3):
    if not os.path.exists(user_info_path):
        print(f"There are no users registered. Please sign up before logging in.")
        return

    users = load_users(user_info_path)
    if not users:
        return

    while True:
        username = input("Please enter your username: ")

        # If username is not valid
        if username not in users:
            print("This username is not found. Please try again.")
            continue

        password = input("Please enter your password: ")

        # If attempts more than 3 times
        if username in attempts and attempts[username] >= max_attempts:
            print("Too many failed attempts. Access terminated.")
            delete_user(user_info_path, username)
            return False

        # If login successful
        if users[username] == password:
            print("Login successful!")
            return True
        else:
            if username in attempts:
                attempts[username] += 1
            else:
                attempts[username] = 1

            if attempts[username] >= max_attempts:
                print("You have been banned from too many attempts.")
                delete_user(user_info_path, username)
                return False
            else:
                print("Login failed. Please try again.")


# RWA File
def read_file(file_path):
    with open (file_path, 'r') as file:
        return file.read()

def readlines_file(file_path):
    with open (file_path, 'r') as file:
        return file.readlines()

def write_file(file_path, content):
    with open (file_path, 'w') as file:
        file.writelines(content)

def append_file(file_path, content):
    with open (file_path, 'a') as file:
        file.writelines(content + '\n')


# ppe_file
def create_ppe_file(ppe_path, supp_path):

    # Check if the file already exists
    if os.path.exists(ppe_path):
        return

    else:
        print(f"{ppe_path} does not exist. Creating a new file.")

        # Open the file in write mode
        print("Example: HC, Head Cover, 100, S01, January 27 2024 \n(The user input should be exactly the same as the expected format)")

        while True:

            # Prompt user to enter text or 'done' to finish
            # Expected input
            # HC, Head Cover, 100, S01, January 27 2024

            user_input = input("Enter text to write into this file or 'done' to finish:")

            if user_input.lower() == 'done':
                break

            try:
                line = user_input.strip().split(', ')
                print(line)

                if len(line) != 5:
                    print("Your input does not contain the expected number of elements.")
                    continue

                # If the user input matches the format
                ppe_code = re.match(r'^[A-Z]{2}$', line[0]) is not None
                ppe_name = re.match(r'^[A-Za-z ]+$', line[1]) is not None
                ppe_quantity = line[2].isdigit() and int(line[2]) == 100

                supp_content = read_file(supp_path)
                ppe_supplier = line[3] in supp_content

                date_format = "%B %d %Y"
                ppe_date = False

                try:
                    # If the text is in the specified (correct) date format
                    parsed_date = datetime.strptime(line[4], date_format)
                    ppe_date = True

                except ValueError:
                    # If the text is not in the specified date format
                    ppe_date = False

                if ppe_code and ppe_name and ppe_quantity and ppe_supplier and ppe_date:
                    write_file(ppe_path, user_input)
                    print("Data written to file.")

                else:
                    print("Input data is not valid based on the criteria.")
                    if not ppe_code:
                        print("Invalid PPE code.")
                    if not ppe_name:
                        print("Invalid PPE name.")
                    if not ppe_quantity:
                        print("Invalid PPE quantity.")
                    if not ppe_supplier:
                        print("Supplier not found.")
                    if not ppe_date:
                        print("Invalid date format.")

            except Exception as e:
                print(f"An error occurred: {e}")

    print(f"{ppe_path} has been created with your input")

# supplier_file
def supplier_file(supp_path):
    # Check if the supplier file exists
    if not os.path.exists(supp_path):
        print(f"{supp_path} does not exist. Creating a new file.")

    else:
        # print("File exists")
        return

    supply_count = 0  # Initialize the supply count

    print("Example: S01, Supplier Name, 1 Jalan XXX Taman XXX, 012-3456789 \n(The user input should be exactly the same as the expected format)")
    print("Noted: The address should not include any ',' ")

    while True:
        # Prompt user for supplier details
        # Expected input
        # S01, Supplier Name, 8 Jalan XXX , 012-3456789
        user_input = input("Please enter supplier details or type 'done' to finish: ")

            # Check if user is done or supply count is 4 or more
        if user_input.lower() == 'done' or supply_count >= 4:
            break

        try:
            line = user_input.strip().split(', ')
            print(line)

            if len(line) != 4:
                print("Your input does not contain the expected number of elements.")
                continue

            supp_code = re.match(r'^S\d{2}$', line[0]) is not None
            supp_name = re.match(r'^[A-Z][A-Za-z ]+$', line[1]) is not None
            supp_address = re.match(r'^[A-Za-z0-9/ ]*$', line[2]) is not None
            supp_contact = re.match(r'^\d{3}-\d{7,8}$', line[3]) is not None

            if supp_code and supp_name and supp_address and supp_contact:
                append_file(supp_path, user_input)
                print("Data written to file.")

            else:
                print("Input data is not valid based on the criteria.")
                if not supp_code:
                    print("Invalid supplier code.")
                if not supp_name:
                    print("Invalid supplier name.")
                if not supp_address:
                    print("Invalid supplier address.")
                if not supp_contact:
                    print("Invalid supplier contact.")

            supply_count += 1
            if supply_count >= 4:
                print("The supplier count has reached the maximum.")
                break

        except Exception as e:
            print(f"An error occurred: {e}")

    print(f"{supp_path} has been created with your input.")

# hospital_file
def hospital_file(hosp_path):

    if not os.path.exists(hosp_path):

        while True:
            user_input = str(input("Would you like to create hospital.txt file?\n '1' for Yes\n '2' for No"))

            if user_input == "1":
                hosp_count = 0
                print("Example: H01, Hospital XXX")

                while True:
                    #Expected input
                    #H01, Hospital Name XXX
                    hosp_details = input("Please enter hospital details or type 'done' to finish: ")

                    if hosp_details.lower() == "done" or hosp_count >= 4:
                        break

                    try:
                        line = hosp_details.strip().split(', ')
                        print(line)

                        if len(line) != 2:
                            print("Your input does not contain the expected number of elements.")
                            continue

                        hosp_code = re.match(r'^H\d{2}$', line[0]) is not None
                        hosp_name = re.match(r'^[A-Z][A-Za-z ]+$', line[1]) is not None

                        if hosp_code and hosp_name:
                            append_file(hosp_path, hosp_details)
                            hosp_count += 1
                            print("Data written to file.")

                        else:
                            print("Input data is not valid based on the criteria.")
                            if not hosp_code:
                                print("Invalid hospital code.")
                            if not hosp_name:
                                print("Invalid hospital name")

                    except Exception as e:
                        print(f"An error occurred: {e}")

                    if hosp_count >= 4:
                        print("The hospital count has reached the maximum number.")
                        break

                print(f"{hosp_path} has been created with your input.")
                break #Break after user done creating and entering the file

            elif user_input == '2':
                break

            else:
                print("Please enter the correct input")

    else:
        print("hospital.txt already exists. Returning to homepage")

#distribution_file
def distribution_file(dist_path, ppe_path, hosp_path):
    while True:
        item_code = input("What item do you want to distribute? (please type in Item Code): ").upper()

        lines = readlines_file(ppe_path)

        # Check if user input is a valid item_code
        item_exists = False
        for line in lines:
            item = line.strip().split(", ")
            if item[0] == item_code:
                item_exists = True
                break

        if not item_exists:
            print("This item does not exist. Please enter a valid item code")
            continue

        while True:
            amount = input("Please input the amount of items to be distributed: ")

            try:
                amount = int(amount)
                updated_lines = []
                quantity_sufficient = True

                for line in lines:
                    item = line.strip().split(", ")

                    if item[0] == item_code:             # HC, Head Cover, 100, S01, DATE
                        current_quantity = int(item[2])

                        # Check if item quantity is sufficient
                        if amount > current_quantity:
                            print("There is not enough of this item for distribution.")
                            quantity_sufficient = False
                            break # Exit for loop

                        while True:
                            hosp_code = input("Which hospital do you want to distribute to? (please type in Hospital Code): ").upper()
                            hosp_content = read_file(hosp_path)

                            if hosp_code not in hosp_content:
                                print("This hospital does not exist. Please enter a valid code.")
                            else:
                                new_quantity = current_quantity - amount
                                item[2] = str(new_quantity)
                                current_date = datetime.datetime.now()
                                date_formalized = current_date.strftime("%B %d %Y")
                                content = f"{item_code}, {amount}, {hosp_code}, {date_formalized}"
                                append_file(dist_path, content)

                                print("Your distribution has been recorded successfully.")
                                break  # Exit hosp_code loop

                        updated_lines.append(", ".join(item) + "\n")
                    else:
                        updated_lines.append(line)

                if quantity_sufficient:
                    write_file(ppe_path, updated_lines)
                    break  # Exit item_code loop

            except ValueError:
                print("This is not a valid number.")

        # Ask if the user wants to continue
        while True:
            choice = input("Do you want to continue distributing items? (yes/no): ").lower()
            if choice in ('yes', 'no'):
                break # Exit choice and continue with distribution
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")

        if choice == 'no':
            break # Exit distribution


# distribution_hospital
def distribution_hospital():
    hospitals = {}
    distribution = {}

    hosp_content = readlines_file(hosp_path)

    for line in hosp_content:
        item = line.strip().split(', ')
        if len(item) == 2:
            hosp_code, hosp_name = item
            hospitals[hosp_code] = hosp_name


    dist_content = readlines_file(dist_path)

    for line in dist_content:
        item = line.strip().split(', ')
        if len(item) >= 3:
            item_code = item[0]
            quantity = int(item[1])
            hosp_code = item[2]

            # Initialize dictionary for the hospital if it doesn't exist
            if hosp_code not in distribution:
                distribution[hosp_code] = {}

            # Sum up quantity for the same product and hospital
            if item_code in distribution[hosp_code]:
                distribution[hosp_code][item_code] += quantity
            else:
                distribution[hosp_code][item_code] = quantity

    # Print the distribution summary
    for hosp_code, items in distribution.items():
        for item_code, total_quantity in items.items():
            hosp_name = hospitals.get(hosp_code, "Unknown Hospital")
            print(f"{hosp_name} ({hosp_code}) has been distributed {total_quantity} of {item_code}")

# update_inventory
def add_invent(ppe_path, receive_path):
    while True:
        item_code = input("What item do you want to add? (Please enter item code): ")
        ppe_content = readlines_file(ppe_path)

        # Check if item exists in PPE (is it a VALID item?)
        if not any(item_code in line for line in ppe_content):
            print("This item does not exist. Please enter a valid code")

        else:
            try:
                amount = int(input("How many items to add?: "))
                if amount <= 0:
                    print("Amount must be a positive integer greater than zero.")
                    continue

            except ValueError:
                print("This is not a valid number")

            else:
                update_cont = []

                for line in ppe_content:
                    parts = line.strip().split(', ')

                    # HC, Head Cover, 100, S01, January 27 2024
                    if len(parts) >= 5 and parts[0] == item_code:
                        curr_quantity = int(parts[2])
                        new_quantity = curr_quantity + amount
                        current_date = datetime.datetime.now()
                        date_formalized = current_date.strftime("%B %d %Y")

                        parts[2] = str(new_quantity)
                        supp_code = parts[3]
                        parts[4] = date_formalized
                        updated_line = ', '.join(parts) + '\n'
                        update_cont.append(updated_line)

                    else:
                        update_cont.append(line)

                write_file(ppe_path, update_cont)
                receive_content = f"{item_code}, {amount}, {supp_code}, {date_formalized}"
                append_file(receive_path, receive_content)

                print("Inventory updated successfully.")
                return # Quit function after successful update

# distribute_inventory
def distribute_invent(hosp_path, dist_path, ppe_path):
    # Check if paths exist
    if os.path.exists(hosp_path):
            distribution_file(dist_path, ppe_path, hosp_path)

    else:
        print("Please create hospital file before distributing inventory")
        # Create hosp file if not exists
        hospital_file(hosp_path)

# update_supplier
def update_supp_details(supp_path):
    supp_content = readlines_file(supp_path)
    while True:
        supp_code = input("Please enter the supplier code: ")

        #Check if is a valid supplier code
        if not any(supp_code in line for line in supp_content):
            print("This supplier code does not exist. Please enter a valid code")
            continue

        while True:
            details = input("Which detail do you want to edit? [Name, Address, Contact]: ").lower()
            updated_content = []

            if details == "name":
                while True:
                    new_name = input("Please enter the new name: ")

                    if re.match(r'^[A-Z][A-Za-z ]+$', new_name):
                        # Update supplier name
                        for line in supp_content:
                            if supp_code in line:
                                parts = line.strip().split(', ')
                                parts[1] = new_name
                                updated_line = ', '.join(parts) + '\n'
                                updated_content.append(updated_line)

                            else:
                                updated_content.append(line)

                        write_file(supp_path, updated_content)
                        print("Supplier name updated successfully.")
                        return

                    else:
                        print("Invalid name format. Please enter alphabetical characters only starting with uppercase.")
                        print("Example: Supplier Name XXX")


            elif details == "address":
                while True:
                    new_address = input("Please enter the new address: ")

                    if re.match(r'^[A-Za-z0-9/ ]*$', new_address):
                        # Update supplier address
                        for line in supp_content:
                            if supp_code in line:
                                parts = line.strip().split(', ')
                                parts[2] = new_address
                                updated_line = ', '.join(parts) + '\n'
                                updated_content.append(updated_line)

                            else:
                                updated_content.append(line)

                        write_file(supp_path, updated_content)
                        print("Supplier address updated successfully.")
                        return

                    else:
                        print("Invalid address format. Please enter alphanumerical characters '/' or spaces only.")
                        print("Example: 1 Jalan 1/2 Taman XXX")


            elif details == "contact":
                while True:
                    new_contact = input("Please enter the new contact: ")

                    if re.match(r'^\d{3}-\d{7,8}$', new_contact):
                        # Update supplier address
                        for line in supp_content:
                            if supp_code in line:
                                parts = line.strip().split(', ')
                                parts[3] = new_contact
                                updated_line = ', '.join(parts) + '\n'
                                updated_content.append(updated_line)

                            else:
                                updated_content.append(line)

                        write_file(supp_path, updated_content)
                        print("Supplier address updated successfully.")
                        return

                    else:
                        print("Invalid name format. Please enter 3 digits, followed by a '-', and end with either 7 or 8 digits.")
                        print("Example: 012-3456789")

            else:
                print("Please enter the correct details.")

# update_hospital
def update_hosp_details(hosp_path):
    if os.path.exists(hosp_path):
        while True:
            hosp_code = input("Please enter the hospital code: ")
            hosp_content = readlines_file(hosp_path)

            # Check if hospital code is valid
            if not any(hosp_code in line for line in hosp_content):
                print("This hospital code does not exist. Please enter a valid hospital code.")
                continue

            else:
                while True:
                    details = input("Which detail do you want to edit? [Name]").lower()
                    if details == 'name':
                        new_name = input("Please enter the new name: ")

                        if re.match(r'^[A-Z][A-Za-z ]+$', new_name):
                            updated_content = []

                            for line in hosp_content:
                                # Update new hospital name
                                if hosp_code in line:
                                    parts = line.strip().split(', ')
                                    parts[1] = new_name
                                    updated_line = ', '.join(parts) + '\n'
                                    updated_content.append(updated_line)
                                else:
                                    updated_content.append(line)

                            write_file(hosp_path, updated_content)
                            print("Hospital name updated successfully.")
                            return

                        else:
                            print("Invalid name format. Please enter alphabetical characters only starting with an uppercase letter.")
                            continue

                    else:
                        print("Please enter a valid detail [Name].")
                        continue
    else:
        print("Please create hospital file before updating it.")
        hospital_file(hosp_path)
        return

# track_items
def track_items():
    ppe_content = readlines_file(ppe_path)
    ppe_content = [line.strip().split(', ') for line in ppe_content]
    while True:
        track = input("Do you want to track available quantity of all items or track all items which has less than 25 stock? [1 or 2]")

        # Print item sorted by item code in asc
        if track == '1':

            # Sort ppe_content by the first column (code)
            sorted_ppe = sorted(ppe_content, key = lambda x: x[0])

            # Print Item Code and Quantity
            for line in sorted_ppe:
                print(f"Item Code: {line[0]}; Quantity: {line[2]}")

            break

        # Print item that less than 25
        elif track == '2':

            # Sort ppe_content by the third column (quantity with ASC)
            sorted_ppe = sorted(ppe_content, key = lambda x: x[2])
            items_below_25 = False

            # Print Item and quantity(where less than 25)
            for line in sorted_ppe:
                if int(line[2]) < 25:
                    items_below_25 = True
                    break

            if items_below_25:
                print("Item belows 25 boxes:")
                for line in sorted_ppe:
                    if int(line[2]) < 25:
                        print(f"Item Code: {line[0]}; Quantity: {line[2]}")

            if not items_below_25:
                print(f"There are no items below 25 boxes.")

            break

        else:
            print("The input is invalid. Please try again.")

# search_distribution
def search_distribution(ppe_path):
    while True:
        item_code = input("Please enter the Item Code")
        ppe_content = readlines_file(ppe_path)

        # Check if user input is valid item code
        if not any (item_code in line for line in ppe_content):
            print('This input is invalid. Please try again.')

        else:
            dist_content = readlines_file(dist_path)

            # Check if user input has been distributed
            if not any (item_code in line for line in dist_content):
                print(f"{item_code} does not distribute to any hospital yet.")
                return

            else:
                hosp_quantity = {} # Dict used to sum up the quantity for the same hosp/item
                for line in dist_content:
                    parts = line.strip().split(', ')
                    if parts[0] == item_code:
                        quantity = int(parts[1])
                        hosp_code = parts[2]

                        # Sum up quantity for the same hosp/item
                        if (item_code, hosp_code) in hosp_quantity:
                            hosp_quantity[(item_code, hosp_code)] += quantity
                        else:
                            hosp_quantity[(item_code, hosp_code)] = quantity

                for (item_code, hosp_code), quantity in hosp_quantity.items():
                    print(f"{item_code} has been distributed {quantity} to {hosp_code}")

                return

# suppliers_with_PPE
def supp_with_ppe(supp_path, ppe_path):
    suppliers = {}
    supp_content = readlines_file(supp_path)

    for line in supp_content:
        parts = line.strip().split(', ')
        suppliers[parts[0]] = parts[1]

    # print(suppliers)
    items = {}
    ppe_content = readlines_file(ppe_path)

    for line in ppe_content:
        parts = line.strip().split(', ')
        item_code = parts[0]
        item_name = parts[1]
        quantity = parts[2]
        supp_code = parts[3]

        if supp_code in suppliers: # Check if is valid supp_code
            if supp_code not in items: # Check whether the supp has alr supplied items b4
                items[supp_code] = []
            items[supp_code].append((item_code, item_name, quantity))

    for supp_code, item_list in items.items():
        print(f"Supplier: {suppliers[supp_code]}")
        for item in item_list:
            print(f"Item Code: {item[0]}, Item Name: {item[1]}, Quantity: {item[2]}")
        print(" ")

# overall_transactions
def overall_transaction(dist_path, receive_path):
    valid_month = {
                    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'
                    }
    while True:
        month = input("Please input the month which you would like to retrieve data from: [January, February...]").capitalize()

        # If month not a valid month
        if month not in valid_month:
            print("Invalid month. Please enter a valid month name.")
            continue

        dist_content = readlines_file(dist_path)

        # Transaction report for distribution
        transactions_found = False
        hosp_transaction = {}

        for line in dist_content:
            # If month found
            if month in line:
                transactions_found = True
                parts = line.strip().split(', ')
                hosp_code = parts[2]
                if hosp_code not in hosp_transaction:
                    hosp_transaction[hosp_code] = []
                hosp_transaction[hosp_code].append(line.strip())

        if transactions_found:
            print(f"Transaction report for items distributed in {month}:")
            for hosp_code, transactions in hosp_transaction.items():
                print(f"\nTransactions for hospital {hosp_code}:")
                for transaction in transactions:
                    print(transaction)
        else:
            print(f"There are no transactions for items distributed in {month}.")

        print(" ")

        receive_content = readlines_file(receive_path)

        # Transaction report for supply received
        receive_found = False
        receive = {}

        for line in receive_content:
            # If month found
            if month in line:
                receive_found = True
                parts = line.strip().split(', ')
                supp_code = parts[2]
                if supp_code not in receive:
                    receive[supp_code] = []
                receive[supp_code].append(line.strip())

        if receive_found:
            print(f"Transaction report for items received from suppliers in {month}:")
            for supp_code, transactions in receive.items():
                print(f"\nTransactions for items received from {supp_code}:")
                for transaction in transactions:
                    print(transaction)
        else:
            print(f"There are no transactions for items received in {month}.")

        return


# Home Code
def home():
    print("Welcome to the menu!")

    # Call functions
    supplier_file(supp_path)
    create_ppe_file(ppe_path, supp_path)

    while True:

        print("""What would you like to do?
        '1' to Create Hospital File
        '2' to Update Inventory
        '3' to Update Supplier Details
        '4' to Update Hospital Details
        '5' to Track Inventory Items
        '6' to Search Distribution List
        '7' to Print Report
        '8' to Log Out""")

        home_input = input("What would you like to do?")

        # Create hosp file
        if home_input == "1":
            hospital_file(hosp_path)
            # break

        # Update inventory
        elif home_input == "2":
            while True:
                # Add or Distribute
                invent_input = input("Would you like to add inventory or distribute inventory? [1 to Add Inventory, 2 to Distribute Inventory]\n> ")

                # Add inventory
                if invent_input == "1":
                    add_invent(ppe_path, receive_path)
                    break

                # Distribute inventory
                elif invent_input == "2":
                    distribute_invent(hosp_path, dist_path, ppe_path)
                    break

                else:
                    print("This is not a valid answer. Please try again")

        # Update supplier details
        elif home_input == "3":
            update_supp_details(supp_path)

        # Update Hospital Details
        elif home_input == "4":
            update_hosp_details(hosp_path)

        # Track Items
        elif home_input == "5":
            track_items()

        # Search Distribution List
        elif home_input == "6":
            search_distribution(ppe_path)

        elif home_input == "7":

            while True:
                print("""What would you like to do?
        '1' to Print the List of Suppliers with their PPE equipments supplied
        '2' to Print the List of Hospitals with quantity of distribution items
        '3' to Print the Overall Transaction Report for a selected month
        '4' to Quit Print Report\n""")

                user_input = input("Would you like to print the list of suppliers with their PPE equipments supplied or the list of hospitals with quantity of distribution items or overall transaction report for a selected month?")

                # Print List of Suppliers with PPE supplied
                if user_input == '1':
                   supp_with_ppe(supp_path, ppe_path)
                   break

                # Print List of Hospitals with quantity of distribution items
                elif user_input == '2':
                    distribution_hospital()
                    break

                # Print Overall Transaction report
                elif user_input == '3':
                    overall_transaction(dist_path, receive_path)
                    break

                elif user_input == '4':
                    break

                else:
                    print("Please enter correct input.")

        # Log Out
        elif home_input == "8":
            print("Logging out...")
            break

        else:
            print("Invalid input. Please try again.")
            continue

if __name__ == '__main__':
    main()