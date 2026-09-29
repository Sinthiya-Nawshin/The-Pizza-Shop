"""
model.py
========
The object model of the Pizza Shop homework.

Design patterns demonstrated here:
    * DECORATOR (GoF structural pattern) -- implements the "dynamic roles"
      requirement: a Pizza entity can gain/lose additional roles at runtime,
      keep its common interface, hold several roles at once, and the set of
      roles is easily expandable (one new class = one new role).

Role requirements mapping (homework statement -> code):
    1. "use entities, with or without roles, in the same way"
          -> PizzaRole delegates the whole common Pizza interface.
    2. "find out if the entity has a role and use it through the role interface"
          -> Pizza.has_role() / Pizza.get_role(); roles expose extra
             operations (heat_level(), allergens(), ...).
    3. "an entity should be able dynamically to gain/lose roles"
          -> Pizza.add_role() / Pizza.remove_role().
    4. "the set of roles should be easily expandable"
          -> subclass PizzaRole, nothing else needs to change.
    5. "an entity ... multiple roles simultaneously"
          -> decorators are stacked: Vegan(Spicy(ExtraCheese(Pizza))).
"""

from abc import ABC


# ---------------------------------------------------------------------------
# Common interface of every pizza entity (with or without roles)
# ---------------------------------------------------------------------------
class Pizza:
    """A concrete pizza entity: the common functionality every entity has.

    It is also the Component of the Decorator pattern: role decorators
    wrap a Pizza (or another role) and expose the same interface.
    """

    def __init__(self, name, size, dough, toppings):
        self._name = name
        self._size = size            # 'Small' | 'Medium' | 'Large'
        self._dough = dough          # 'classic' | 'thin' | 'whole-grain'
        self._toppings = list(toppings)

    # -- common interface ---------------------------------------------------
    def get_name(self):
        return self._name

    def get_size(self):
        return self._size

    def get_dough(self):
        return self._dough

    def get_toppings(self):
        return list(self._toppings)

    def get_description(self):
        return "{} pizza on {} dough with {}".format(
            self._size, self._dough,
            ", ".join(self._toppings) if self._toppings else "no toppings")

    def get_price(self):
        """Base price; the Singleton PizzaShop owns all price data."""
        from shop import PizzaShop
        shop = PizzaShop.get_instance()
        price = shop.get_base_price(self._size, self._dough)
        price += sum(shop.get_topping_price(t) for t in self._toppings)
        return round(price, 2)

    # -- role management (Decorator add / remove / test / access) -----------
    def add_role(self, role_class, *args, **kwargs):
        """Dynamically GAIN a role. Returns the new outermost entity, so the
        client re-binds:  pizza = pizza.add_role(SpicyRole)."""
        return role_class(self, *args, **kwargs)

    def has_role(self, role_class):
        """Requirement 2: can the entity be used specifically as role_class?"""
        return self.get_role(role_class) is not None

    def get_role(self, role_class):
        """Return the role object (the role interface) or None."""
        node = self
        while isinstance(node, PizzaRole):
            if isinstance(node, role_class):
                return node
            node = node._wrapped
        return None

    def remove_role(self, role_class):
        """Dynamically LOSE a role: unwrap the decorator chain, drop every
        decorator of role_class, re-wrap the rest, return the new outermost."""
        chain = []                       # outer -> inner
        node = self
        while isinstance(node, PizzaRole):
            chain.append(node)
            node = node._wrapped
        kept = [r for r in reversed(chain) if not isinstance(r, role_class)]
        result = node                    # the plain Pizza at the bottom
        for role in kept:                # re-wrap inside -> outside
            role._wrapped = result
            result = role
        return result


# ---------------------------------------------------------------------------
# Decorator pattern: abstract role decorator
# ---------------------------------------------------------------------------
class PizzaRole(Pizza, ABC):
    """Abstract Decorator: IS-A Pizza (same interface) and HAS-A Pizza
    (delegates the common operations to the wrapped entity)."""

    def __init__(self, wrapped):
        self._wrapped = wrapped

    # delegation of the common interface (requirement 1)
    def get_name(self):
        return self._wrapped.get_name()

    def get_size(self):
        return self._wrapped.get_size()

    def get_dough(self):
        return self._wrapped.get_dough()

    def get_toppings(self):
        return self._wrapped.get_toppings()

    def get_description(self):
        return self._wrapped.get_description()

    def get_price(self):
        return self._wrapped.get_price()


# ---------------------------------------------------------------------------
# Concrete roles -- each one is ONE small class (requirement 4: expandable)
# ---------------------------------------------------------------------------
class ExtraCheeseRole(PizzaRole):
    """Extra cheese: changes the common functionality (price, description)."""
    SURCHARGE = 1.50

    def get_price(self):
        return round(self._wrapped.get_price() + self.SURCHARGE, 2)

    def get_description(self):
        return self._wrapped.get_description() + ", extra cheese"

    # role-specific operation, usable through the role interface
    def cheese_blend(self):
        return "mozzarella + cheddar blend"


class SpicyRole(PizzaRole):
    """Spicy: adds a role-specific operation heat_level()."""
    SURCHARGE = 1.00

    def __init__(self, wrapped, heat=4):
        super().__init__(wrapped)
        self._heat = heat                # 1..5

    def get_price(self):
        return round(self._wrapped.get_price() + self.SURCHARGE, 2)

    def get_description(self):
        return self._wrapped.get_description() + ", spicy"

    def heat_level(self):
        return self._heat


class VeganRole(PizzaRole):
    """Vegan: replaces cheese in the description, adds allergen info."""
    SURCHARGE = 2.00

    def get_price(self):
        return round(self._wrapped.get_price() + self.SURCHARGE, 2)

    def get_description(self):
        text = self._wrapped.get_description()
        return text.replace("cheese", "vegan cheese") + " [vegan]"

    def allergens(self):
        return "no dairy, no animal products"


class StuffedCrustRole(PizzaRole):
    """Stuffed crust: premium crust option with its own operation."""
    SURCHARGE = 2.50

    def get_price(self):
        return round(self._wrapped.get_price() + self.SURCHARGE, 2)

    def get_description(self):
        return self._wrapped.get_description() + ", stuffed crust"

    def dipping_sauce(self):
        return "garlic sauce included"
