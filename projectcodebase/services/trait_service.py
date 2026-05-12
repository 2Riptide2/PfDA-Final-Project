from database import SessionLocal
from models import Trait, Tag, TraitTag

def create_trait(name, category, description, tag_names):
    session = SessionLocal()

    trait = Trait(name=name, category=category, description=description)
    session.add(trait)
    session.commit()

    for tag_name in tag_names:
        tag = session.query(Tag).filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            session.add(tag)
            session.commit()

        session.add(TraitTag(trait_id=trait.id, tag_id=tag.id))

    session.commit()
    session.close()


def get_traits(search_text=None, include_tags=None):
    session = SessionLocal()
    query = session.query(Trait)

    # 🔍 Name search
    if search_text:
        query = query.filter(Trait.name.ilike(f"%{search_text}%"))

    # 🏷 Tag filtering
    if include_tags:
        query = query.join(TraitTag).join(Tag).filter(Tag.name.in_(include_tags))

    traits = query.all()
    session.close()
    return traits

def get_trait_by_id(trait_id):
    session = SessionLocal()
    trait = session.query(Trait).filter_by(id=trait_id).first()
    session.close()
    return trait


def update_trait(trait_id, name, category, description, tag_names):
    session = SessionLocal()

    trait = session.query(Trait).filter_by(id=trait_id).first()
    if not trait:
        session.close()
        return

    trait.name = name
    trait.category = category
    trait.description = description

    # Remove old tags
    session.query(TraitTag).filter_by(trait_id=trait_id).delete()

    # Add new tags
    for tag_name in tag_names:
        tag = session.query(Tag).filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            session.add(tag)
            session.commit()

        session.add(TraitTag(trait_id=trait_id, tag_id=tag.id))

    session.commit()
    session.close()


def get_trait_tags(trait):
    return [tt.tag.name for tt in trait.tags]

def delete_trait(trait_id):
    session = SessionLocal()

    # Delete tag links first (important for DB integrity)
    session.query(TraitTag).filter_by(trait_id=trait_id).delete()

    # Delete the trait itself
    session.query(Trait).filter_by(id=trait_id).delete()

    session.commit()
    session.close()