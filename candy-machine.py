# TODO
# TEST
# comments
# clean up code

import tkinter as tk
from tkinter import messagebox


def main():

    app = App()
    app.mainloop()





class App(tk.Tk):
    """ GUI app """
    def __init__(self):
        super().__init__()
        
        # Create a candy machine
        self.candy_machine = Candy_Machine()

        self.title('My Candy Machine')
        self.geometry('1080x720')
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.container = tk.Frame(self, bg="#FFCAC8")
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.Selection_Menu = Selection_Menu
        self.Admin_Menu = Admin_Menu
        self.Buy_Page = Buy_Page

        self.build_frames()
        
        self.show_frame(Selection_Menu)

    def build_frames(self):
        for F in {Selection_Menu, Admin_Menu, Buy_Page, Edit_Balance, Edit_Item}:
            frame = F(self, self.container)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
    
    def controller(self, coming_from, doing=None, item=None):
        if coming_from == "selection":
            if item:
                self.candy_machine.item = item
                if self.candy_machine.item_key[self.candy_machine.item].get_count() <= 0:
                    return messagebox.showerror("Error", f"Sorry, {self.candy_machine.item} is out of stock.")
                self.build_frames()
                self.frames[Buy_Page].buy_entry.focus_set()
                self.show_frame(Buy_Page)


        elif coming_from == "buy":
            if doing == "buy":
                is_successful = self.candy_machine.sell_product(self.frames[Buy_Page].buy_entry.get())
                self.frames[Buy_Page].buy_entry.delete(0, tk.END)

                if is_successful:
                    self.build_frames()
                    self.show_frame(Selection_Menu)

            elif doing == "back":
                if self.candy_machine.deposit != 0:
                    if messagebox.askokcancel(title="Cancel?", message=f"Are you sure you want to cancel the purchase of {self.candy_machine.item}?"):
                        messagebox.showinfo(title="Return", message=f"Here is the ${self.candy_machine.deposit:,.2f} you deposited.")
                        self.candy_machine.deposit = 0
                        self.show_frame(Selection_Menu)
                else:
                    self.show_frame(Selection_Menu)

        elif coming_from == "admin":
            self.build_frames()

            if item == "balance":
                self.frames[Edit_Balance].balance_entry.focus_set()
                self.show_frame(Edit_Balance)

            else:
                self.candy_machine.item = item
                self.frames[Edit_Item].price_entry.focus_set()
                self.show_frame(Edit_Item)


        elif coming_from == "edit_balance":
            if doing == "save":
                try:
                    entered_balance = int(self.frames[Edit_Balance].balance_entry.get())

                except (TypeError, ValueError):
                    messagebox.showerror("Error", "Balance in the candy machine must be a positive integer.")
                    self.build_frames()
                    self.show_frame(Edit_Balance)
                    return
                if self.candy_machine.cash_register.current_balance() == entered_balance:
                    messagebox.showerror("Error", "Balance in the candy machine remains the same.")

                elif entered_balance < 0:
                    messagebox.showinfo("Warning", "Balance in the machine were set to default due to invalid input.")

                else:
                    self.candy_machine.cash_register.cash_register(entered_balance)
                    messagebox.showinfo("success", f"There are ${self.candy_machine.cash_register.current_balance():,.2f} in the candy machine.")

                self.build_frames()
                self.show_frame(Edit_Balance)

        elif coming_from == "edit_item":
            if doing == "save":
                current_dispenser = self.candy_machine.item_key[self.candy_machine.item]

                try:
                    entered_stocks = int(self.frames[Edit_Item].stocks_entry.get())
                    entered_price = int(self.frames[Edit_Item].price_entry.get())

                except (TypeError, ValueError):
                    messagebox.showerror("Error", "Price and number of stocks must be a positive integer.")
                    self.build_frames()
                    self.show_frame(Edit_Item)
                    return

                if current_dispenser.get_count() == entered_stocks and current_dispenser.get_product_cost() == entered_price:
                    messagebox.showerror("Error", "Price and number of stocks remains the same.")
                elif entered_price <= 0 or entered_stocks < 0:
                    messagebox.showinfo("Warning", "Values were set to default due to invalid values.")
                else:
                    current_dispenser.dispenser(entered_price, entered_stocks)
                    messagebox.showinfo("Success", "Changes were saved.\n")

                self.build_frames()
                self.show_frame(Edit_Item)








    # Reprompt when closing
    def on_closing(self):
        if messagebox.askyesno(title="Exit?", message="Do you really want to close 'My Candy Machine'?"):
            self.destroy()





