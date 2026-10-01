from dataclasses import dataclass


@dataclass(frozen=True)
class TimezoneOption:
    """Represents a curated timezone choice."""

    name: str
    timezone: str
    flag: str


TIMEZONE_OPTIONS = (
    # Asia-Pacific
    TimezoneOption(
        name="Singapore",
        timezone="Asia/Singapore",
        flag="🇸🇬",
    ),
    TimezoneOption(
        name="Tokyo",
        timezone="Asia/Tokyo",
        flag="🇯🇵",
    ),
    TimezoneOption(
        name="Seoul",
        timezone="Asia/Seoul",
        flag="🇰🇷",
    ),
    TimezoneOption(
        name="Hong Kong",
        timezone="Asia/Hong_Kong",
        flag="🇭🇰",
    ),
    TimezoneOption(
        name="Taipei",
        timezone="Asia/Taipei",
        flag="🇹🇼",
    ),
    TimezoneOption(
        name="Shanghai",
        timezone="Asia/Shanghai",
        flag="🇨🇳",
    ),
    TimezoneOption(
        name="Mumbai",
        timezone="Asia/Kolkata",
        flag="🇮🇳",
    ),
    TimezoneOption(
        name="Dubai",
        timezone="Asia/Dubai",
        flag="🇦🇪",
    ),
    TimezoneOption(
        name="Sydney",
        timezone="Australia/Sydney",
        flag="🇦🇺",
    ),
    TimezoneOption(
        name="Auckland",
        timezone="Pacific/Auckland",
        flag="🇳🇿",
    ),

    # Europe
    TimezoneOption(
        name="London",
        timezone="Europe/London",
        flag="🇬🇧",
    ),
    TimezoneOption(
        name="Paris",
        timezone="Europe/Paris",
        flag="🇫🇷",
    ),
    TimezoneOption(
        name="Berlin",
        timezone="Europe/Berlin",
        flag="🇩🇪",
    ),
    TimezoneOption(
        name="Madrid",
        timezone="Europe/Madrid",
        flag="🇪🇸",
    ),
    TimezoneOption(
        name="Rome",
        timezone="Europe/Rome",
        flag="🇮🇹",
    ),
    TimezoneOption(
        name="Moscow",
        timezone="Europe/Moscow",
        flag="🇷🇺",
    ),

    # North America
    TimezoneOption(
        name="New York",
        timezone="America/New_York",
        flag="🇺🇸",
    ),
    TimezoneOption(
        name="Chicago",
        timezone="America/Chicago",
        flag="🇺🇸",
    ),
    TimezoneOption(
        name="Denver",
        timezone="America/Denver",
        flag="🇺🇸",
    ),
    TimezoneOption(
        name="Los Angeles",
        timezone="America/Los_Angeles",
        flag="🇺🇸",
    ),
    TimezoneOption(
        name="Toronto",
        timezone="America/Toronto",
        flag="🇨🇦",
    ),
    TimezoneOption(
        name="Vancouver",
        timezone="America/Vancouver",
        flag="🇨🇦",
    ),

    # Other
    TimezoneOption(
        name="São Paulo",
        timezone="America/Sao_Paulo",
        flag="🇧🇷",
    ),
    TimezoneOption(
        name="Johannesburg",
        timezone="Africa/Johannesburg",
        flag="🇿🇦",
    ),
)
