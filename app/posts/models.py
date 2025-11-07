from datetime import datetime, UTC
from typing import Optional
from enum import Enum
from app import db  

class CategoryEnum(Enum):
    news = "news"
    publication = "publication"
    tech = "tech"
    other = "other"

class Post(db.Model):
    __tablename__ = "posts"

    id: db.Mapped[int] = db.mapped_column(primary_key=True)
    title: db.Mapped[str] = db.mapped_column(db.String(150), nullable=False)
    content: db.Mapped[str] = db.mapped_column(db.Text, nullable=False)
    category: db.Mapped[CategoryEnum] = db.mapped_column(
        db.Enum(CategoryEnum), default=CategoryEnum.news
    )
    is_active: db.Mapped[bool] = db.mapped_column(default=True)
    posted: db.Mapped[datetime] = db.mapped_column(
        db.DateTime, default=lambda: datetime.now(UTC)
    )

    def __repr__(self) -> str:
        return f"<Post {self.id} - {self.title}>"
