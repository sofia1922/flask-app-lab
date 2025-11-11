from datetime import datetime
from app import db
from sqlalchemy import String, Integer, Numeric, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Category(db.Model):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Category {self.name}>"

class Product(db.Model):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")

    def __repr__(self):
        return f"<Product {self.name} (${self.price})>"
