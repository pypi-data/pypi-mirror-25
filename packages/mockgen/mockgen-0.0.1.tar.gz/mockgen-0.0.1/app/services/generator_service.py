from jinja2 import Template
from os import path
import os
import glob
import re

def generate(mocks, template_name, output_dir, templates_path, domain):
    template_name = get_template_name(templates_path, template_name)
    template = get_template(templates_path, template_name)
    output_path = path.join(output_dir, template_name)
    mock_str = template.render(mocks=mocks, domain=domain)
    if not path.exists(output_dir):
        os.mkdir(output_dir)
    with open(output_path, 'w') as f:
        f.write(mock_str)
    return {
        'template_name': template_name,
        'output_path': output_path,
        'mock_str': mock_str
    }

def get_template_name(templates_path, template_name):
    filenames = list()
    shortest = 0
    current_filename = ''
    for filename in glob.glob(path.join(templates_path, '*')):
        try:
            if filename.index(template_name):
                filename = re.sub('.*\/', '', filename)
                if len(filename) < shortest or shortest == 0:
                    shortest = len(filename)
                    current_filename = filename
        except ValueError:
            pass
    if current_filename == '':
        exit('Invalid template')
    return current_filename

def get_template(templates_path, template_name):
    template_path = path.abspath(path.join(templates_path, template_name))
    with open(template_path, 'r') as f:
        return Template(f.read())
