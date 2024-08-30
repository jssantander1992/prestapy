from prestapy.prestashop_ep import PsWebService


class Stock(PsWebService):
    def __init__(self, base_url, api_key=None):
        super().__init__(PsWebService.EndPointEnum.STOCK_AVAILABLES, base_url, api_key)

    def stock_range(self, start_quantity=1, end_quantity=1000):
        stock_params = {
            "display": "[id_product,quantity]",
            "filter[quantity]": f"[{start_quantity},{end_quantity}]"
        }

        stock_available = super().get_all(params=stock_params).get("stock_availables", [])

        return {int(d['id_product']): d['quantity'] for d in stock_available}
