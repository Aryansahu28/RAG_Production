
import enum
import uuid

from datetime import datetime

from sqlalchemy import DateTime,Enum,ForeignKey,Index,Integer,Text,Uuid,func

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

class MessageRole(str, enum.Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    values_callable=lambda enum_cls: [
        member.value for member in enum_cls
    ]

class Message(Base):

    __tablename__ = "messages"

    __table_args__ = (
        Index(
            "ix_messages_conversation_created",
            "conversation_id",
            "created_at",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True),primary_key=True,default=uuid.uuid4,)

    conversation_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True),ForeignKey("conversations.id",ondelete="CASCADE",),nullable=False,)

    role: Mapped[MessageRole] = mapped_column(
        Enum(
            MessageRole,
            name="message_role",
            native_enum=False,
            create_constraint=True,
            length=20,
            values_callable=lambda enum_cls: [
                member.value for member in enum_cls    ]
        ),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(Text,nullable=False)

    token_count: Mapped[int | None] = mapped_column(Integer,nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False),server_default=func.current_timestamp(),nullable=False,)

    conversation: Mapped["Conversation"] = relationship(back_populates="messages",lazy="raise")