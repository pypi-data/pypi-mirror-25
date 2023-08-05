
from flask import Flask
from flatapi import *
import argparse


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--port", type=int,
                    help="Customize the port")
    parser.add_argument("-G", "--cfgfile", 
                    help="Customize the config file") 
    parser.add_argument("-S", "--storage", 
                    help="Customize the storage. Option: FILE | MOMERY ")  
    parser.add_argument("-X", "--prefix", 
                    help="Customize the prefix, e.g. /api")

    args = parser.parse_args()               
    _port = args.port or 5000
    _cfgfile = args.cfgfile 
    _prefix = args.prefix
    _storage = upper(args.storage) if args.storage else args.storage

    app = Flask(__name__)
    restApi = FlatApi(app, cfg_file=_cfgfile, prefix = _prefix , storage = _storage)
    app.run(debug=False, port = _port )
