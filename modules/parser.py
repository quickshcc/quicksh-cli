from tkinter import filedialog as fd
from modules import output

from enum import Enum
import sys
import os


class Intent(Enum):
    RECEIVE = "receive"
    TRANSFER = "transfer"
    LIST = "list"
    DELETE = "delete"


TRANSFER_LIFETIMES = {
    "15m": 0,
    "1h": 1,
    "12d": 2,
    "1d": 3,
    "3d": 4,
}


def get_intent(intent: str) -> Intent | None:
    if intent in ("r", "receive", "get"):
        return Intent.RECEIVE
        
    elif intent in ("t", "u", "transfer", "up", "upload"):
        return Intent.TRANSFER
        
    elif intent in ("l", "list"):
        return Intent.LIST
        
    elif intent in ("d", "del", "delete", "rm", "remove"):
        return Intent.DELETE
    

def parse_argvs() -> tuple[Intent, str | None, int | None] | None:
    args = sys.argv[1:]
    
    if not args:
        return output.error_message("Intent not set.  ( [r]eceive / [t]ransfer / [l]ist / [d]elete )")

    intent = get_intent(args.pop(0).lower())
    
    if intent is None:
        return output.error_message(f"Invalid intent.  Use: ( [r]eceive / [t]ransfer / [l]ist / [d]elete )")
    
    if intent == Intent.RECEIVE:
        if not args:
            return output.error_message(f"Code not set.  (... {intent} CODE)")
        
        code = args.pop(0)
        
        if len(code) != 5:
            return output.error_message("Code must contain 5 digits.")
        
        if not code.isnumeric():
            return output.error_message("Code must contain only digits.")
    
        if code[0] == "0":
            return output.error_message("Code must not start with 0.")
    
        return (intent, code, None)
    
    if intent == Intent.TRANSFER:
        if not args:
            path = fd.askopenfilename()
            
            if not path:
                return output.error_message("No file chosen.")
            
            output.output_transfer_status("Set transfer lifetime to:  1 hour")
            lifetime = TRANSFER_LIFETIMES.get("1h")

            return (intent, path, lifetime)

        path = args.pop(0)
        
        if not os.path.exists(path):
            return output.error_message(f"File: `{path}` does not exist.")
        
        if not os.path.isfile(path):
            return output.error_message(f"`{path}` must be a file.")
            
        if not args:
            output.output_transfer_status("Set transfer lifetime to:  1 hour")
            lifetime = TRANSFER_LIFETIMES.get("1h")

            return (intent, path, lifetime)
        
        lifetime = args.pop(0).lower()
        
        if lifetime not in TRANSFER_LIFETIMES:
            return output.error_message(f"Invalid lifetime: `{lifetime}`. Use: (15m / 1h / 12h / 1d / 3d)")
            
        lifetime = TRANSFER_LIFETIMES.get(lifetime)
        return (intent, path, lifetime)

    if intent == Intent.LIST:
        return (intent, None, None)
    
    if intent == Intent.DELETE:
        if not args:
            return output.error_message("Delete target `code` not provided.")
        
        code = args.pop(0)
        return (intent, code, None)
    