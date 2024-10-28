import json
import os
from typing import TypedDict, List, Tuple, Dict, Set, Optional

# Define a TypedDict for the element structure
class ElementData(TypedDict, total=False):
    emoji: str  # The emoji associated with the element
    recipes: List[Tuple[str, str]]  # List of tuples of ingredients


class FileIndexerNoId:
    elements: Dict[str, ElementData]  # Map case-sensitive element string to dictionary containing emoji and all recipes (see ElementData)
    elements_normalised: Dict[str, Set[str]]  # Map case-insensitive element string to list of all encountered casing variants which can then be used to lookup in self.elements dictionary
    recipes_fwd: Dict[Tuple[str, str],  str]  # Map case-insensitive ingredients to case-sensitive result.
    conflicts: Dict[str, Set[str]]  # Store conflicting emojis, mostly a curiosity thing.
    use_emojis: bool  # Flag specifying whether to care about emojis or just discard them. Default is False.

    def __init__(self, initial_items: List | Dict, use_emojis: bool = False):
        # Initialise with blank dictionaries for storage
        self.elements = {}
        self.elements_normalised = {}
        self.recipes_fwd = {}
        self.conflicts = {}

        # Set variables that impact the behaviour
        self.use_emojis = use_emojis

        # Add initial items
        self.add_items(initial_items)

    def add_items(self, items: List | Dict):
        """Wrapper (is that the right word?) to add all the items from a file, in either dictionary or list form
        in a single call. """
        for item in items:
            self.add_item(item)

    def add_item(self, item):
        """Public method for adding items to the indexer. Responsible for handling formatting input to _add_item
        as well as assigning the default '⬜' if emoji is unspecified, and we care about them. """
        if isinstance(item, str):
            # Assume here that it is just a string of the name.
            if self.use_emojis:
                self._add_item(item_name=item, emoji='⬜')
            else:
                self._add_item(item_name=item)
        elif isinstance(item, dict):
            item_name = item.get("text")
            # Name is critical, cannot have it missing.
            if not item_name:
                raise ValueError("Dictionary must contain a 'text' key with the item name.")

            if self.use_emojis:
                self._add_item(item_name=item_name, emoji=item.get("emoji",'⬜'))

            else:
                self._add_item(item_name=item_name)

        else:
            raise TypeError("Item must be either a string or a dictionary.")

    def _add_item(self, item_name: str, emoji: Optional[str] = None):
        """
        Add an item to the indexer.

        Args:
            item_name (str): The name of the element.
            emoji (Optional[str]): The emoji associated with the element. Defaults to None.

        Notes:
            If emoji is not None, we assume that we care about emojis.
        """

        # Normalised (case-insensitive) name for use for lookup of recipes.
        normalized_name = item_name.lower()
        if normalized_name not in self.elements_normalised:
            self.elements_normalised[normalized_name] = set()
        self.elements_normalised[normalized_name].add(item_name)  # Safe in all cases since duplicates are removed in sets.

        # Purpose of this block is two-fold:
        # 1. If data already exists, we really do not want to overwrite the recipes, hence we must return
        # 2. Check for emoji conflicts (only possible if data already exists)
        existing_data = self.elements.get(item_name)  # Data or None if it doesn't exist.
        # This logic MUST be improved, I really hate the way the default emoji logic is working here.
        if existing_data:
            existing_emoji = existing_data.get("emoji")
            if existing_emoji != emoji and emoji and emoji != '⬜':  # Required in order for conflict to trigger, no conflict if default emoji passed.
                if existing_emoji == '⬜':  # Override, assume default.
                    self.elements[item_name]["emoji"]= emoji
                else:  # Conflict
                    # Standard dictionary logic, although slight caveat in that we initialise the set with an item already since I want to note down the original too, which would be missed if I didn't do this.
                    #print(f"Conflict: original emoji: {existing_emoji}, claimed emoji: {emoji}")
                    if item_name not in self.conflicts:
                        self.conflicts[item_name] = {existing_emoji}
                    self.conflicts[item_name].add(emoji)
                    #print(self.conflicts[item_name])

            return   # As promised by purpose 1 of the check (don't overwrite recipes).

        # If no existing data, initialize new element data
        element_data = {"recipes": []}  # Initialise as empty list since no recipes yet.
        if emoji:
            element_data["emoji"] = emoji

        self.elements[item_name] = element_data  # Add to the data structure

    def add_recipe(self, ing1: Dict | str, ing2: Dict | str, result: Dict | str):
        """
        Add a recipe to the indexer.

        Args:
            ing1: The first ingredient, in either text or dictionary form
            ing2: The second ingredient, in either text or dictionary form
            result: The result in either text or dictionary form

        Notes:
            The inputs need not be of same type, normalise_input handles this
            The recipe that is set will be case-sensitive result with case-insensitive ingredients
            All items go through add_item to ensure parity is maintained
            Conflicting recipes will raise an error, may want to modify this behaviour, especially if your save is
            impacted by bugs or modified or otherwise.
        """

        # Function to normalize input to casing and ensure parity
        def normalise_input(ingredient) -> str:
            if isinstance(ingredient, dict):
                # Extract the name and emoji if present
                name = ingredient.get("text")
                self.add_item(ingredient)
                return name.lower()  # Return the normalised name for recipe tracking
            elif isinstance(ingredient, str):
                self.add_item(ingredient)  # Directly add the item if it's a string
                return ingredient.lower()  # Return the normalised name
            else:
                raise ValueError("Ingredient must be a string or a dictionary.")

        normalised_ing1 = normalise_input(ing1)
        normalised_ing2= normalise_input(ing2)
        normalise_input(result)  # Don't need normalised name here.

        ing_pair = tuple(sorted((normalised_ing1, normalised_ing2)))
        if ing_pair in self.recipes_fwd:
            existing_result = self.recipes_fwd[ing_pair]
            if existing_result != result:
                raise ValueError(f"Conflicting recipe detected! {ing_pair} -> {existing_result} but also {ing_pair} -> {result}, aborting....")

        else:
            self.recipes_fwd[ing_pair] = result
            self.elements[result]["recipes"].append(ing_pair)

    def get_recipes_list(self, item_name: str, strict=False):
        """
        Get the recipes of a given element (formatted as a list), with options for normalisation.

        Args:
            item_name: the name of the item, given as a string. Note: maybe I will let it be dictionary one day.
            strict: whether to care about the casing of the result or not, default is False.
        Notes:
            May not end up using this method in favour of a dictionary instead.
        """

        if strict:
            item = self.elements.get(item_name)
            if not item:
                print(f"Item with exact casing '{item_name}' not found")
                return []
            else:
                recipes = item.get("recipes")
                if not recipes:
                    print(f"No recipes found for exact casing '{item_name}'")
                    return []
                else:
                    return recipes

        else:
            normalised_name = item_name.lower()
            item_variants = self.elements_normalised.get(normalised_name)
            if item_variants:
                total_recipes = []
                for variant in item_variants:
                    variant_recipes = self.elements.get(variant, {}).get("recipes", [])
                    total_recipes.extend(variant_recipes)
                if not total_recipes:
                    print(f"No recipes for item with normalised case '{normalised_name}' found")
                return total_recipes
            else:
                print(f"No items with normalised case '{normalised_name}' found")
                return []

    def get_recipes_dict(self, item_name: str, strict=False):
        """
        Get the recipes of a given element (formatted as a dictionary), with options for normalisation.

        Args:
            item_name: the name of the item, given as a string. Note: maybe I will let it be dictionary one day.
            strict: whether to care about the casing of the result or not, default is False.
        Notes:
            Use this one preferably, is compatible with prettify function (which is currently located in main, not sure if it will stay there)
        """

        # The dictionary that will store the recipe info to export
        recipes_dict = {"item": item_name, "recipes": {}, "count": 0, "sensitive": strict}

        # If strict, only return recipes for the exact casing
        if strict:
            element_data = self.elements.get(item_name)
            if element_data:
                recipes = element_data.get("recipes")
                if recipes:
                    recipes_dict["recipes"][item_name] = recipes  # Note: This is a pointer, you *may* want to make it a copy or a deepcopy since technically it is a list of tuples
                    recipes_dict["count"] += len(recipes)  # Update length
                else:
                    print(f"No recipes found for exact casing '{item_name}', but the item exists somewhere in the savefile.")
            else:
                print(f"Item with exact casing '{item_name}' not found")

        # If not strict, gather recipes for all casing variants
        else:
            normalised_name = item_name.lower()
            item_variants = self.elements_normalised.get(normalised_name)
            if item_variants:
                for variant in item_variants:
                    variant_recipes = self.elements.get(variant, {}).get("recipes", [])
                    recipes_dict["recipes"][variant] = variant_recipes
                    recipes_dict["count"] += len(variant_recipes)
                if not recipes_dict["count"]:
                    print(f"No recipes for items with normalised case '{normalised_name}' found")
            else:
                print(f"No items with normalised case '{normalised_name}' found")

        return recipes_dict




