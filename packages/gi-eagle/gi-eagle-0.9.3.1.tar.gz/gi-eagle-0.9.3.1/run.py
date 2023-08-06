#!/usr/bin/env python3
from eagle.application import app
from eagle.scripts import convert_vcf
import sys

import argparse


def start_interface(args):
    if args.public:
        host = '0.0.0.0'
    else:
        host = '127.0.0.1'

    # start the server
    app.secret_key = 'T0Jw9sidVJi0vybbuCNN'
    app.run(config=args.config, host=host, port=args.port, debug=args.debug, use_reloader=args.debug)


def add_interface_parser(parser):
    parser.add_argument('--port', '-p', default=8000, type=int, help="port (default: 8000)")
    parser.add_argument('--public', default=False, action='store_true', help="listen for external connections")
    parser.add_argument('--nodebug', dest='debug', default=True, action='store_false', help="disable debug messages")
    parser.add_argument('--config', '-c', required=True, help="config file to use.")
    parser.set_defaults(func=start_interface)



def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command', description='valid subcommands')
    subparsers.required = True
	
    parser_interface = subparsers.add_parser('interface', help='run the EAGLE interface service')
    add_interface_parser(parser_interface)

    parser_convert = subparsers.add_parser('convert', help='converts a vcf file to the eagle format')
    convert_vcf.create_parser(parser_convert)


    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
