# Pizza Shop - OOD Homework (GoF Design Patterns)

Console application in Python 3 demonstrating three GoF patterns:

| Pattern    | Where                          | What it does |
|------------|--------------------------------|--------------|
| Decorator  | `model.py` (PizzaRole + 4 roles) | Dynamic roles on pizza entities |
| Builder    | `builder.py` (PizzaBuilder, PizzaDirector) | Step-by-step pizza construction |
| Singleton  | `shop.py` (PizzaShop)          | One shared shop: menu + orders |

## Run

```
python main.py
```

No external libraries needed. Python 3.8+.

## Files

- `model.py` - Pizza entity, abstract PizzaRole decorator, concrete roles
  (ExtraCheeseRole, SpicyRole, VeganRole, StuffedCrustRole), role management
  (add_role / remove_role / has_role / get_role)
- `builder.py` - fluent PizzaBuilder + PizzaDirector with standard recipes
- `shop.py` - PizzaShop singleton (price menu, order list)
- `main.py` - labelled demo covering every homework requirement
- `sample_output.txt` - captured output of one run

## Homework requirements coverage

1. Entities with/without roles used the same way -> common `Pizza` interface,
   roles delegate it (section 6 of the demo).
2. Role detection + role-specific use -> `has_role()`, `get_role()`, e.g.
   `SpicyRole.heat_level()` (section 4).
3. Dynamic gain/lose roles -> `add_role()`, `remove_role()` (sections 3, 5).
4. Expandable role set -> a new role is one new `PizzaRole` subclass.
5. Multiple simultaneous roles -> stacked decorators (section 3).
