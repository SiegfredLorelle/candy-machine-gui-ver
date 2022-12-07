# TODO
# admin
# comments
# clean up code

import tkinter as tk
from tkinter import messagebox


def main():

    app = App()
    app.mainloop()





class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.candy_machine = Candy_Machine()
        self.candy_machine.chip_dispenser.dispenser(set_cost=5, set_no_of_items=1)
        # print(self.candy_machine.chip_dispenser)
        self.candy_machine.item = "candy"



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
        for F in {Selection_Menu, Admin_Menu, Buy_Page}:
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
                    return messagebox.showerror("Error", f"Sorry {self.candy_machine.item} is out of stock.")

                self.build_frames()
                self.show_frame(Buy_Page)

        if coming_from == "buy":
            if doing == "buy":
                is_successful = self.candy_machine.sell_product(self.frames[Buy_Page].entry.get())
                self.frames[Buy_Page].entry.delete(0, tk.END)

                if is_successful:
                    self.show_frame(Selection_Menu)

            elif doing == "back":
                if self.candy_machine.deposit != 0:
                    if messagebox.askokcancel(title="Cancel?", message=f"Are you sure you want to cancel the purchase of {self.candy_machine.item}?"):
                        messagebox.showinfo(title="Return", message=f"Here is the ${self.candy_machine.deposit:,.2f} you deposited.")
                        self.candy_machine.deposit = 0
                        self.show_frame(Selection_Menu)
                else:
                    self.show_frame(Selection_Menu)


        

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

        title = tk.Label(self, text="My Candy Machine", font="Times 25 bold", bg="#C0EEE4")
        title.grid(row=0, column=0, columnspan=2, sticky="nesw")

        intstructions = tk.Label(self, text="Press an item to purchase!", font="Times 18 bold", fg="black", bg="#FFD1D1")
        intstructions.grid(row=1, column=0, columnspan=2, sticky="nesw")

        candy = tk.Button(self, text="Candy", font="Times 15", bg="#FFE3E1", command=lambda: parent.controller("selection", item="candy"))
        candy.grid(row=2, column=0, columnspan=2, sticky="nesw")

        chip = tk.Button(self, text="Chip", font="Times 15", bg="#FFE3E1", command=lambda: parent.controller("selection", item="chip"))
        chip.grid(row=3, column=0, columnspan=2, sticky="nesw")

        gum = tk.Button(self, text="Gum", font="Times 15", bg="#FFE3E1", command=lambda: parent.controller("selection", item="gum"))
        gum.grid(row=4, column=0, columnspan=2, sticky="nesw")

        cookie = tk.Button(self, text="Cookie", font="Times 15", bg="#FFE3E1", command=lambda: parent.controller("selection", item="cookie"))
        cookie.grid(row=5, column=0, columnspan=2, sticky="nesw")

        exit = tk.Button(self, text="Exit", font="Times 15", bg="#FFE3E1", command=parent.on_closing)
        exit.grid(row=6, column=0, sticky="nesw", ipadx=15)

        admin = tk.Button(self, text="Admin", font="Times 15", bg="#FFE3E1", command=lambda: parent.show_frame(parent.Admin_Menu))
        admin.grid(row=6, column=1, sticky="nesw")


class Admin_Menu(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container, bg="black")

        label = tk.Label(self, text="Admin Menu", font=("Times", 30))


