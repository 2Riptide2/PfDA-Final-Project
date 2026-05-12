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


def get_traits(include_tags=None, exclude_tags=None):
    session = SessionLocal()
    query = session.query(Trait)

    if include_tags:
        query = query.join(TraitTag).join(Tag).filter(Tag.name.in_(include_tags))

    traits = query.all()

    if exclude_tags:
        filtered = []
        for trait in traits:
            trait_tag_names = [tt.tag.name for tt in trait.tags]
            if not any(tag in trait_tag_names for tag in exclude_tags):
                filtered.append(trait)
        traits = filtered

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