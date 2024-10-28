from Structure_2.FileIndexerNoId import FileIndexerNoId, savefile_to_indexer_noid, add_file_data_to_indexer

def prettify_recipe_dict(recipes_data: dict) -> str:
    """Formats the recipe list for printing."""

    item_name = recipes_data.get("item", "Unknown Item")
    recipes_dict = recipes_data.get("recipes", {})
    count = recipes_data.get("count", 0)
    strict = recipes_data.get("sensitive", False)

    recipe_count_str = f"{count} recipe{'s' if count != 1 else ''} found" if count > 0 else "No recipes found"
    case_str = "exact" if strict else "any"
    result_lines = [f"{recipe_count_str} for '{item_name}' ({case_str} casing):"]

    for item, recipe_list in recipes_dict.items():
        for ing1, ing2 in recipe_list:
            result_lines.append(f"{ing1} + {ing2} = {item}")

    return "\n".join(result_lines)


def prettify_recipe_list(recipes: list) -> str:
    """Formats the recipe list for printing."""
    return '\n'.join([f"{ing1} + {ing2} => {result}" for ing1, ing2, result in recipes])

# Put your actual file here
indexer = savefile_to_indexer_noid(r"file_1.json", use_emojis=True)
add_file_data_to_indexer(r"file_2.json", indexer)
print("Number of elements (most generous total possible):", len(indexer.elements))
print("Number of elements (normalised, most generous total possible):", len(indexer.elements_normalised))
#recipes = indexer.get_recipes_list("100%")
recipes = indexer.get_recipes_dict("100%")
print(prettify_recipe_dict(recipes))
