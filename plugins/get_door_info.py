import uuid
import socket
import logging
import requests
import subprocess
from bs4 import BeautifulSoup


def get_public_ip_2():
    url = "https://diagnostic.opendns.com/myip"
    session = requests.Session()
    public_ip = session.get(url).text
    return public_ip

def get_public_ip_1():
    # https://www.cyberciti.biz/faq/how-to-find-my-public-ip-address-from-command-line-on-a-linux/
    cmd_ip = "dig +short myip.opendns.com @resolver1.opendns.com -4"
    resp = subprocess.run(cmd_ip, shell=True, capture_output=True, text=True)
    public_ip = resp.stdout
    if public_ip.endswith("\n"):
        public_ip = public_ip.split("\n")[0]
    return public_ip

def get_local_addr_2():
    cmd = "ip route show | grep -oP '(?<=src\s)\d+(\.\d+){3}'"
    resp = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    ips = resp.stdout.split("\n")
    local_ip = None
    if len(ips) == 3:
        inter_wlp, local_ip, _ = ips
    else:
        inter_wlp, _ = ips
    return local_ip, inter_wlp

def get_ip_address():
    # https://stackoverflow.com/a/30990617
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

def get_local_addr_1():
    # https://stackoverflow.com/a/23822431
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    local_ip = s.getsockname()[0]
    s.close()
    return local_ip

def get_loc():
    tags = {"ip": "Public IP", "lat": "Latitude", 
            "lng": "Longitude", "country_name": "Country", 
            "region_name": "Region", "city": "City", 
            "company": "Organization"}
    url = "https://iplocation.com/"
    session = requests.Session()
    resp = session.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    info = [{value:c.text for c in soup.findAll(class_=tag)} for tag, value in tags.items()]
    return info

def get_mac_eno():
    _mac = uuid._ip_getnode()
    mac = uuid.getnode()
    m = mac if mac == _mac else _mac
    fmac = ":".join(hex(m)[i:i+2] for i in range(2, 14, 2))
    return fmac

def write_infos():
    infoloc = get_loc()
    local_ip1, inter_wlp = get_local_addr_2()
#    local_ip2 = get_ip_address()
    local_ip3 = get_local_addr_1()
    mac = get_mac_eno()

    with open("door_info.txt", "w") as info_door:
        info_door.write("Door Host Information\n\n")
        for infos in infoloc:
            for key, value in infos.items():
                form_str = f"{key}:\t{value}\n"
                info_door.write(form_str)
        form_str = f"Local IP:\t{local_ip3:}\n"
        info_door.write(form_str)
        form_str = f"Interface wlp IP:\t{inter_wlp}\n"
        info_door.write(form_str)
        form_str = f"MAC Address:\t{mac}\n"
        info_door.write(form_str)
    return True

if __name__ == "__main__":
    write_infos()
