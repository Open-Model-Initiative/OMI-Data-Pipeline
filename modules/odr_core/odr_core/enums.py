from enum import Enum


class ContentType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    VOICE = "voice"
    MUSIC = "music"
    TEXT = "text"


class ContentStatus(str, Enum):
    PENDING = "PENDING"
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    DELISTED = "DELISTED"


class ContentSourceType(str, Enum):
    URL = "url"
    PATH = "path"
    HUGGING_FACE = "hugging_face"


class ReportStatus(str, Enum):
    PENDING = "pending"
    REVIEWED = "reviewed"
    RESOLVED = "resolved"


class AnnotationSourceType(str, Enum):
    CONTENT_DESCRIPTION = "content_description"
    SPATIAL_ANALYSIS = "spatial_analysis"
    TAGS = "tags"
    OTHER = "other"


class ReportType(str, Enum):
    ILLEGAL_CONTENT = "illegal_content"
    MALICIOUS_ANNOTATION = "malicious_annotation"
    OTHER = "other"


class EmbeddingEngineType(str, Enum):
    IMAGE = "image"
    VIDEO = "video"
    VOICE = "voice"
    MUSIC = "music"
    TEXT = "text"


class UserType(str, Enum):
    user = "user"
    bot = "bot"