class Selection_Menu(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container, bg="#FFD1D1")

        for number in range(7):
            self.grid_rowconfigure(number, weight=1)
        for number in range(2):
            self.grid_columnconfigure(number, weight=1)

        title = tk.Label(self, text="My Candy Machine", font="Helvetica 25 bold", bg="#C0EEE4")
        title.grid(row=0, column=0, columnspan=2, sticky="nesw")

        intstructions = tk.Label(self, text="Press an item to purchase!", font="Helvetica 18 bold", fg="black", bg="#FFD1D1")
        intstructions.grid(row=1, column=0, columnspan=2, sticky="nesw")

        candy = tk.Button(self, text="Candy", font="Helvetica 15", bg="#E8C4C4", command=lambda: parent.controller("selection", item="candy"))
        candy.grid(row=2, column=0, columnspan=2, sticky="nesw")

        chip = tk.Button(self, text="Chip", font="Helvetica 15", bg="#E8C4C4", command=lambda: parent.controller("selection", item="chip"))
        chip.grid(row=3, column=0, columnspan=2, sticky="nesw")

        gum = tk.Button(self, text="Gum", font="Helvetica 15", bg="#E8C4C4", command=lambda: parent.controller("selection", item="gum"))
        gum.grid(row=4, column=0, columnspan=2, sticky="nesw")

        cookie = tk.Button(self, text="Cookie", font="Helvetica 15", bg="#E8C4C4", command=lambda: parent.controller("selection", item="cookie"))
        cookie.grid(row=5, column=0, columnspan=2, sticky="nesw")

        exit = tk.Button(self, text="Exit", font="Helvetica 15", bg="#F2E5E5", command=parent.on_closing)
        exit.grid(row=6, column=0, sticky="nesw")

        admin = tk.Button(self, text="Admin", font="Helvetica 15", bg="#E8C4C4", command=lambda: parent.show_frame(parent.Admin_Menu))
        admin.grid(row=6, column=1, sticky="nesw")


