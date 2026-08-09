from dataclasses import dataclass


@dataclass(slots=True)
class LineItem:
    sku: str
    unit_price: float
    quantity: int


def calculate_order_total(
    items: list[LineItem],
    discount_code: str | None = None,
    tax_rate: float = 0.20,
) -> float:
    """
    Calculate the order total.

    Known issues for teaching purposes:
    - validation is incomplete
    - discount handling is simplistic
    - error messages are weak
    """
    subtotal = sum(item.unit_price * item.quantity for item in items)

    if discount_code == "SAVE10":
        subtotal *= 0.90
    elif discount_code == "VIP25":
        subtotal *= 0.75

    tax = subtotal * tax_rate
    return round(subtotal + tax, 2)
