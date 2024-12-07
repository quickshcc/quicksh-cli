from modules import output
from modules import parser
from modules import api

import sys

parse_status = parser.parse_argvs()
if parse_status is None:
    sys.exit(1)
    
intent = parse_status[0]


if intent == parser.Intent.RECEIVE:
    code = parse_status[1]
    api.request_file_receive(code)


if intent == parser.Intent.TRANSFER:
    path = parse_status[1]
    lifetime = parse_status[2]
    api.request_file_transfer(path, lifetime)


if intent == parser.Intent.LIST:
    api.request_codes_list()
    
    
if intent == parser.Intent.DELETE:
    code = parse_status[1]
    api.request_delete(code)
