from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///characters.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def init_db():
    from models import Trait, Tag, TraitTag, Character, CharacterTrait
    Base.metadata.create_all(bind=engine)