#!/home/rodrigo/projetos/flexdeploy/venv27/bin/python

# -*- coding: utf-8 -*-

import os

import fabric.main

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    fabric.main.main(fabfile_locations=[path + '/fabfile.py'])

if __name__ == "__main__":
    main()
