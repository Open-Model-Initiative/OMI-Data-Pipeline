from sqlalchemy import Column, Integer, String, Boolean
from odr_core.models.base import Base


class FeatureToggle(Base):
    __tablename__ = 'feature_toggles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    feature_name = Column(String(255), unique=True, nullable=False)
    is_enabled = Column(Boolean, nullable=False)
    default_state = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"<FeatureToggle(id={self.id}, feature_name={self.feature_name}, is_enabled={self.is_enabled}, default_state={self.default_state})>"
