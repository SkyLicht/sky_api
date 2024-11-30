from core.data.types import OutputType


def map_output_from_type_to_string(output: OutputType, factory:str=None) -> str:
    """Map the output type to a string."""
    if output == "input":
        return "SMT"
    elif output == "output":
        return "SMT"
    elif output == "packing":
        return "Packing"
    else:
        return "Unknown"