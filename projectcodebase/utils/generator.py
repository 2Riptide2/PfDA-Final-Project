import random
from services.trait_service import get_traits

REQUIRED_CATEGORIES = [
    "personality",
    "physical",
    "eye",
    "hair"
]

def generate_character(include_tags=None):
    traits = get_traits(include_tags=include_tags)

    character = {}

    for category in REQUIRED_CATEGORIES:
        category_traits = [t for t in traits if t.category == category]
        if category_traits:
            character[category] = random.choice(category_traits).name

    return character