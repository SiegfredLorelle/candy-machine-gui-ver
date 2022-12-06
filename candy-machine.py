import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
# from tkinter import ttk

def main():
    candy_machine = Candy_Machine()

    """ Optional - uncomment then edit default values in registers and dispensers """
    # candy_machine.cash_register.cash_register(cash_in=10_000)
    # candy_machine.candy_dispenser.dispenser(set_cost=25, set_no_of_items=20)
    # candy_machine.chip_dispenser.dispenser(set_cost=25, set_no_of_items=20)
    # candy_machine.gum_dispenser.dispenser(set_cost=25, set_no_of_items=20)
    # candy_machine.cookie_dispenser.dispenser(set_cost=25, set_no_of_items=20)

    app = App(candy_machine)
    # app.show_frame(0)
    app.mainloop()





class App(tk.Tk):
    def __init__(self, candy_machine):
        super().__init__()

        self.candy_machine = candy_machine

        self.title('My Candy Machine')
        self.geometry('1080x720')
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        container = tk.Frame(self, bg="#FFCAC8")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}
        self.Selection_Menu = Selection_Menu
        self.Admin_Menu = Admin_Menu
        self.Buy_Page = Buy_Page

        for F in {Selection_Menu, Admin_Menu, Buy_Page}:
            frame = F(self, container)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(Selection_Menu)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    # Reprompt when closing
    def on_closing(self):
        if messagebox.askyesno(title="Exit?", message="Do you really want to close 'My Candy Machine'?"):
            self.destroy()

    

class Selection_Menu(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container, bg="#FFCAC8")

        for number in range(7):
            self.grid_rowconfigure(number, weight=1)
        for number in range(2):
            self.grid_columnconfigure(number, weight=1)


        title = tk.Label(self, text="My Candy Machine", font="Times 25 bold", fg="black", bg="#C0EEE4")
        title.grid(row=0, column=0, columnspan=2, sticky="nesw")

        intstructions = tk.Label(self, text="Press the item to purchase!", font="Times 18 bold", fg="black", bg="#FFCAC8")
        intstructions.grid(row=1, column=0, columnspan=2, sticky="nesw")

        candy = tk.Button(self, text="Candy", font="Times 15", bg="#FF9E9E", command=lambda: parent.show_frame(parent.Buy_Page))
        candy.grid(row=2, column=0, columnspan=2, sticky="nesw")

        chip = tk.Button(self, text="Chip", font="Times 15", bg="#FF9E9E", command=lambda: parent.show_frame(parent.Buy_Page))
        chip.grid(row=3, column=0, columnspan=2, sticky="nesw")

        gum = tk.Button(self, text="Gum", font="Times 15", bg="#FF9E9E", command=lambda: parent.show_frame(parent.Buy_Page))
        gum.grid(row=4, column=0, columnspan=2, sticky="nesw")

        cookie = tk.Button(self, text="Cookie", font="Times 15", bg="#FF9E9E", command=lambda: parent.show_frame(parent.Buy_Page))
        cookie.grid(row=5, column=0, columnspan=2, sticky="nesw")

        exit = tk.Button(self, text="Exit", font="Times 15", bg="#FF9E9E", command=parent.on_closing)
        exit.grid(row=6, column=0, sticky="nesw", ipadx=15)

        admin = tk.Button(self, text="Admin", font="Times 15", bg="#FF9E9E", command=lambda: parent.show_frame(parent.Admin_Menu))
        admin.grid(row=6, column=1, sticky="nesw")



    

class Admin_Menu(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container, bg="black")

        label = tk.Label(self, text="Admin Menu", font=("Times", 30))


class Buy_Page(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container, bg="red")

        label = tk.Label(self, text="Admin Menu", font=("Times", 30))
        label.pack()






























