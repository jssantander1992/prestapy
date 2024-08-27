from prestapy.prestashop_ep import PSEndPoint


def get_stocks(url, start_quantity=1, end_quantity=500):
    stock_availables_ep = PSEndPoint(
        base_url=url, endpoint='api/stock_availables')
    stock_params = {
        "display": "[id_product,quantity]",
        "filter[quantity]": f"[{start_quantity},{end_quantity}]"
    }
    stock_availables = stock_availables_ep.get_all(params=stock_params)[
        "stock_availables"]
    return {int(d['id_product']): d['quantity'] for d in stock_availables}
