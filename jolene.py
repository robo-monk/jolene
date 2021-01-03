#!/usr/bin/env python3

from cryptography.fernet import Fernet
import os
import sys
import json

_version = "0.1.0"
_creds = "jolene/creds.json"

def _key():
    key = os.environ.get("JOLENE")
    if key is None: return None
    return key.encode()

def _set_key(key):
    return f"export JOLENE={key}"

def _fernet():
    return Fernet(_key())

def _gen_key():
    key = Fernet.generate_key().decode()
    os.environ['JOLENE'] = key
    return key

def decrypt(string):
    return _fernet().decrypt(string.encode()).decode()

def encrypt(string):
    return _fernet().encrypt(string.encode()).decode()

def encrypt_dic(dic):
    enc = {}
    for key, value in dic.items():
        enc[key] = encrypt(value)

    return enc


def _load_creds():
    with open(_creds) as rf:
        return json.load(rf)

def get(key):
    creds = _load_creds()
    if key in creds:
        return decrypt(creds[key])

    return None

def run_cli(args):
    print(f" \n\n\tJOLENE 💈  \n\n \tv{_version}\n")
    print(f"Current ENV key is {_key().decode()} \n")
    input(f"Press any key to remove everything and start over. Or CTRL+c to exit\n")
    print(f" \n\n\tJOLENE SETUP 💈 \n\n")
    print(f"By continuing {_creds} will be obliterated and the current JOLENE key will be rendered useless. \n ")
    input("Ok?")

    input("Generate new JOLENE key [enter] \n")
    new_key = _gen_key()
    print(f"New key is {new_key} \n")

    print(f"Enter data to ecode in JSON format with JOLENE. \n eg. username: jolene, password: i love jolene, date: 7/10/2017")
    entering = True

    data = {}
    inp = input(":: ")

    for row in inp.split(", "):
        key, value = row.split(": ")
        data[key] = value

    enc = encrypt_dic(data)
    print(enc)

    with open(_creds, "w") as write_file:
        json.dump(enc, write_file)

    print(f"Exported encrypted data to {_creds} \n")
    print(f"Please run $\t {_set_key(new_key)}")



if len(sys.argv) > 1:
    run_cli(sys.argv)
