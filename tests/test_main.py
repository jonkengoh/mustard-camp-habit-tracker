from unittest.mock import AsyncMock, Mock

import discord_habit_tracker.main as main


async def test_main_wires_application_dependencies(monkeypatch):
    # Arrange
    mock_config = Mock()
    mock_config.bot_token = "test-token"
    mock_config.tracked_user_ids = {12345}
    mock_config.tracked_user_timezone = "America/Chicago"

    mock_repository = Mock()
    mock_qualification_service = Mock()
    mock_date_resolver = Mock()
    mock_listener = Mock()
    mock_streak_service = Mock()
    mock_stats_service = Mock()
    mock_streak_command = Mock()
    mock_gateway = Mock()

    mock_gateway.start = AsyncMock()

    config_mock = Mock(return_value=mock_config)
    sqlite_activity_repository_mock = Mock(return_value=mock_repository)
    qualification_service_mock = Mock(return_value=mock_qualification_service)
    date_resolver_mock = Mock(return_value=mock_date_resolver)
    listener_mock = Mock(return_value=mock_listener)
    streak_service_mock = Mock(return_value=mock_streak_service)
    activity_stats_service_mock = Mock(return_value=mock_stats_service)
    streak_command_mock = Mock(return_value=mock_streak_command)
    gateway_mock = Mock(return_value=mock_gateway)

    monkeypatch.setattr(main, "Config", config_mock)
    monkeypatch.setattr(
        main,
        "SQLiteActivityRepository",
        sqlite_activity_repository_mock,
    )
    monkeypatch.setattr(
        main,
        "ActivityQualificationService",
        qualification_service_mock,
    )
    monkeypatch.setattr(main, "ActivityDateResolver", date_resolver_mock)
    monkeypatch.setattr(main, "EventListener", listener_mock)
    monkeypatch.setattr(main, "StreakService", streak_service_mock)
    monkeypatch.setattr(
        main,
        "ActivityStatsService",
        activity_stats_service_mock,
    )
    monkeypatch.setattr(main, "StreakCommand", streak_command_mock)
    monkeypatch.setattr(main, "DiscordGateway", gateway_mock)

    # Act
    await main.main()

    # Assert
    config_mock.assert_called_once_with()

    sqlite_activity_repository_mock.assert_called_once_with(
        "data/activity_tracker.db"
    )
    qualification_service_mock.assert_called_once_with()
    date_resolver_mock.assert_called_once_with()

    listener_mock.assert_called_once_with(
        mock_repository,
        {12345},
        mock_qualification_service,
        mock_date_resolver,
        "America/Chicago",
    )

    streak_service_mock.assert_called_once_with()

    activity_stats_service_mock.assert_called_once_with(
        mock_repository,
        mock_streak_service,
    )

    streak_command_mock.assert_called_once_with(
        mock_stats_service,
    )

    gateway_mock.assert_called_once_with(
        "test-token",
        mock_listener.handle_message,
        mock_streak_command,
        "America/Chicago",
    )

    mock_gateway.start.assert_awaited_once()


async def test_main_closes_repository_when_gateway_stops(monkeypatch):
    # Arrange
    mock_config = Mock()
    mock_config.bot_token = "test-token"
    mock_config.tracked_user_ids = {12345}
    mock_config.tracked_user_timezone = "America/Chicago"

    mock_repository = Mock()
    mock_qualification_service = Mock()
    mock_date_resolver = Mock()
    mock_listener = Mock()
    mock_gateway = Mock()

    mock_gateway.start = AsyncMock()

    config_mock = Mock(return_value=mock_config)
    sqlite_activity_repository_mock = Mock(return_value=mock_repository)
    qualification_service_mock = Mock(return_value=mock_qualification_service)
    date_resolver_mock = Mock(return_value=mock_date_resolver)
    listener_mock = Mock(return_value=mock_listener)
    gateway_mock = Mock(return_value=mock_gateway)

    monkeypatch.setattr(main, "Config", config_mock)
    monkeypatch.setattr(
        main,
        "SQLiteActivityRepository",
        sqlite_activity_repository_mock,
    )
    monkeypatch.setattr(
        main,
        "ActivityQualificationService",
        qualification_service_mock,
    )
    monkeypatch.setattr(main, "ActivityDateResolver", date_resolver_mock)
    monkeypatch.setattr(main, "EventListener", listener_mock)
    monkeypatch.setattr(main, "DiscordGateway", gateway_mock)

    # Act
    await main.main()

    # Assert
    mock_repository.close.assert_called_once()
