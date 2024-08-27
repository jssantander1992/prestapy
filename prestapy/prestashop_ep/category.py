from . import PSEndPoint


def get_categories(url):
    categories_ep = PSEndPoint(base_url=url, endpoint='api/categories')
    categories_params = {
        "display": "[id, name, id_parent, description, h1_title, link_rewrite, meta_title]"
    }
    categories_data = categories_ep.get_all(
        params=categories_params)["categories"]
    # categories = [catgory_json_2_category(category) for category in categories_data]

    return {
        d['id']: {
            "name": d['name'],
            "id_parent": d['id_parent'],
            "description": d['description'],
            "h1_title": d["h1_title"],
            "link_rewrite": d["link_rewrite"],
            "meta_title": d["meta_title"]
        } for d in categories_data}


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