from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Trait(Base):
    __tablename__ = "traits"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    category = Column(String)
    description = Column(String)

    tags = relationship("TraitTag", back_populates="trait")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    traits = relationship("TraitTag", back_populates="tag")


class TraitTag(Base):
    __tablename__ = "trait_tags"

    id = Column(Integer, primary_key=True)
    trait_id = Column(Integer, ForeignKey("traits.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))

    trait = relationship("Trait", back_populates="tags")
    tag = relationship("Tag", back_populates="traits")


class Character(Base):
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    traits = relationship("CharacterTrait", back_populates="character")


class CharacterTrait(Base):
    __tablename__ = "character_traits"

    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    trait_id = Column(Integer, ForeignKey("traits.id"))

    character = relationship("Character", back_populates="traits")