from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, DateTime
from flask_login import UserMixin
from datetime import datetime
from app import db, bcrypt


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    image: Mapped[str] = mapped_column(
        String(200),
        nullable=True,
        default="profile_default.jpg"
    )

    about_me: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    last_seen: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        default=datetime.utcnow
    )

    posts: Mapped[List["Post"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def set_password(self, raw_password: str) -> None:
        self.password = (
            bcrypt.generate_password_hash(raw_password).decode("utf-8")
        )

    def check_password(self, raw_password: str) -> bool:
        return bcrypt.check_password_hash(self.password, raw_password)

    def __repr__(self) -> str:
        return f"<User {self.username}>"
