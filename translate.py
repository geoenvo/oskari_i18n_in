#!/usr/bin/env python

import argparse
import shutil

import os
import sys


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate translated Oskari language .js file from language string mapping file')
    parser.add_argument('-m', '--mapping', help='Translation string mapping file', type=str, nargs='?', default='en_in.txt')
    parser.add_argument('-i', '--input', help='Input Oskari language .js file', type=str, nargs='?', default='oskari_lang_en.js')
    parser.add_argument('-idi', '--id-input', help='Language ID of input Oskari language .js file', type=str, nargs='?', default='en')
    parser.add_argument('-o', '--output', help='Output Oskari language .js file', type=str, nargs='?', default='oskari_lang_in.js')
    parser.add_argument('-ido', '--id-output', help='Language ID of output Oskari language .js file', type=str, nargs='?', default='in')
    args = parser.parse_args()
    mapping = args.mapping
    input = args.input
    id_input = args.id_input
    output = args.output
    id_output = args.id_output
    if not os.path.isfile(mapping):
        print("The mapping file '{}' does not exist".format(mapping))
        sys.exit()
    if not os.path.isfile(input):
        print("The input js file '{}' does not exist".format(input))
        sys.exit()
    # copy input js to output js file
    output_dirname = os.path.dirname(output)
    ##print output_dirname
    try:
        shutil.copy(input, output)
    except IOError as io_err:
        os.makedirs(output_dirname)
        shutil.copy(input, output)
    # read output file content to string
    output_file_string = ""
    with open(output, 'r') as file_output:
        output_file_string = file_output.read()
    # replace input language id with output language id
    # only replace the string on the right side of colon character
    input_string = ":\"{}\"".format(id_input)
    output_string = ":\"{}\"".format(id_output)
    print("Input string=={}".format(input_string))
    print("Output string=={}".format(output_string))
    output_file_string = output_file_string.replace(input_string, output_string)
    # loop mapping file and replace string in output js file
    with open(mapping, 'r') as file_mapping:
        lines_mapping = file_mapping.readlines() 
        count = 0
        for line in lines_mapping:
            count += 1
            language_string = line.strip()
            if not language_string:
                print("Skipping empty line {}".format(count))
                continue
            if language_string.startswith('#'):
                print("Skipping comment line {}".format(count))
                continue
            language_string_split = language_string.split('==', 1)
            # replace whole input string with quotes to avoid replacing a match within a string!
            # only replace the string on the right side of colon character
            input_string = ":\"{}\"".format(language_string_split[0])
            output_string = ":\"{}\"".format(language_string_split[1])
            # replace <space> placeholder on end of output string
            output_string = output_string.replace('<space>', ' ')
            print("Line {}: {}".format(count, language_string))
            print("Input string=={}".format(input_string))
            print("Output string=={}".format(output_string))
            output_file_string = output_file_string.replace(input_string, output_string)
            # do not replace key matches, replace it back to original! example: "key":"Search" not "key":"Pencarian"
            output_key_string = "\"key\"{}".format(output_string)
            input_key_string = "\"key\"{}".format(input_string)
            print("Output key string=={}".format(output_key_string))
            print("Input key string=={}".format(input_key_string))
            output_file_string = output_file_string.replace(output_key_string, input_key_string)
    # write replaced output string to output file
    ##print output_file_string
    with open(output, 'w') as file_output:
        file_output.write(output_file_string)
