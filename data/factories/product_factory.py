from typing import Any, Dict, List, Optional

from data.factories.base_factory import BaseFactory
from flows.flow_utils import (
    BACKPACK,
    BIKE_LIGHT,
    BOLT_TSHIRT,
    FLEECE_JACKET,
    ONESIE,
    RED_TSHIRT,
    ALL_ITEMS,
)


class ProductFactory(BaseFactory):
    """Generates product-related test data.

    Provides known SauceDemo products, random e-commerce products,
    price lists, and inventory payloads.
    """

    # ── Known SauceDemo Products ──────────────────────────────────

    _SAUCEDEMO_CATALOG: Dict[str, Dict[str, Any]] = {
        BACKPACK: {
            "name": BACKPACK,
            "description": "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequalled laptop and tablet protection.",
            "price": 29.99,
        },
        BIKE_LIGHT: {
            "name": BIKE_LIGHT,
            "description": "A red light isn't the desired state in testing but it sure helps when riding your bike at night. Water-resistant with 3 lighting modes.",
            "price": 9.99,
        },
        BOLT_TSHIRT: {
            "name": BOLT_TSHIRT,
            "description": "Get your testing superhero on with the Sauce Labs bolt T-shirt. From American Apparel, 100% ringspun combed cotton, heather gray with red bolt.",
            "price": 15.99,
        },
        FLEECE_JACKET: {
            "name": FLEECE_JACKET,
            "description": "It's not every day that you come across a midweight quarter-zip fleece jacket capable of handling everything from a relaxing day outdoors to a busy day at the office.",
            "price": 49.99,
        },
        ONESIE: {
            "name": ONESIE,
            "description": "Rib snap infant onesie for the junior automation engineer in development. Reinforced 3-snap bottom closure, two-needle hemmed sleeved and bottom won't unravel.",
            "price": 7.99,
        },
        RED_TSHIRT: {
            "name": RED_TSHIRT,
            "description": "This classic Sauce Labs t-shirt is perfect to wear when cozying up to your keyboard to automate a few tests. Super-soft and comfy ringspun combed cotton.",
            "price": 15.99,
        },
    }

    @staticmethod
    def saucedemo_product(name: str) -> Dict[str, Any]:
        if name not in ProductFactory._SAUCEDEMO_CATALOG:
            raise ValueError(
                f"Unknown SauceDemo product: '{name}'. "
                f"Available: {list(ProductFactory._SAUCEDEMO_CATALOG)}"
            )
        return dict(ProductFactory._SAUCEDEMO_CATALOG[name])

    @staticmethod
    def all_saucedemo_products() -> List[Dict[str, Any]]:
        return [ProductFactory.saucedemo_product(name) for name in ALL_ITEMS]

    @staticmethod
    def saucedemo_price_list() -> List[float]:
        return [ProductFactory._SAUCEDEMO_CATALOG[n]["price"] for n in ALL_ITEMS]

    # ── Random Product Data ───────────────────────────────────────

    def random_product(self, **overrides: Any) -> Dict[str, Any]:
        data = {
            "name": self.faker.catch_phrase(),
            "description": self.faker.text(max_nb_chars=120).replace("\n", " "),
            "price": round(float(self.faker.pydecimal(min_value=0.99, max_value=199.99, right_digits=2)), 2),
            "sku": self.faker.bothify(text="SKU-???").upper(),
            "category": self.faker.random_element(elements=["Electronics", "Clothing", "Books", "Home", "Sports"]),
            "in_stock": self.faker.boolean(chance_of_getting_true=80),
        }
        data.update(overrides)
        data["price"] = round(float(data["price"]), 2)
        return data

    def random_product_list(self, count: int = 5) -> List[Dict[str, Any]]:
        return [self.random_product() for _ in range(count)]

    # ── Price Utilities ───────────────────────────────────────────

    def price_list(self, count: int = 5, min_price: float = 0.99, max_price: float = 199.99) -> List[float]:
        return [
            round(float(self.faker.pydecimal(min_value=min_price, max_value=max_price, right_digits=2)), 2)
            for _ in range(count)
        ]

    def json(self, **overrides: Any) -> Dict[str, Any]:
        return self.random_product(**overrides)
