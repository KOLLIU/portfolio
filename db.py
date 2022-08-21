from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, Text

Base = declarative_base()


class CityDB(Base):
    __tablename__ = "cities"

    number = Column(Integer, primary_key=True, unique=True)
    title = Column(Text, primary_key=True, unique=True)
    title_href = Column(Text)
    city_district = Column(Text)
    city_district_href = Column(Text)
    okato = Column(Integer)
    population = Column(Integer)
    foundation = Column(Text)
    city_status = Column(Integer)
    emblem_href = Column(Text)
