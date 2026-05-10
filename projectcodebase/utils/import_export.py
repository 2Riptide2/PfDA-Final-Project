import json
from services.trait_service import create_trait

def import_traits(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)

    for trait in data["traits"]:
        create_trait(
            trait["name"],
            trait["category"],
            trait.get("description", ""),
            trait["tags"]
        )


def export_traits(file_path, traits):
    data = {
        "traits": [
            {
                "name": t.name,
                "category": t.category,
                "description": t.description,
                "tags": [tt.tag.name for tt in t.tags]
            }
            for t in traits
        ]
    }

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)