class Candy_Machine:

    def __init__(self):
        """ Initalize the components of candy machine """
        self.cash_register = Cash_Register()
        self.candy_dispenser = Dispenser()
        self.chip_dispenser = Dispenser()
        self.gum_dispenser = Dispenser()
        self.cookie_dispenser = Dispenser()
        
        # Key mapping in selection menu
        self.item_key = {"1": {"item": "candy", "dispenser": self.candy_dispenser},
                         "2": {"item": "chip", "dispenser": self.chip_dispenser},
                         "3": {"item": "gum", "dispenser": self.gum_dispenser},
                         "4": {"item": "cookie", "dispenser": self.cookie_dispenser},
                         "A": "admin",
                         "Q": "exit"}

        # Key mapping in admin menu
        self.admin_key = {"1": {"item": "candy", "dispenser": self.candy_dispenser},
                          "2": {"item": "chip", "dispenser": self.chip_dispenser},
                          "3": {"item": "gum", "dispenser": self.gum_dispenser},
                          "4": {"item": "cookie", "dispenser": self.cookie_dispenser},
                          "V": "view_balance",
                          "S": "set_balance",
                          "Q": "back"}

    # Getter
    @property
    def choice(self):
        return self._choice

    # Setter
    @choice.setter
    def choice(self, choice):
        if not choice or choice not in self.item_key:
            raise ValueError("Choice is not in item key")
        else:
            self._choice = self.item_key[choice]

    # Getter
    @property
    def admin_choice(self):
        return self._admin_choice

    # Setter
    @admin_choice.setter
    def admin_choice(self, admin_choice):
        if not admin_choice or admin_choice not in self.admin_key:
            raise ValueError("Choice is not in admin key")
        else:
            self._admin_choice = self.admin_key[admin_choice]

    def program(self):
        """ Main Program """
        turn_off_msg = "\nMy Candy Machine' is turning off"
        error_msg = "\n\n❌ Please select a proper item!"

        print("\n⭐⭐⭐⭐⭐ Welcome to ⭐⭐⭐⭐\n🔥🔥🔥 My Candy Machine 🔥🔥🔥")

        # Shows the selection of items being sold
        while True:
            try:
                self.show_selection()
                if self.choice:
                    break

            except (ValueError, IndexError):
                print(error_msg)
                
        # Turn off candy machine if customer choose to
        if self.choice == "exit":
            # sys.exit(turn_off_msg)
            ...



        # Show menu intented for admin/owners
        elif self.choice == "admin":
            while True:
                try:
                    self.show_admin_menu()
                    if self.admin_choice:
                        break
                except (ValueError, IndexError):
                    print(error_msg)
            
            # Go back to selection menu if admin chooses to
            if self.admin_choice == "back":
                return self.program()

            # Let the admin view the current balance in the candy machine
            elif self.admin_choice == "view_balance":
                print(f"\nCurrent balance in the candy machine: ${self.cash_register.current_balance():,.2f}")
                while True:
                    # Add a buffer to let admin read the current balance
                    if not input("\nPress enter to proceed:  "):
                        return self.program()

            # Let admin change the current balance in the candy machine
            elif self.admin_choice == "set_balance":
                error_msg = "❌ Cash in candy machine must be a positive integer (Q - cancel)"
                while True:
                    try:
                        cash_in = input("\nHow much cash should the candy machine have:  ")

                        # Cancel if admin chooses to
                        if cash_in[0].upper() == "Q":
                            print("\nCash on candy machine wasn't changed.")
                            # Add a buffer to let admin read the msg
                            while True:
                                if not input("\nPress enter to proceed:  "):
                                    return self.program()
                        
                        # Stop asking if cash in the machine is valid
                        cash_in = int(cash_in)
                        if cash_in > 0:
                            break

                    # Inform admin of the error
                        else:
                            print(error_msg)
                    except (IndexError, TypeError, ValueError):
                        print(error_msg)

                # Set the new cash in register
                print(f"\n✅ Cash on the candy machine is set to ${cash_in:,.2f}")
                self.cash_register.cash_register(cash_in)
            
            # Admin chose to set values for items
            else:
                error_msg = f"❌ Price and stock of {self.admin_choice['item']} must be a positive integer (Q - cancel)"
                while True:
                    try:
                        # Ask for price of the item
                        set_cost = input(f"\nHow much should a {self.admin_choice['item']} be:  ")

                        # Cancel if admin chooses to
                        if set_cost[0].upper() == "Q":
                            print(f"\nPrice and stock of {self.admin_choice['item']} wasn't changed.")
                            # Add a buffer to let admin read the purchase msg
                            while True:
                                if not input("\nPress enter to proceed:  "):
                                    return self.program()
                        # if not Q try to convert to int
                        set_cost = int(set_cost)

                        # Asks for the number of stock of the item
                        set_no_of_items = input(f"How many stock of {self.admin_choice['item']} should be available:  ")

                        # Cancel if admin chooses to
                        if set_no_of_items[0].upper() == "Q":
                            print(f"\nPrice and stock of {self.admin_choice['item']} wasn't changed.")
                            # Add a buffer to let admin read the msg
                            while True:
                                if not input("\nPress enter to proceed:  "):
                                    return self.program()
                        # if not Q try to convert to int
                        set_no_of_items = int(set_no_of_items)

                        # Stop asking if both values are valid
                        if set_cost > 0 and set_no_of_items > 0:
                            break

                    # Inform admin of the error
                        else:
                            print(error_msg)
                    except (IndexError, TypeError, ValueError):
                        print(error_msg)

                # Set the new cost and stock of an item
                print(f"\n✅ A {self.admin_choice['item']} now cost ${set_cost:,.2f} and there are {set_no_of_items} stocks available")
                self.admin_choice["dispenser"].dispenser(set_cost, set_no_of_items)


        # If user chose an item to sell in selection menu (not admin menu)
        else:
            self.sell_product()

        # Add a buffer to let customer read the purchase succesful msg
        while True:
            if not input("\nPress enter to proceed:  "):
                return self.program()


    def sell_product(self):
        """ Sell the item selected by the customer """
        # Ensure that the chosen item is not out of stock
        if self.choice["dispenser"].get_count() <= 0:
            print(f"\nSorry, {self.choice['item']} is out of stock")
        
        # Add a buffer to let customer read the out of stock msg
            while True:
                if not input("\nPress enter to proceed:  "):
                    return self.program()

        # Get deposit from the customer until deposit is enough to pay the cost
        error_msg = "❌ Must deposit using positive integers. (Q - cancel purchase)"
        deposit = 0
        while deposit < self.choice['dispenser'].get_product_cost():
            try:
                new_deposit = input(f"\nPlease insert ${self.choice['dispenser'].get_product_cost() - deposit} to buy a {self.choice['item']}:  ")

                # Cancel the purchase if customer choose to
                if new_deposit[0].upper() == "Q":
                    print(f"\nCanceling your purchase for {self.choice['item']}")

                    # Return the deposited money by the customer
                    if deposit != 0:
                        print(f"Here is the ${deposit:,.2f} you inserted")
                    return self.program()
                
                # Add the new deposit to total deposit
                new_deposit = int(new_deposit)
                if new_deposit > 0:
                    deposit += new_deposit

            # Inform customer if their deposit is invalid
                else:
                    print(error_msg)
            except (ValueError, IndexError):
                print(error_msg)
        
        # Give the item if deposit is enough
        self.choice["dispenser"].makeSale()
        print(f"\n✅ Successfully purchased a {self.choice['item']}! Here is your {self.choice['item']}! Enjoy!")

        # Register takes in the payment (not total deposit, just the price of item)
        self.cash_register.accept_amount(self.choice['dispenser'].get_product_cost())

        # if there is change, return it
        if  deposit != self.choice['dispenser'].get_product_cost():
            print(f"Here also is your change of ${deposit - self.choice['dispenser'].get_product_cost():,.2f}")


    def show_selection(self):
        """ displays the main menu, allow users to select an item to buy """
        print("\nSelect an item to purchase by entering its corresponding value")
        print("1 - Candy \n2 - Chip \n3 - Gum \n4 - Cookie \n\nA - Admin Menu \nQ - Exit")
        self.choice = input("\nYour choice:  ")[0].upper() 

    def show_admin_menu(self):
        """ Allows owner to view and set balance in register, and set price and number of items """
        print("\nAdmin Settings: Enter corresponding value")
        print("1 - Set Candy \n2 - Set Chips \n3 - Set Gum \n4 - Set Cookies\n\nV - View Balance \nS - Set Balance \nQ - Back")
        self.admin_choice = input("\nYour choice:  ")[0].upper() 


