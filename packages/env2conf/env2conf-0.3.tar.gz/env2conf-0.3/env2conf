#!/usr/bin/env python
import fnmatch
import os
import re
from os.path import abspath, dirname, join

from jinja2 import Environment, FileSystemLoader

current_dir = dirname(abspath(__file__))


def main():
    _setup_output_dir()

    template_file_names = _list_template_file_names()
    context = _collect_context()

    for filename in template_file_names:
        content = _render_template(filename, context)
        _write_to_output(content, filename)


def _setup_output_dir():
    os.system('mkdir -p {}'.format(args.output_dir))
    os.system('rm -rf {}/*'.format(args.output_dir))


def _render_template(template_file_name, context):
    return templates_env.get_template(template_file_name).render(context)


def _write_to_output(content, template_file_name):
    output_file_path = join(args.output_dir, re.sub(r"\.j2$", '', template_file_name))
    
    with open(output_file_path, 'w') as f:
        f.write(content)


def _collect_context():
    return {key: val for key, val in os.environ.items()}


def _list_template_file_names():
    matches = []

    for root, dir_names, file_names in os.walk(args.templates_dir):
        if len(dir_names) > 0:
            print("It does not support sub folder in templates folder.")
            exit(1)
        matches.extend(fnmatch.filter(file_names, '*.j2'))

    return matches


def _parse_args():
    import argparse
    parser = argparse.ArgumentParser(description='A tool for the config files generation from environment variables.')
    parser.add_argument("-i", action="store", dest="templates_dir",
                        help="existing templates dir", required=True)
    parser.add_argument("-o", action="store", dest="output_dir",
                        help="expected output dir", required=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()

    templates_env = Environment(loader=FileSystemLoader(args.templates_dir))

    main()
    print("Done. Check out the output files at {}".format(args.output_dir))