class Buy_Page(tk.Frame):
    def __init__(self, parent, container):
        super().__init__(container, bg="#FFCAC8")

        for number in range(8):
            self.grid_rowconfigure(number, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        title = tk.Label(self, text="My Candy Machine", font="Times 25 bold", fg="black", bg="#C0EEE4")
        title.grid(row=0, column=0, columnspan=2, sticky="nesw")


        instructions = tk.Label(self, text=f"Insert ${parent.candy_machine.item_key[parent.candy_machine.item].get_product_cost():,} to buy a {parent.candy_machine.item}:", font="Times 18 bold", fg="black", bg="#FFCAC8")
        instructions.grid(row=1, column=0, columnspan=2,sticky="nesw")

        self.entry = tk.Entry(self, font="Times 25 bold", justify="center")
        self.entry.grid(row=2, column=0, columnspan=2)
        self.entry.focus_set()

        back = tk.Button(self, text="Back", font="Times 15", bg="#FFD1D1", command=lambda: parent.controller("buy", "back"))
        back.grid(row=8, column=0, sticky="w", ipadx=15, padx=20, pady=20)

        deposit = tk.Button(self, text="Insert", font="Times 15", bg="#C0EEE4", command=lambda: parent.controller("buy", "buy"))
        deposit.grid(row=3, column=0, columnspan=2, ipadx=15)































class Candy_Machine():

    def __init__(self):
        # super().__init__()

        """ Initalize the components of candy machine """

        self.cash_register = self.Cash_Register()
        self.candy_dispenser = self.Dispenser()
        self.chip_dispenser = self.Dispenser()
        self.gum_dispenser = self.Dispenser()
        self.cookie_dispenser = self.Dispenser()

        self.deposit = 0

        # Key mapping in selection menu
        self.item_key = {"candy": self.candy_dispenser,
                         "chip": self.chip_dispenser,
                         "gum": self.gum_dispenser,
                         "cookie": self.cookie_dispenser,
                         "A": "admin"}

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
    def item(self):
        return self._item

    # Setter
    @item.setter
    def item(self, item):
        if not item or item not in self.item_key:
            return messagebox.showerror("Error", "An error has occured.\nSelected item is invalid.")
        else:
            self._item = item

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



    # Getter
    @property
    def deposit(self):
        return self._deposit

    # Setter
    @deposit.setter
    def deposit(self, deposit):
        if deposit < 0:
            raise ValueError("Deposit must be positive.")
        else:
            self._deposit = deposit


    def program():
        """ Start the program"""
        # app = App()
        # app.mainloop()

    def sell_product(self, new_deposit):
        """ Sell the item selected by the customer, return true if purchase is successful """
        # Ensure that the chosen item is not out of stock
        
        if self.item_key[self.item].get_count() <= 0:
            messagebox.showerror("Error", f"Sorry {self.item} is out of stock.")
            return False
        try:
            new_deposit = int(new_deposit)

            if new_deposit > 0:
                self.deposit += new_deposit

        except (ValueError, TypeError):
            messagebox.showerror("Error", f"Inserted cash must be positive number.")
            return False

        # Asks for more if deposit is not enough
        if self.deposit < self.item_key[self.item].get_product_cost():
            messagebox.showinfo("Insufficient Deposit", f"Deposit ${self.item_key[self.item].get_product_cost() - self.deposit} more.")
            return False

        # Give the item if deposit is enough
        self.item_key[self.item].makeSale()

        # Register takes in the payment (not total deposit, just the price of item)
        self.cash_register.accept_amount(self.item_key[self.item].get_product_cost())

        # if there is change, return it
        if  self.deposit != self.item_key[self.item].get_product_cost():
            messagebox.showinfo("Success", f"Successfully purchased a {self.item}!\nHere is your {self.item}! Enjoy!\n\nHere also is your change of ${self.deposit - self.item_key[self.item].get_product_cost():,.2f}")
        else:
            messagebox.showinfo("Success", f"Successfully purchased a {self.item}!\nHere is your {self.item}! Enjoy!")
        self.deposit = 0
        return True


    def show_selection(self):
        """ displays the main menu, allow users to select an item to buy """


    def show_admin_menu(self):
        """ Allows owner to view and set balance in register, and set price and number of items """
        print("\nAdmin Settings: Enter corresponding value")
        print("1 - Set Candy \n2 - Set Chips \n3 - Set Gum \n4 - Set Cookies\n\nV - View Balance \nS - Set Balance \nQ - Back")
        self.admin_choice = input("\nYour choice:  ")[0].upper() 


    class Cash_Register():
        """ Component of Candy Machine, handles money """

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