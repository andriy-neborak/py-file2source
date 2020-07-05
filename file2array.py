#!/usr/bin/env python3

import os
import sys
import argparse

def bytes2string(line, elem_per_line=8):
    """
    converts bytes to formated c-style code
    """
    text = ""

    for i, byte in enumerate(line):
        # 4 spaces indention for a new line
        if (i % elem_per_line) == 0:
            text += " " * 4 

        text += "0x{0:02x}, ".format(byte)

        # end of line 
        if ((i+1) % elem_per_line) == 0 and i != 0:
            text += "\r\n"

    return text


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Convert file to file with C-style const array')

    parser.add_argument('-f', required=True, metavar='input file', help='File name for converting')
    parser.add_argument('-o', required=True, metavar='output file', help='The output file that will be created')
    parser.add_argument('-a', action='store_true', help='Append data to output file')
    parser.add_argument('-t', metavar='data type', help='Specifies data type')
    parser.add_argument('-offset', metavar='data offset', help="Specifies input file data offset")
    args = parser.parse_args()

    # -a key
    try:
        mode = "a" if args.a else "w"
        out_file = open(args.o, mode)    
    except OSError:
        print(f"Error to open or create file {args.o}")
        sys.exit(1)

    # -t key
    if args.t:
        data_type = args.t 
    else:
        data_type = "const unsigned char"

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
        file = open(filename, 'rb')
        file.seek(offset)

        array_name = os.path.basename(filename)
        array_name = array_name.replace(".", "_")

        header = f"// File: {filename} \r\n"
        header += f"{data_type} {array_name}[] = "
        header += "{\r\n"

        out_file.write(header)
        out_file.write(bytes2string(line=file.read()))
        out_file.write("\r\n};\r\n\r\n")
                    
        file.close()

    out_file.close()

    
    


    
    
