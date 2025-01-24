def check_quantity(order) -> bool:
    return all(map(lambda x: x.product.quntity >= x.quantity, order.product_orders.all()))