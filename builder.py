"""
builder.py
==========
BUILDER (GoF creational pattern): step-by-step construction of a Pizza.

* PizzaBuilder  -- the Builder: assembles a pizza piece by piece
  (name -> size -> dough -> toppings) and builds the final entity.
* PizzaDirector -- the optional Director: knows the standard recipes and
  drives the same builder through preset construction sequences.

The builder validates every part against the Singleton PizzaShop menu,
so the two creational patterns cooperate: the Builder constructs, the
Singleton supplies the shared price data.
"""

from model import Pizza


class PizzaBuilder:
    """Fluent Builder for Pizza entities."""

    def __init__(self):
        self.reset()

    def reset(self):
        self._name = None
        self._size = None
        self._dough = None
        self._toppings = []

    # -- construction steps (each returns the builder: fluent chain) ---------
    def set_name(self, name):
        self._name = name
        return self

    def set_size(self, size):
        self._size = size
        return self

    def set_dough(self, dough):
        self._dough = dough
        return self

    def add_topping(self, topping):
        self._toppings.append(topping)
        return self

    # -- product retrieval ----------------------------------------------------
    def build(self):
        """Validate against the Singleton menu, then return the Pizza."""
        from shop import PizzaShop
        shop = PizzaShop.get_instance()

        if self._size not in shop._menu["base_price"]:
            raise ValueError("Unknown size: {}".format(self._size))
        if self._dough not in shop._menu["dough_price"]:
            raise ValueError("Unknown dough: {}".format(self._dough))
        for t in self._toppings:
            if t not in shop._menu["topping_price"]:
                raise ValueError("Unknown topping: {}".format(t))

        name = self._name or "Custom Pizza"
        pizza = Pizza(name, self._size, self._dough, self._toppings)
        self.reset()                      # builder is reusable after build()
        return pizza


class PizzaDirector:
    """Director: standard recipes built through the same Builder."""

    def __init__(self, builder=None):
        self._builder = builder or PizzaBuilder()

    def build_margherita(self, size="Medium"):
        return (self._builder.set_name("Margherita")
                .set_size(size)
                .set_dough("classic")
                .add_topping("cheese")
                .add_topping("tomato")
                .build())

    def build_pepperoni(self, size="Large"):
        return (self._builder.set_name("Pepperoni")
                .set_size(size)
                .set_dough("thin")
                .add_topping("cheese")
                .add_topping("pepperoni")
                .build())
