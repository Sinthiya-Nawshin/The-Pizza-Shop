"""
main.py
=======
Working prototype / sample execution of the Pizza Shop homework.

Run:  python main.py

The demo walks through every homework requirement and prints a labelled
section for each, so it can double as the classroom demonstration script.
"""

from model import ExtraCheeseRole, SpicyRole, VeganRole, StuffedCrustRole
from builder import PizzaBuilder, PizzaDirector
from shop import PizzaShop


def section(title):
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def show(pizza):
    """Use the entity through the COMMON interface only."""
    print("  name   : " + pizza.get_name())
    print("  desc   : " + pizza.get_description())
    print("  price  : {:.2f} EUR".format(pizza.get_price()))


def main():
    shop = PizzaShop.get_instance()

    # ------------------------------------------------------------------ #
    section("1. SINGLETON: the shop is one shared instance")
    shop2 = PizzaShop.get_instance()
    print("  shop  id: ", id(shop))
    print("  shop2 id: ", id(shop2))
    print("  same object? ", shop is shop2)
    shop.print_menu()

    # ------------------------------------------------------------------ #
    section("2. BUILDER: step-by-step construction")
    director = PizzaDirector()
    margherita = director.build_margherita("Large")
    custom = (PizzaBuilder()
              .set_name("My Custom")
              .set_size("Medium")
              .set_dough("thin")
              .add_topping("ham")
              .add_topping("olives")
              .build())
    show(margherita)
    show(custom)

    # ------------------------------------------------------------------ #
    section("3. DECORATOR: gain roles dynamically (multiple at once)")
    custom = custom.add_role(ExtraCheeseRole)
    custom = custom.add_role(SpicyRole, heat=5)
    show(custom)

    # ------------------------------------------------------------------ #
    section("4. ROLE INTERFACES: detect a role, use it specifically")
    print("  has ExtraCheeseRole? ", custom.has_role(ExtraCheeseRole))
    print("  has VeganRole?       ", custom.has_role(VeganRole))
    spicy = custom.get_role(SpicyRole)          # role interface
    if spicy:
        print("  heat level via role : ", spicy.heat_level())
    cheese = custom.get_role(ExtraCheeseRole)
    if cheese:
        print("  cheese via role     : ", cheese.cheese_blend())

    # ------------------------------------------------------------------ #
    section("5. DECORATOR: lose a role dynamically")
    custom = custom.remove_role(SpicyRole)
    show(custom)
    print("  still spicy?         ", custom.has_role(SpicyRole))

    # ------------------------------------------------------------------ #
    section("6. COMMON INTERFACE: with/without roles used the same way")
    vegan = director.build_margherita("Small").add_role(VeganRole)
    vegan = vegan.add_role(StuffedCrustRole)
    order_batch = [margherita, custom, vegan]   # plain, decorated, decorated
    for p in order_batch:                        # one loop, one interface
        show(p)
    stuffed = vegan.get_role(StuffedCrustRole)
    if stuffed:
        print("  stuffed crust bonus  : ", stuffed.dipping_sauce())
    print("  vegan allergens      : ", vegan.get_role(VeganRole).allergens())

    # ------------------------------------------------------------------ #
    section("7. ORDERS through the Singleton shop")
    for p in order_batch:
        shop.place_order(p)
    shop.list_orders()


if __name__ == "__main__":
    main()
