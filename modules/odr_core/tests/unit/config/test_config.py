from odr_core.config import settings


def test_settings():
    assert settings.get_db_url().startswith("postgresql://")
    assert settings.API_V1_STR == "/api/v1"
    assert settings.PROJECT_NAME == "OMI-DataModel"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
