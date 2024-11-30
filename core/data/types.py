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


class OutputType(Enum):
    """Output types."""
    INPUT = "input"
    OUTPUT = "output"
    PACKING = "packing"

    @classmethod
    def from_string(cls, value: str) -> "OutputType":
        """Get the enum from a string."""

        if value == "SMT_OUT":
            return cls.OUTPUT
        elif value == "SMT_IN":
            return cls.INPUT
        elif value == "PACKING":
            return cls.PACKING

        for item in cls:
            if item.value == value:
                return item
        return cls.PACKING



    @classmethod
    def from_value(cls, value: str) -> "OutputType":
        """Get the enum from a string."""
        return cls.from_string(value)
class ShiftType(Enum):
    """Shifts."""
    ALL = "all"
    FIRST = "first"
    SECOND = "second"
    THIRD = "third"

    @classmethod
    def from_string(cls, value: str) -> "ShiftType":
        """Get the enum from a string."""
        for item in cls:
            if item.value == value:
                return item
        return cls.ALL

    @classmethod
    def from_value(cls, value: str) -> "ShiftType":
        """Get the enum from a string."""
        return cls.from_string(value)

class FactoryType(Enum):
    """Factories."""
    A5 = "A5"
    A6 = "A6"

    @classmethod
    def from_string(cls, value: str) -> "FactoryType":
        """Get the enum from a string."""
        for item in cls:
            if item.value == value:
                return item
        return cls.A6

    @classmethod
    def from_value(cls, value: str) -> "FactoryType":
        """Get the enum from a string."""
        return cls.from_string(value)