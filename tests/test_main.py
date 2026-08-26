from unittest.mock import AsyncMock, Mock
import discord_habit_tracker.main as main


async def test_main_creates_gateway_with_config_token(monkeypatch):
    """Test that main creates the Gateway using the configured token."""

    mock_config = Mock()
    mock_config.bot_token = "test-token"

    mock_gateway = Mock()
    mock_gateway.start = AsyncMock()

    monkeypatch.setattr(main, "Config", Mock(return_value=mock_config))
    monkeypatch.setattr(main, "DiscordGateway", Mock(return_value=mock_gateway))

    await main.main()

    main.DiscordGateway.assert_called_once_with("test-token")
    mock_gateway.start.assert_awaited_once()
