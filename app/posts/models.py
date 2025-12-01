from datetime import datetime, UTC
import enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, Table, Column, Integer, ForeignKey, String, Text, Boolean, DateTime
from app import db


class CategoryEnum(enum.Enum):
    news = "news"
    publication = "publication"
    tech = "tech"
    other = "other"


post_tags = Table(
    "post_tags",
    db.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    category: Mapped[CategoryEnum] = mapped_column(
        Enum(CategoryEnum, name="category_enum"),  
        default=CategoryEnum.news,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    posted: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="posts")

    tags: Mapped[list["Tag"]] = relationship(
        secondary=post_tags,
        back_populates="posts",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Post {self.id} - {self.title}>"


class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        secondary=post_tags,
        back_populates="tags",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"
