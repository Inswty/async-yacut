from datetime import datetime

from . import db
from .constants import MAX_ORIGINAL_LINK_LENGTH, MAX_SHORT_LINK_LENGTH


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LINK_LENGTH), nullable=False)
    short = db.Column(db.String(MAX_SHORT_LINK_LENGTH),
                      unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Сериализация объекта в словарь для API."""
        return {
            'id': self.id,
            'original': self.original,
            'short': self.short,
            'timestamp': self.timestamp.isoformat()
        }
