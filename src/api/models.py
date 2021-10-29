import uuid

from sqlalchemy.dialects.postgresql import UUID

from src import db


class Url(db.Model):

    __tablename__ = 'urls'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    target_url = db.Column(db.String(2048))
    custom_name = db.Column(db.String(64), unique=True)
