# Importing tabulate to use for the view_all function
from tabulate import tabulate


# Setting up my class
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        """ Takes country, code, product, cost and quantity to create a Shoe object. """
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        """ Returns how much a shoe costs. """
        return self.cost

    def get_quantity(self):
        """ Returns the quantity of a shoe held in the inventory. """
        read_shoes_data()
        return self.quantity.strip("\n")

    def __str__(self):
        """ Returns a string representation of the data held about a shoe. """
        return f"""Country: {self.country}
Code: {self.code}
Product name: {self.product}
Cost: {self.cost}
Quantity: {self.quantity}"""


# Used to store a list of objects of shoes.
shoe_list = []


# Below are functions outside the class
def read_shoes_data():
    """Reads the inventory txt file and adds the data to a list"""
    try:
        with open("inventory.txt", "r") as ofile:
            for line in ofile:
                line = line.split(",")
                # Skipping the first line and any lines that aren't 5 entries
                # long, in case of user error or corrupted data
                if line[0] == "Country" or len(line) != 5:
                    continue
                else:
                    shoe_name = line[-3]
                    shoe_name = Shoe(line[0], line[1], line[2], line[3], line[4])
                    shoe_list.append(shoe_name)
        return shoe_list
    # Building in an exception in case the file is deleted or moved
    except FileNotFoundError:
        return f"'inventory.txt' was not found. Check that it has not been deleted or moved"


def capture_shoes():
    """ Allows the user to enter data about a shoe that is then saved to
    the shoe_list and written to  inventory.txt. """
    cap_country = input("Enter country: ")
    cap_code = input("Enter code: ")
    cap_product = input("Enter product name: ")
    cap_cost = input("Enter cost: ")
    cap_quantity = input("Enter quantity: ")
    captured_shoe = Shoe(cap_country, cap_code, cap_product, cap_cost, cap_quantity)
    shoe_list.append(captured_shoe)
    with open("inventory.txt", "a") as ofile:
        ofile.write(f"\n{captured_shoe.country},{captured_shoe.code},\
{captured_shoe.product},{captured_shoe.cost},{captured_shoe.quantity}")
    return shoe_list


def view_all():
    """ Displays a table of the shoe inventory """
    for shoe in shoe_list:
        table = ["Country", shoe.country], ["Code", shoe.code], ["Product", shoe.product], \
                ["Cost", shoe.cost], ["Quantity", shoe.quantity]
        print(tabulate(table))


def re_stock():
    """ Gives the user options linked to restocking """
    minimum = 100
    for i in range(len(shoe_list)):
        if int(shoe_list[i].quantity) < minimum:
            minimum = int(shoe_list[i].quantity)
    for i in range(len(shoe_list)):
        if int(shoe_list[i].quantity) == minimum:
            restock_choice = input(f"""There are only {minimum} in stock of the {shoe_list[i].product}.
Would you like to update the stock details? y/n: """).lower()
            if restock_choice == "y":
                new_quantity = int(input("What's the new stock level? "))
                for i in range(len(shoe_list)):
                    if int(shoe_list[i].quantity) == minimum:
                        shoe_list[i].quantity = f"{new_quantity}\n"
                    with open("inventory.txt", "w") as ofile:
                        for i in range(len(shoe_list)):
                            ofile.write(f"{shoe_list[i].country},{shoe_list[i].code},\
{shoe_list[i].product},{shoe_list[i].cost},{shoe_list[i].quantity}")
                print("Thank you! The stock level has been updated")
            elif restock_choice == "n":
                print("OK. Returning you to the main menu")
                menu()
            else:
                print("Invalid response")


def search_shoe():
    """ Allows the user to look up details about a shoe using its code """
    code_input = input("Enter code: ")
    for shoe in shoe_list:
        if shoe.code == code_input:
            print(shoe)


def value_per_item(code_choice):
    """Displays the value of a shoe"""
    shoe_value = 0
    for shoe in shoe_list:
        if shoe.code == code_choice:
            product_name = shoe.product
            shoe_value = int(shoe.quantity) * int(shoe.cost)
    print(f"The stock of {product_name} is worth R{shoe_value}")


def highest_qty():
    """ Displays the shoe with the highest stock in the inventory """
    maximum = 0
    for i in range(len(shoe_list)):
        if int(shoe_list[i].quantity) > maximum:
            maximum = int(shoe_list[i].quantity)
    for i in range(len(shoe_list)):
        if int(shoe_list[i].quantity) == maximum:
            print(f"You have {shoe_list[i].quantity.strip()} {shoe_list[i].product}s! Consider putting them on sale")
            menu()


def product_choices():
    """ Shows the user options about viewing details about the shoes """
    valid_codes = []
    for shoe in shoe_list:
        valid_codes.append(shoe.code)

    code_choice = input("Enter the product code: ")
    while code_choice not in valid_codes:
        print("Oops! Invalid code. Try again.")
        code_choice = input("Enter the product code: ")
    while True:
        detail_choice = input("Enter 'p' for price, 'q' for quantity,\
'v' to see the value of stock held or 'f' for full details:\n")
        for shoe in shoe_list:
            if shoe.code == code_choice:
                chosen_shoe = shoe
        if detail_choice == "p":
            print(f"The {chosen_shoe.product} costs R{Shoe.get_cost(chosen_shoe)}")
        elif detail_choice == "q":
            print(f"There are {Shoe.get_quantity(chosen_shoe)} in stock of the {chosen_shoe.product}")
        elif detail_choice == "f":
            print(chosen_shoe)
        elif detail_choice == "v":
            value_per_item(code_choice)
        code_again = input(f"Would you like to check something else about the {chosen_shoe.product}? y/n: ").lower()
        if code_again == "n":
            go_again()


def go_again():
    """ Asks the user if they want to check another code """
    again = input("Would you like to check another code? y/n: ")
    if again != "y" and again != "n":
        again = input("Oops! Invalid input. Would you like to check another code? y/n: ").lower()
    if again == "n":
        print("OK. Returning you to the main menu.")
        menu()
    elif again == "y":
        product_choices()


# Creating a menu for the user that uses all of the above functions
def menu():
    """ Presents a menu of options about the inventory to the user. """
    user_choice = input('''\nPlease select an option:

    a:  Add a new product to the inventory
    i:  View the inventory
    s:  Stock options
    d:  Display product details\n\n''').lower()

    if user_choice == "a":
        capture_shoes()
        print("The new shoe has been added to the inventory")
        menu()

    elif user_choice == "i":
        view_all()
        menu()

    elif user_choice == "s":
        while True:
            stock_choice = input('''To see the product with the lowest stock levels, enter 'l'. You can then restock.
If you're planning a sale, press 'h' to see the product with the highest stock:\n''').lower()
            if stock_choice == 'l':
                re_stock()
                break
            elif stock_choice == 'h':
                highest_qty()
                break
            else:
                print("Oops! Invalid input. Try again")

    elif user_choice == "d":
        product_choices()

    elif user_choice == "d":
        print("Goodbye!")
    else:
        print("Oops! Invalid selection. Try again!")
        menu()


print("Welcome to the Nike inventory!")

# Calling this first to make sure that the shoe list is up to date
read_shoes_data()

menu()
