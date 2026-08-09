from retail_demo.pricing import LineItem, calculate_order_total


def test_calculate_order_total_without_discount():
    items = [
        LineItem(sku="A-1", unit_price=10.0, quantity=2),
        LineItem(sku="B-1", unit_price=5.0, quantity=1),
    ]
    assert calculate_order_total(items, tax_rate=0.20) == 30.0


def test_calculate_order_total_with_save10_discount():
    items = [LineItem(sku="A-1", unit_price=100.0, quantity=1)]
    assert calculate_order_total(items, discount_code="SAVE10", tax_rate=0.10) == 99.0
