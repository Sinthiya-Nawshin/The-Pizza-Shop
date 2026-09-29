# Pizza Shop (GoF Design Patterns)

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
