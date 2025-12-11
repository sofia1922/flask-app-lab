from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime
from datetime import datetime
from app import db


class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    recipes: Mapped[list["Recipe"]] = relationship(
        "Recipe",
        back_populates="category",
        cascade="all, delete"
    )

    def __repr__(self):
        return f"<Category {self.name}>"


class Recipe(db.Model):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)

    ingredients: Mapped[str] = mapped_column(Text, nullable=False)
    instructions: Mapped[str] = mapped_column(Text, nullable=False)

    cook_time: Mapped[int] = mapped_column(Integer, nullable=False)

    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False
    )
    category: Mapped["Category"] = relationship("Category", back_populates="recipes")
    category_rel = relationship("Category", back_populates="recipes")

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    category = relationship("Category", back_populates="recipes")
    user = relationship("User", back_populates="recipes")

    image: Mapped[str] = mapped_column(
        String(255), nullable=True, default="default_recipe.jpg"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Recipe {self.title}>"
