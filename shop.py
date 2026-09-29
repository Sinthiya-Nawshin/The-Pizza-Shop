"""
shop.py
=======
SINGLETON (GoF creational pattern): the PizzaShop.

The pizza shop is a single shared point of truth for the whole program:
one price list (the menu) and one order list. The Builder reads prices
from it and the client places orders through it. Exactly one instance
can exist; everyone gets the same one through PizzaShop.get_instance().
"""


class PizzaShop:
    """Singleton: one menu + one order list for the whole application."""

    _instance = None                      # the only instance (GoF: uniqueInstance)

    def __init__(self):
        # guard: __init__ runs for every get_instance() call -> init once
        if getattr(self, "_initialized", False):
            return
        self._menu = {
            "base_price": {               # size -> price
                "Small": 5.00, "Medium": 7.00, "Large": 9.00,
            },
            "dough_price": {              # dough -> surcharge
                "classic": 0.00, "thin": 0.50, "whole-grain": 1.00,
            },
            "topping_price": {            # topping -> price
                "cheese": 1.00, "mushrooms": 1.20, "ham": 1.50,
                "pepperoni": 1.80, "olives": 0.90, "onions": 0.70,
                "tomato": 0.60, "chicken": 2.00,
            },
        }
        self._orders = []                 # (pizza, final_price) tuples
        self._initialized = True

    @classmethod
    def get_instance(cls):
        """Classic Singleton access point (GoF: Instance())."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # -- menu (used by the Builder and by Pizza.get_price) -------------------
    def get_base_price(self, size, dough):
        return (self._menu["base_price"][size]
                + self._menu["dough_price"][dough])

    def get_topping_price(self, topping):
        return self._menu["topping_price"][topping]

    def print_menu(self):
        print("MENU".center(46, "-"))
        for size, price in self._menu["base_price"].items():
            print("  {:<12} {:>6.2f} EUR".format(size + " pizza", price))
        print("  dough:  " + ", ".join(
            "{} {:+.2f}".format(d, p)
            for d, p in self._menu["dough_price"].items()))
        print("  toppings: " + ", ".join(
            "{} {:.2f}".format(t, p)
            for t, p in self._menu["topping_price"].items()))

    # -- orders ---------------------------------------------------------------
    def place_order(self, pizza):
        """Accept any pizza entity, with or without roles, in the same way."""
        self._orders.append((pizza, pizza.get_price()))
        print("Order accepted: {} -> {:.2f} EUR".format(
            pizza.get_name(), pizza.get_price()))

    def list_orders(self):
        print("ORDERS".center(46, "-"))
        if not self._orders:
            print("  (no orders yet)")
        for i, (pizza, price) in enumerate(self._orders, 1):
            print("  {}. {:<22} {:>6.2f} EUR".format(
                i, pizza.get_name(), price))
            print("     " + pizza.get_description())
