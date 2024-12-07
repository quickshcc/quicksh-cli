import tcolorpy


RECEIVE_COLOR = (100, 185, 137)
TRANSFER_COLOR = (71, 171, 201)

RECEIVE_PREFIX = f"{tcolorpy.tcolor('(', styles=[tcolorpy.AnsiStyle.DIM])}{tcolorpy.tcolor('receive', RECEIVE_COLOR)}{tcolorpy.tcolor(')', styles=[tcolorpy.AnsiStyle.DIM])} "
TRANSFER_PREFIX = f"{tcolorpy.tcolor('(', styles=[tcolorpy.AnsiStyle.DIM])}{tcolorpy.tcolor('transfer', TRANSFER_COLOR)}{tcolorpy.tcolor(')', styles=[tcolorpy.AnsiStyle.DIM])} "
ERROR_PREFIX = tcolorpy.tcolor(" E ", color=tcolorpy.AnsiFGColor.BLACK, bg_color=tcolorpy.AnsiBGColor.RED) + " "


def output_receive_staus(message: str) -> None:
    print(RECEIVE_PREFIX + message)
    
    
def output_transfer_status(message: str) -> None:
    print(TRANSFER_PREFIX + message)


def error_message(message: str) -> None:
    print(ERROR_PREFIX + message)
    
