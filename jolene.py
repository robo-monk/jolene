#!/usr/bin/env python3

from cryptography.fernet import Fernet
import os
import sys
import json

_version = "0.1.0"
_creds = ".jolene/creds.json"

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

def write(dic):
    print('writing to file', dic)
    with open(_creds, "w") as write_file:
        json.dump(dic, write_file)

def _load_creds():
    with open(_creds) as rf:
        return json.load(rf)

def user_input_data():
    print(f"Enter data to ecode in JSON format with JOLENE. \n eg. username: jolene, password: i love jolene, date: 7/10/2017")
    entering = True

    data = {}
    inp = input(":: ")

    for row in inp.split(", "):
        key, value = row.split(": ")
        data[key] = value

    return data

def dic_diff(og, edit):
    for key, value in edit.items():
        og[key] = value
    return og

def add_data(dic):
    new = encrypt_dic(dic)
    write(dic_diff(_load_creds(), new))

def get(key):
    creds = _load_creds()
    if key in creds:
        return decrypt(creds[key])

    return None

def run_cli(args):
    print(f" \n\n\tJOLENE 💈  \n\n \tv{_version}\n")
    if _key() is not None: 
        print(f"Current ENV key is {_key().decode()} \n")
        inp = input(f"Add data to JOLENE? (y/n): ")
        if inp == "y":
            add_data(user_input_data())
            return


    inp = input(f"Remove everything and start over (y/n): ")
    if (inp != "y"): return
    print(f" \n\n\tJOLENE SETUP 💈 \n\n")
    print(f"By continuing {_creds} will be obliterated and the current JOLENE key will be rendered useless. \n ")
    input("Ok?")

    input("Generate new JOLENE key [enter] \n")
    new_key = _gen_key()
    print(f"New key is {new_key} \n")

    data = user_input_data() 

    enc = encrypt_dic(data)
    print(enc)
    write(enc)

    print(f"Exported encrypted data to {_creds} \n")
    print(f"Please run $\t {_set_key(new_key)}")


