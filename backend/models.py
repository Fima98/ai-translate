from sqlalchemy import Column, Integer, String, Text, JSON, ARRAY, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class TranslationTask(Base):
    __tablename__ = "translation_tasks"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)  # Використовуйте 'content' як поле для тексту
    languages = Column(ARRAY(String), nullable=False)
    status = Column(String, default="pending", nullable=False)
    translations = Column(JSON, nullable=False, default={})
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),  # Це правильний спосіб
    )
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="tasks")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()"),
    )

    tasks = relationship("TranslationTask", back_populates="owner", cascade="all, delete-orphan")
