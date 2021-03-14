#!/usr/bin/env python3

import os
import sys
import argparse

def bytes2string(data, elem_per_line=8, indent_level=4, indent_symbol=" "):
    """
    converts bytes to formated c-style code
    """
    lines = list()
    line = str()

    for start in range(0, len(data), elem_per_line):
        line = indent_symbol * indent_level
        line += ", ".join(map("0x{0:02x}".format, data[start:start + elem_per_line]))
        lines.append(line)

    return ",\n".join(lines)


def get_array_name(filename):
    name = os.path.basename(filename)
    return name.replace(".", "_")


def create_parser():
    parser = argparse.ArgumentParser(description='Convert file to file with C-style const array')

    parser.add_argument('-f', required=True, metavar='input file', help='File name for converting')
    parser.add_argument('-o', required=True, metavar='output file', help='The output file that will be created')
    parser.add_argument('-a', action='store_true', help='Append data to output file')
    parser.add_argument('-t', metavar='data type', help='Specifies data type')
    parser.add_argument('-offset', metavar='data offset', type=int, help="Specifies input file data offset")
    parser.add_argument('-ds', action='store_true', help='Add array size #define')

    return parser.parse_args()


if __name__ == "__main__":
    args = create_parser()
    # -a key
    mode = "a" if args.a else "w"
    # -t key
    data_type = args.t or "const unsigned char"
    # -offset key
    offset = args.offset or 0
    # -ds 
    define_arr_size = bool(args.ds) 

    for filename in [args.f]:
        file_content = None
        try:
            with open(filename, 'rb') as file:
                file.seek(offset)
                file_content = file.read()
        except FileNotFoundError:
            print(f"File {filename} not found")
            continue
        except Exception as e:
            print(f"{e}")
            continue

        # Preparing data to write
        array_name = get_array_name(filename)

        source = str()
        source += f'// File: {filename}\n'

        define_name = ""
        if define_arr_size:
            define_name = f"{array_name.upper()}_SIZE"
            source += f'#define {define_name} {len(file_content)}\n'

        source += f'{data_type} {array_name}[{define_name}] = {{\n'
        source += bytes2string(file_content)
        source += "\n};"

        try:
            with open(args.o, mode) as out_file:
                out_file.write(source)
        except OSError:
            print(f"Error to open or create file {args.o}")
            sys.exit(1)

    sys.exit(0)
