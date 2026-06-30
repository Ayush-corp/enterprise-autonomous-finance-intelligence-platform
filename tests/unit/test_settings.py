from app.config import settings


def test_settings_app_name():
    """Test that app_name is configured"""
    assert settings.app_name is not None
    assert isinstance(settings.app_name, str)


def test_settings_environment():
    """Test that environment is configured"""
    assert settings.environment is not None


def test_settings_llm_provider():
    """Test that llm_provider is configured"""
    assert settings.llm_provider is not None


def test_settings_llm_model():
    """Test that llm_model is configured"""
    assert settings.llm_model is not None


def test_settings_market_provider():
    """Test that market_provider is configured"""
    assert settings.market_provider is not None
