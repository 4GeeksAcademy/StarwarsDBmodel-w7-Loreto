from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

user_planet_favorites: Table = db.Table(
    "favorite_planets",
    db.Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    db.Column("planet_id", Integer, ForeignKey(
        "planets.id"), primary_key=True),
)

user_character_favorites: Table = db.Table(
    "favorite_characters",
    db.Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    db.Column("character_id", Integer, ForeignKey(
        "characters.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True)

    # N:M
    favorite_planets: Mapped[List["Planets"]] = relationship(
        "Planets",
        secondary=user_planet_favorites,
        back_populates="fans",
    )
    favorite_people: Mapped[List["People"]] = relationship(
        "People",
        secondary=user_character_favorites,
        back_populates="fans",
    )

    def serialize(self):
        return {"id": self.id, "email": self.email}


class Planets(db.Model):
    __tablename__ = "planets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    population: Mapped[int | None] = mapped_column(Integer, nullable=True)
    terrain: Mapped[str | None] = mapped_column(String(120), nullable=True)
    rotation: Mapped[str | None] = mapped_column(String(120), nullable=True)
    climate: Mapped[str | None] = mapped_column(String(120), nullable=True)
    diameter: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # lado inverso de N:M
    fans: Mapped[List["User"]] = relationship(
        "User",
        secondary=user_planet_favorites,
        back_populates="favorite_planets",
    )

    def serialize(self):
        return {"id": self.id, "name": self.name}

    def serialize_all_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
            "rotation": self.rotation,
            "climate": self.climate,
            "diameter": self.diameter,
        }


class People(db.Model):
    __tablename__ = "characters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    gender: Mapped[str | None] = mapped_column(String(120), nullable=True)
    hair: Mapped[str | None] = mapped_column(String(120), nullable=True)
    eye_color: Mapped[str | None] = mapped_column(String(120), nullable=True)
    skin_color: Mapped[str | None] = mapped_column(String(120), nullable=True)
    day_of_birth: Mapped[str | None] = mapped_column(
        String(120), nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # lado inverso de N:M
    fans: Mapped[List["User"]] = relationship(
        "User",
        secondary=user_character_favorites,
        back_populates="favorite_people",
    )

    def serialize(self):
        return {"id": self.id, "name": self.name}

    def serialize_all_data(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair": self.hair,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color,
            "day_of_birth": self.day_of_birth,
            "height": self.height,
        }
