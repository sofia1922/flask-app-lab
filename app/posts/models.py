from datetime import datetime, UTC
from enum import Enum
from app.users.models import User
from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CategoryEnum(Enum):
    news = "news"
    publication = "publication"
    tech = "tech"
    other = "other"

post_tags = db.Table(
    "post_tags",
    db.Column("post_id", db.Integer, db.ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tags.id"), primary_key=True)
)

class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(db.String(150), nullable=False)
    content: Mapped[str] = mapped_column(db.Text, nullable=False)
    category: Mapped[CategoryEnum] = mapped_column(
        db.Enum(CategoryEnum), 
        default=CategoryEnum.news
    )
    is_active: Mapped[bool] = mapped_column(default=True)
    posted: Mapped[datetime] = mapped_column(
        db.DateTime, default=lambda: datetime.now(UTC)
    )

    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="posts")

    tags: Mapped[list["Tag"]] = relationship(
        secondary=post_tags,
        back_populates="posts"
    )

    def __repr__(self):
        return f"<Post {self.id} - {self.title}>"


class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(50), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        secondary=post_tags,
        back_populates="tags"
    )

    def __repr__(self):
        return f"<Tag {self.name}>"
