from unittest.mock import AsyncMock, Mock

import pytest

import discord_habit_tracker.main as main



@pytest.mark.asyncio
async def test_main_wires_application_dependencies(monkeypatch):
    # Arrange
    mock_config = Mock()
    mock_config.bot_token = "test-token"
    mock_config.tracked_user_id = 12345

    mock_repository = Mock()
    mock_qualification_service = Mock()
    mock_listener = Mock()
    mock_gateway = Mock()

    mock_gateway.start = AsyncMock()

    config_mock = Mock(return_value=mock_config)
    activity_repository_mock = Mock(return_value=mock_repository)
    qualification_service_mock = Mock(return_value=mock_qualification_service)
    listener_mock = Mock(return_value=mock_listener)
    gateway_mock = Mock(return_value=mock_gateway)

    monkeypatch.setattr(main, "Config", config_mock)
    monkeypatch.setattr(main, "ActivityRepository", activity_repository_mock)
    monkeypatch.setattr(main, "ActivityQualificationService", qualification_service_mock)
    monkeypatch.setattr(main, "EventListener", listener_mock)
    monkeypatch.setattr(main, "DiscordGateway", gateway_mock)

    # Act
    await main.main()

    # Assert
    config_mock.assert_called_once_with()

    activity_repository_mock.assert_called_once_with()
    qualification_service_mock.assert_called_once_with()

    listener_mock.assert_called_once_with(
        mock_repository,
        12345,
        mock_qualification_service,
    )

    gateway_mock.assert_called_once_with(
        "test-token",
        mock_listener.handle_message,
    )

    mock_gateway.start.assert_awaited_once()
