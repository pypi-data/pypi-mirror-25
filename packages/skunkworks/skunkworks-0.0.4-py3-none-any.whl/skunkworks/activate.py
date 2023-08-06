# -*- coding: utf-8 -*-

# LICENSE
# -------

# Copyright 2017 James Draper

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files, (the software)), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions: The above copyright
# notice and this permission notice shall be included in all copies or
# substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS",
# WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import sys
import subprocess
import zipfile
import getpass
import shutil
import zipfile
import argparse
import compileall
from simplecrypt import encrypt, decrypt

here = os.path.abspath(os.path.dirname(__file__))
# Find the sitepackages file.
upper = os.path.split(here)[0]
upper = os.path.split(upper)[0]
omin_dir = os.path.join(upper, 'omin')

# def destroy():
#     p = subprocess.Popen("pip uninstall -y skunkworks")
#     p.kill()

def activate(password=None):
    cb_dir = os.path.join(here, 'CODEBASE')
    if os.path.exists(cb_dir):
        with open(cb_dir,"rb") as f:
            dec = f.read()
        if password == None:
            password = getpass.getpass("Password:")
        try:
            dec = decrypt(password, dec)
            decrypted_path = '.'.join([cb_dir, 'zip'])
            print('Extracting codebase...')
            with open(decrypted_path, 'wb') as f:
                f.write(dec)
            decrypted_archive = zipfile.ZipFile(decrypted_path, 'r')
            decrypted_archive.extractall(omin_dir)
            # compileall.compile_dir(omin_dir)
            compileall.compile_dir(omin_dir)
            decrypted_archive.close()
            os.remove(decrypted_path)
        except Exception:
            print("Failed...")
    else:
        print('CODEBASE not found.')
    # destroy()


# Commandline interface
parser = argparse.ArgumentParser()
parser.add_argument("-p", "--password",
                    type=str,
                    help="The password to activate the package.",
                    nargs='?',
                    default=None)

args = parser.parse_args()

if __name__ == "__main__":
    activate(args.password)
