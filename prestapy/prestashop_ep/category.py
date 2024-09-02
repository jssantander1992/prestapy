from .base import PsWebService, EndPointEnum


class Category(PsWebService):
    def __init__(self, base_url, api_key=None):
        super().__init__(EndPointEnum.CATEGORIES, base_url, api_key)

    @staticmethod
    def append_parent_categories(categories, category):
        parent_id = category[1]['id_parent']
        cat_tree = [str(category[0])]

        if category[0] == 1:
            return category

        while parent_id != "1":
            for potential_id, potential_parent in categories.items():
                if int(potential_id) == int(parent_id):
                    cat_tree.append(str(potential_id))
                    parent_id = potential_parent['id_parent']
                    break
        new_category = category[1]

        new_category['cat_tree'] = ",".join(cat_tree)

        return category[0], new_category

    def get_all(self, **kwargs):
        params = kwargs.get('params', {})
        categories_params = {
            "display": "[id, name, id_parent, description, h1_title, link_rewrite, meta_title]",
            **params
        }
        categories_data = super().get_all(
            params=categories_params
        )["categories"]

        return {
            d['id']: {
                "name": d['name'],
                "id_parent": d['id_parent'],
                "description": d['description'],
                "h1_title": d["h1_title"],
                "link_rewrite": d["link_rewrite"],
                "meta_title": d["meta_title"]
            } for d in categories_data}