class Cash_Register():
    """ component of Candy Machine, handles money """

    def __init__(self, cash_on_hand=500):
        self.cash_on_hand = cash_on_hand

    # Getter
    @property
    def cash_on_hand(self):
        return self._cash_on_hand

    # Setter
    @cash_on_hand.setter
    def cash_on_hand(self, cash_on_hand):
        if isinstance(cash_on_hand, int):
            if cash_on_hand < 0:
                self._cash_on_hand = 500
            else:
                self._cash_on_hand = cash_on_hand
        else:
            raise TypeError("Cash on Hand must be an integer")

    def __str__(self):
        return f"Cash on hand is ${self.cash_on_hand:,.2f}"

    def cash_register(self, cash_in=500):
        """ Let candy machine modify cash on hand """
        self.cash_on_hand = cash_in

    def current_balance(self):
        """ Shows the current amount in the cash register """
        return self.cash_on_hand

    def accept_amount(self, amount_in):
        """ Accepts the amount entered by the customer """
        if isinstance(amount_in, int) and amount_in > 0:
            self.cash_on_hand += amount_in
        
        else:
            raise TypeError("Amount In must be non negative integer")


class Dispenser:
    """ Component of Candy Machine, handles product """
    def __init__(self, cost=50, number_of_items=50):
        self.cost = cost
        self.number_of_items = number_of_items

    # Getter
    @property
    def cost(self):
        return self._cost

    # Setter
    @cost.setter
    def cost(self, cost):
        if isinstance(cost, int):
            if cost < 0:
                self._cost = 50
            else:
                self._cost = cost 
        else:
            raise TypeError("Cost must be an integer")

    # Getter
    @property
    def number_of_items(self):
        return self._number_of_items

    # Setter
    @number_of_items.setter
    def number_of_items(self, number_of_items):
        if isinstance(number_of_items, int):
            if number_of_items < 0:
                self._number_of_items = 50 
            else:
                self._number_of_items = number_of_items 
        else:
            raise TypeError("Number of Items must be an integer")

    def __str__(self):
        return f"Cost is ${self.cost:,.2f} and Number of Items is {self.number_of_items}"

    def dispenser(self, set_cost=50, set_no_of_items=50):
        """ Let candy machine modify number of items and cost of item """
        self.cost = set_cost
        self.number_of_items = set_no_of_items

    def get_count(self):
        """ returns the number of items of a particular product """
        return self.number_of_items

    def get_product_cost(self):
        """ returns the cost of a product """
        return self.cost

    def makeSale(self):
        """ Product sold, reduce number of items by 1 """
        self.number_of_items -= 1


if __name__ == "__main__":
	main()