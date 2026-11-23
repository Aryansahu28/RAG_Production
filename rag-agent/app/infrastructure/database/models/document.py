import enum
import uuid

from datetime import datetime

from sqlalchemy import BigInteger,CheckConstraint,DateTime,Enum,Index,JSON,String,Text,Uuid,func

from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base

class DocumentStatus(str,enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    values_callable=lambda enum_cls: [
    member.value for member in enum_cls]

class Document(Base):

    __tablename__ = "documents"

    __table_args__ = (
    CheckConstraint(
            "file_size_bytes >= 0",
            name="file_size_non_negative",
        ),
    Index("ix_documents_status_created", "status", "created_at"),
    Index("ix_documents_checksum", "checksum_sha256"),
    )

    #Primary Key
    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True),primary_key=True,default=uuid.uuid4)

     # File Information
    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    file_size_bytes: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )

    checksum_sha256: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    storage_key: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    # Processing Information
    status: Mapped[DocumentStatus] = mapped_column(
    Enum(
        DocumentStatus,
        name="document_status",
        native_enum=False,
        create_constraint=True,
        length=20,
        values_callable=lambda enum_cls: [
            member.value for member in enum_cls
        ]
    ),
    default=DocumentStatus.PENDING,
    nullable=False
)

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # Additional Metadata
    metadata_json: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True,
    )

    # Timestamps (UTC convention)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.current_timestamp(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
        nullable=False,
    )
