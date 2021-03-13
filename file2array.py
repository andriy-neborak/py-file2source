#!/usr/bin/env python3

import os
import sys
import argparse

def bytes2string(data, elem_per_line=8):
    """
    converts bytes to formated c-style code
    """
    text = str()
    lines_list = list()

    for r in range(0, len(data), elem_per_line):
        line = " " * 4
        line += ", ".join(map("0x{0:02x}".format, data[r:r + elem_per_line]))
        lines_list.append(line)
    
    text = ",\n".join(lines_list)

    return text


def get_array_name(filename):
    name = os.path.basename(filename)
    return name.replace(".", "_")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert file to file with C-style const array')

    parser.add_argument('-f', required=True, metavar='input file', help='File name for converting')
    parser.add_argument('-o', required=True, metavar='output file', help='The output file that will be created')
    parser.add_argument('-a', action='store_true', help='Append data to output file')
    parser.add_argument('-t', metavar='data type', help='Specifies data type')
    parser.add_argument('-offset', metavar='data offset', help="Specifies input file data offset")
    args = parser.parse_args()

    # -a key
    mode = "a" if args.a else "w"
    # -t key
    data_type = args.t or "const unsigned char"

    # -offset key
    if args.offset:
        try:
            offset = int(args.offset, 0)
        except ValueError:
            print(f"Offset value {args.offset} is invalid")
            sys.exit(1)
    else:
        offset = 0

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

        try:
            with open(args.o, mode) as out_file:
                array_name = get_array_name(filename)

                header = list()
                header.append(f'// File: {filename}')
                header.append(f'{data_type} {array_name}[] = {{')

                out_file.write("\n".join(header) + "\n")
                out_file.write(bytes2string(file_content))

                out_file.write("\n};")

        except OSError:
            print(f"Error to open or create file {args.o}")
            sys.exit(1)

    sys.exit(0)
