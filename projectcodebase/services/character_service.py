# services/character_service.py

from database import SessionLocal
from models import Character, CharacterTrait, Trait

def create_character(name):
    session = SessionLocal()
    character = Character(name=name)
    session.add(character)
    session.commit()
    session.refresh(character)
    session.close()
    return character


def add_trait_to_character(character_id, trait_id):
    session = SessionLocal()

    link = CharacterTrait(
        character_id=character_id,
        trait_id=trait_id
    )
    session.add(link)
    session.commit()
    session.close()


def get_character(character_id):
    session = SessionLocal()
    character = session.query(Character).filter_by(id=character_id).first()
    session.close()
    return character


def get_all_characters():
    session = SessionLocal()
    characters = session.query(Character).all()
    session.close()
    return characters


def get_character_traits(character_id):
    session = SessionLocal()

    links = session.query(CharacterTrait).filter_by(character_id=character_id).all()

    traits = []
    for link in links:
        trait = session.query(Trait).filter_by(id=link.trait_id).first()
        if trait:
            traits.append(trait)

    session.close()
    return traits