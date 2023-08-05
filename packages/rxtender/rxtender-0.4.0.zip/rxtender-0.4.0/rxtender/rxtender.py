import os
import argparse
import tatsu
from tatsu.util import re
from codecs import open
from pprint import pprint

from jinja2 import Environment, PackageLoader

def generate_feature(template, streams, structs):
    generated_code = {
    'header':  template['header'].render(streams=streams, structs=structs),
    'content': template['content'].render(streams=streams, structs=structs),
    'footer': template['footer'].render(streams=streams, structs=structs)
    }
    return generated_code

def split_template_location(location):
    return location.split('.', maxsplit=1)

def get_template(package_name):
    env = Environment(
        loader=PackageLoader(package_name, '')
    )

    template = {
        'header': env.get_template('source.header.tpl'),
        'footer': env.get_template('source.footer.tpl'),
        'content': env.get_template('source.content.tpl')
    }
    return template

def append_generated_code(accumulator, code):
    sections = ['header', 'content', 'footer']
    for section in sections:
        accumulator[section].append(code[section])
    return accumulator

def save_generated_code(filename, accumulator):
    file = open(filename, 'w')
    sections = ['header', 'content', 'footer']
    for section in sections:
        for block in accumulator[section]:
            file.write(block)
            file.write('\n')

    file.close()

def generate_code(ast, generate):
    structs = []
    streams = []
    for entry in ast:
        if 'struct' in entry and entry['struct'] is not None:
            structs.append(entry['struct'])
        elif 'stream' in entry and entry['stream'] is not None:
            streams.append(entry['stream'])

    generated_accumulator = {'header':[], 'content':[], 'footer':[]}

    if 'framing' in generate:
        generated = generate_feature(get_template(generate['framing']), streams, structs)
        generated_accumulator = append_generated_code(generated_accumulator, generated)
    if 'serialization' in generate:
        generated = generate_feature(get_template(generate['serialization']), streams, structs)
        generated_accumulator = append_generated_code(generated_accumulator, generated)
    if 'stream' in generate:
        for stream_pkg in generate['stream']:
            generated = generate_feature(get_template(stream_pkg), streams, structs)
            generated_accumulator = append_generated_code(generated_accumulator, generated)

    return generated_accumulator

def parse_idl(definitions, filename=''):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    grammar = open(dir_path + '/rxtender.ebnf').read()
    parser = tatsu.compile(grammar)

    ast = None
    try:
        ast = parser.parse(definitions)
    except tatsu.exceptions.FailedParse as e:
        info = e.buf.line_info(e.pos)
        text = info.text.rstrip()
        leading = re.sub(r'[^\t]', ' ', text)[:info.col]
        leading = leading.expandtabs()
        print('{}({}:{}) {}:\n{}\n{}^'.format(
            filename,
            info.line + 1, info.col + 1,
            e.message.rstrip(),
            text.expandtabs(),
            leading
        ))
        pass

#    pprint(ast, width=20, indent=4)
    return ast

def parse_idl_file(input):
    return parse_idl(open(input).read(), input)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', help='rxtender definition file of a source stream')
    parser.add_argument('--output', help='file where generated code is saved')
    parser.add_argument('--framing', help='module used for framing')
    parser.add_argument('--serialization', help='module used for serialization')
    parser.add_argument('--stream', action='append', help='module used for stream routing')
    args = parser.parse_args()

#    print("args: ", repr(args))

    ast = parse_idl_file(args.input) if args.input else None
    generate = {}
    if args.framing:
        generate['framing'] = args.framing
    if args.serialization:
        generate['serialization'] = args.serialization
    if args.stream:
        generate['stream'] = args.stream

    if ast and args.output:
        save_generated_code(args.output, generate_code(ast, generate))


if __name__ == '__main__':
    main()
