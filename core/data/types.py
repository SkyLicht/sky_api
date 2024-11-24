from enum import Enum


class AreaType(Enum):
    """Area types."""
    UNKNOWN = "unknown"
    OUTPUT = "output"
    PACKING = "packing"

    @classmethod
    def from_string(cls, value: str) -> "AreaType":
        """Get the enum from a string."""
        for item in cls:
            if item.value == value:
                return item
        return cls.UNKNOWN

    @classmethod
    def from_value(cls, value: str) -> "AreaType":
        """Get the enum from a string."""
        return cls.from_string(value)


class SectionNickname(Enum):
    """Section nicknames."""
    UNKNOWN = "unknown"
    AU = "au" # Automation
    EES = "ees" # Equipment SMT
    EEP = "eep" # Equipment Packing
    PD = "pd" # Production
    PN = "pn" # Programming
    IE = "ie" # Industrial Engineering
    QA = "qa" # Quality

    @classmethod
    def from_string(cls, value: str) -> "SectionNickname":
        """Get the enum from a string."""
        for item in cls:
            if item.value == value:
                return item
        return cls.UNKNOWN

    @classmethod
    def from_value(cls, value: str) -> "SectionNickname":
        """Get the enum from a string."""
        return cls.from_string(value)