class Admin_Menu(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container, bg="#CE7777")

        for number in range(8):
            self.grid_rowconfigure(number, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title = tk.Label(self, text="Admin Menu", font="Times 25 bold", fg="white", bg="#2B3A55")
        title.grid(row=0, column=0, sticky="nesw")

        intstructions = tk.Label(self, text="Press item to manage!", font="Times 18 bold", fg="white", bg="#CE7777")
        intstructions.grid(row=1, column=0, sticky="nesw")

        admin = tk.Button(self, text="Balance", font="Times 15", bg="#E8C4C4", command=lambda: parent.controller("admin", item="balance"))
        admin.grid(row=2, column=0, sticky="nesw")

        candy = tk.Button(self, text="Candy", font="Times 15", bg="#E8C4C4", command=lambda: parent.controller("admin", item="candy"))
        candy.grid(row=3, column=0, sticky="nesw")

        chip = tk.Button(self, text="Chip", font="Times 15", bg="#E8C4C4", command=lambda: parent.controller("admin", item="chip"))
        chip.grid(row=4, column=0, sticky="nesw")

        gum = tk.Button(self, text="Gum", font="Times 15", bg="#E8C4C4", command=lambda: parent.controller("admin", item="gum"))
        gum.grid(row=5, column=0, sticky="nesw")

        cookie = tk.Button(self, text="Cookie", font="Times 15", bg="#E8C4C4", command=lambda: parent.controller("admin", item="cookie"))
        cookie.grid(row=6, column=0, sticky="nesw")

        exit = tk.Button(self, text="Back", font="Times 15", bg="#F2E5E5", command=lambda: parent.show_frame(parent.Selection_Menu))
        exit.grid(row=7, column=0, sticky="nesw", ipadx=15)


class Buy_Page(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container, bg="#FFD1D1")

        for number in range(8):
            self.grid_rowconfigure(number, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title = tk.Label(self, text="My Candy Machine", font="Helvetica 25 bold", fg="black", bg="#C0EEE4")
        title.grid(row=0, column=0, columnspan=2, sticky="nesw")


        instructions = tk.Label(self, text=f"Insert ${parent.candy_machine.item_key[parent.candy_machine.item].get_product_cost():,} to buy a {parent.candy_machine.item}:", font="Helvetica 18 bold", fg="black", bg="#FFD1D1")
        instructions.grid(row=1, column=0, columnspan=2,sticky="nesw")

        self.buy_entry = tk.Entry(self, font="Helvetica 25", justify="center")
        self.buy_entry.grid(row=2, column=0, columnspan=2)
        self.buy_entry.focus_get()

        back = tk.Button(self, text="Back", font="Helvetica 15", bg="#FFD1D1", command=lambda: parent.controller("buy", "back"))
        back.grid(row=8, column=0, sticky="w", ipadx=15, padx=20, pady=20)

        deposit = tk.Button(self, text="Insert", font="Helvetica 15", bg="#C0EEE4", command=lambda: parent.controller("buy", "buy"))
        deposit.grid(row=3, column=0, columnspan=2, ipadx=15)






class Edit_Balance(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container, bg="#CE7777")

        for number in range(8):
            self.grid_rowconfigure(number, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title = tk.Label(self, text="Admin Menu", font="Times 25 bold", fg="white", bg="#2B3A55")
        title.grid(row=0, column=0, columnspan=2, sticky="nesw")

        instructions = tk.Label(self, text=f"Save changes to set a new balance in the candy machine.", font="Times 18 bold", fg="white", bg="#CE7777")
        instructions.grid(row=2, column=0, columnspan=2,sticky="nesw")

        price = tk.Label(self, text="Amount of cash in the candy machine:", font="Times 18 bold", fg="white", bg="#CE7777")
        price.grid(row=3, column=0, columnspan=2 ,sticky="esw")

        self.balance_entry = tk.Entry(self, font="Times 25", justify="center")
        # print(parent.candy_machine.cash_register.current_balance())
        self.balance_entry.insert(0, parent.candy_machine.cash_register.current_balance())
        self.balance_entry.grid(row=4, column=0, columnspan=2)

        save = tk.Button(self, text="Save Changes", font="Times 15", fg="white", bg="#2B3A55", command=lambda: parent.controller("edit_balance", "save"))
        save.grid(row=5, column=0, columnspan=2, ipadx=15)

        back = tk.Button(self, text="Back", font="Times 15", fg="white", bg="#CE7777", command=lambda: parent.show_frame(Admin_Menu))
        back.grid(row=8, column=0, sticky="w", ipadx=15, padx=20, pady=20)


class Edit_Item(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container, bg="#CE7777")

        for number in range(8):
            self.grid_rowconfigure(number, weight=1)
        self.grid_columnconfigure(0, weight=1)

        title = tk.Label(self, text="Admin Menu", font="Times 25 bold", fg="white", bg="#2B3A55")
        title.grid(row=0, column=0, columnspan=2, sticky="nesw")

        instructions = tk.Label(self, text=f"Save the changes to edit the values of {parent.candy_machine.item}.", font="Times 18 bold", fg="white", bg="#CE7777")
        instructions.grid(row=1, column=0, columnspan=2,sticky="nesw")

        price = tk.Label(self, text=f"Price of a {parent.candy_machine.item}:", font="Times 18 bold", fg="white", bg="#CE7777")
        price.grid(row=2, column=0, columnspan=2 ,sticky="esw")

        self.price_entry = tk.Entry(self, font="Times 25", justify="center")
        self.price_entry.insert(0, parent.candy_machine.item_key[parent.candy_machine.item].get_product_cost())
        self.price_entry.grid(row=3, column=0, columnspan=2)

        stocks = tk.Label(self, text=f"Number of available {parent.candy_machine.item}:", font="Times 18 bold", fg="white", bg="#CE7777")
        stocks.grid(row=4, column=0, columnspan=2 ,sticky="esw")

        self.stocks_entry = tk.Entry(self, font="Times 25", justify="center")
        self.stocks_entry.insert(0, parent.candy_machine.item_key[parent.candy_machine.item].get_count())
        self.stocks_entry.grid(row=5, column=0, columnspan=2)

        save = tk.Button(self, text="Save Changes", font="Times 15", fg="white", bg="#2B3A55", command=lambda: parent.controller("edit_item", "save"))
        save.grid(row=6, column=0, columnspan=2, ipadx=15)

        back = tk.Button(self, text="Back", font="Times 15", fg="white", bg="#CE7777", command=lambda: parent.show_frame(Admin_Menu))
        back.grid(row=8, column=0, sticky="w", ipadx=15, padx=20, pady=20)


























class Candy_Machine():

    def __init__(self):
        """ Initalize the components of candy machine """
        self.cash_register = self.Cash_Register()
        self.candy_dispenser = self.Dispenser()
        self.chip_dispenser = self.Dispenser()
        self.gum_dispenser = self.Dispenser()
        self.cookie_dispenser = self.Dispenser()

        # Key mapping to access each items' dispenser
        self.item_key = {"candy": self.candy_dispenser,
                         "chip": self.chip_dispenser,
                         "gum": self.gum_dispenser,
                         "cookie": self.cookie_dispenser}

        # Variables accessed/modified app
        self.deposit = 0
        self.item = "candy"

    # Item Getter
    @property
    def item(self):
        return self._item

    # Item Setter
    @item.setter
    def item(self, item):
        # Ensures the item maps to the key
        if not item or item not in self.item_key:
            return messagebox.showerror("Error", "An error has occured.\nSelected item is invalid.")
        else:
            self._item = item

    # Deposit Getter
    @property
    def deposit(self):
        return self._deposit

    # Desposit Setter
    @deposit.setter
    def deposit(self, deposit):
        # Ensures deposit is a non negative integer
        if deposit < 0:
            raise ValueError("Deposit must be positive.")
        else:
            self._deposit = deposit


    def sell_product(self, new_deposit):
        """ Sell the item selected by the customer, return true if purchase is successful """

        # Ensure that the chosen item is not out of stock
        if self.item_key[self.item].get_count() <= 0:
            messagebox.showerror("Error", f"Sorry {self.item} is out of stock.")
            return False
        # Ensures the inserted deposit is an non negative integer
        try:
            new_deposit = int(new_deposit)
            if new_deposit > 0:
                self.deposit += new_deposit
        # Show error message if inserted deposit is invalid
        except (ValueError, TypeError):
            messagebox.showerror("Error", f"Inserted cash must be positive number.")
            return False

        # Asks for more deposit if deposit is not enough to buy the item
        if self.deposit < self.item_key[self.item].get_product_cost():
            messagebox.showinfo("Insufficient Deposit", f"Deposit ${self.item_key[self.item].get_product_cost() - self.deposit} more.")
            return False

        # Give the item if deposit is enough
        self.item_key[self.item].makeSale()

        # Register takes in the payment (not total deposit, just the price of item)
        self.cash_register.accept_amount(self.item_key[self.item].get_product_cost())

        # Inform the user about the successful transcation
        # If there is change, return it
        if  self.deposit != self.item_key[self.item].get_product_cost():
            messagebox.showinfo("Success", f"Successfully purchased a {self.item}!\nHere is your {self.item}! Enjoy!\n\nHere also is your change of ${self.deposit - self.item_key[self.item].get_product_cost():,.2f}")
        else:
            messagebox.showinfo("Success", f"Successfully purchased a {self.item}!\nHere is your {self.item}! Enjoy!")
        
        # Reset the deposit
        self.deposit = 0
        return True



    # Component (inner class) of Candy Machine
    class Cash_Register():
        """ Handles money """

        def __init__(self, cash_on_hand=500):
            self.cash_on_hand = cash_on_hand

        # Cash Getter
        @property
        def cash_on_hand(self):
            return self._cash_on_hand

        # Cash Setter
        @cash_on_hand.setter
        def cash_on_hand(self, cash_on_hand):
            # Ensure cash is an integer
            if isinstance(cash_on_hand, int):
                # Change cash to default value if less than 0 (instructed in pdf)
                if cash_on_hand < 0:
                    self._cash_on_hand = 500
                else:
                    self._cash_on_hand = cash_on_hand
            else:
                raise TypeError("Cash on Hand must be an integer")

        # Prints out the cash by calling register itself
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
            # Ensures the amount paid by the customer is valid
            if isinstance(amount_in, int) and amount_in > 0:
                # Add the payment of customer to current cash on hand
                self.cash_on_hand += amount_in
            else:
                raise TypeError("Amount In must be non negative integer")

    # Component (inner class) of Candy Machine
    class Dispenser:
        """ Handles product """
        def __init__(self, cost=50, number_of_items=50):
            self.cost = cost
            self.number_of_items = number_of_items

        # Cost Getter
        @property
        def cost(self):
            return self._cost

        # Cost Setter
        @cost.setter
        def cost(self, cost):
            # Ensures cost of an item is an integer
            if isinstance(cost, int):
                # If cost of an item is not positive, set to default 50 (instructed in pdf)
                if cost <= 0:
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
            # Ensures the number if items in stock is an integer
            if isinstance(number_of_items, int):
                # If the number of items in stock is negative, set to default 50 (instructed in pdf)
                if number_of_items < 0:
                    self._number_of_items = 50 
                else:
                    self._number_of_items = number_of_items 
            else:
                raise TypeError("Number of Items must be an integer")

        # Prints out the cost and number of items by calling dispenser itself
        def __str__(self):
            return f"Cost is ${self.cost:,.2f} and Number of Items is {self.number_of_items}"

        def dispenser(self, set_cost=50, set_no_of_items=50):
            """ Let candy machine modify number of items and cost of an item """
            self.cost = set_cost
            self.number_of_items = set_no_of_items

        def get_count(self):
            """ returns the number of items in stock if an an item """
            return self.number_of_items

        def get_product_cost(self):
            """ returns the cost of an item """
            return self.cost

        def makeSale(self):
            """ Product sold, so reduce number of items in stock by 1 """
            self.number_of_items -= 1


if __name__ == "__main__":
	main()