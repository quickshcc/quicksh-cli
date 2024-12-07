from modules import output

import requests
import os

API_BASE = "http://quicksh.cc/api/"


def request_file_receive(code: str) -> None:
    url = API_BASE + f"receive/{code}"

    try:
        response = requests.get(url, timeout=3)
    except Exception as error:
        return output.output_receive_staus(f"Failed to connect with API: {error}")
        
    if response.status_code != 200:
        if response.status_code == 422:
            return output.output_receive_status("Internal error.")
        
        err_msg = response.json()["error"]
        return output.output_receive_staus(f"Failed to receive: {code} - {err_msg}")
        
    content_disposition = response.headers.get("content-disposition")
    name = content_disposition.split("=")[1].strip('"')

    with open(name, "a+b") as file:
        file.write(response._content)

    output.output_receive_staus(f"Received file:  {name} ({code})")
    
    
def request_file_transfer(path: str, lifetime: int) -> None:
    url = API_BASE + "transfer"
    name = os.path.basename(path)
    response = requests.post(url, data={"expire": str(lifetime)}, files={'file': open(path, 'rb')})

    if response.status_code != 200:
        if response.status_code == 422:
            return output.output_transfer_status("Internal error.")
        
        err_msg = response.json()["error"]
        return output.output_transfer_status(f"Failed to tranfer: {err_msg}")
    
    code = response.json()["code"]
    expire = response.json()["expire"]
    output.output_transfer_status(f"Transfered: {name}")
    output.output_transfer_status(f"CODE  : {code}")
    output.output_transfer_status(f"EXPIRE: {expire}")
    
    
def request_codes_list() -> None:
    url = API_BASE + "owned-codes"
    response = requests.get(url)
    
    if response.status_code != 200:
        if response.status_code == 422:
            return output.output_transfer_status("Internal error.")
        
        err_msg = response.json()["error"]
        return output.output_transfer_status(f"Failed receive transfers history: {err_msg}")
    
    codes = response.json().get("response", {})
    if not codes:
        return output.output_transfer_status("(no items)")
    
    for code, data in codes.items():
        name = data["file"]
        expire = data["expire"]
        output.output_transfer_status(f"{code}  -  {name} ({expire})")
        
        
def request_delete(code: str) -> None:
    url = API_BASE + f"delete/{code}"
    response = requests.delete(url)
    
    if response.status_code != 200:
        if response.status_code == 422:
            return output.output_transfer_status("Internal error.")
        
        err_msg = response.json()["error"]
        return output.output_transfer_status(f"Failed to delete: {err_msg}")
        
    output.output_transfer_status(f"Removed {code}")