def savefile_to_indexer_noid(file_path: str, use_emojis=False) -> FileIndexerNoId:
    """Turns the file path you give it into an indexer instance with the initial state loaded. Honestly I don't know
    why I did it like this, or how hard it would be to change.
    """

    elements_raw, recipes_raw = get_file_data(file_path)

    indexer = FileIndexerNoId(elements_raw, use_emojis=use_emojis)

    for recipe_result, recipes in recipes_raw.items():
        for ing1, ing2 in recipes:
            indexer.add_recipe(ing1, ing2, recipe_result)

    return indexer


def get_file_data(file_path: str) -> Tuple[List, Dict]:
    """Single function to get important file data and return it, including elements and recipes.
    Raises errors if these are not present or if the savefile is specified. Up to calling function to catch these.
    Also note, it does not do anything with this data, it just gives it to you. This is so you don't have to
    do it yourself everytime.
    """

    name, ext = os.path.splitext(file_path)
    if ext != ".json":
        raise ValueError(f"Improper savefile specified. Expected type '.json', but got type '{ext}'")

    with open(file_path, 'r', encoding='utf-8') as f:
        save_raw = json.load(f)

    # Check for required keys and that they are a list or a dictionary
    elements_raw = save_raw.get("elements")
    if not isinstance(elements_raw, list):
        raise ValueError("Savefile does not contain a valid 'elements' list, aborting...")

    recipes_raw = save_raw.get("recipes")
    if not isinstance(recipes_raw, dict):  # Change here to check for dictionary
        raise ValueError("Savefile does not contain a valid 'recipes' dictionary, aborting...")

    return elements_raw, recipes_raw


def add_file_data_to_indexer(file_path: str, indexer: FileIndexerNoId) -> FileIndexerNoId:
    """Add file data from file specified by file_path to indexer specified by indexer.
    I really don't know if I should make it return the indexer or not.
    """

    # Technically duplicate code here, not sure what to do.
    elements_raw, recipes_raw = get_file_data(file_path)
    indexer.add_items(elements_raw)
    for recipe_result, recipes in recipes_raw.items():
        for ing1, ing2 in recipes:
            indexer.add_recipe(ing1, ing2, recipe_result)

    return indexer
