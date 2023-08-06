import os
import argparse
from jinja2 import Environment, FileSystemLoader

from tinyj2 import __description__


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument('--template-dir', '-t', default='templates/', help='Directory containing templates')
    parser.add_argument('--output-dir', '-o', default='./', help='Directory to store output files')
    args = parser.parse_args()

    template_dir = os.path.expanduser(args.template_dir)
    output_dir = os.path.expanduser(args.output_dir)

    j2_env = Environment(loader=FileSystemLoader(template_dir))
    env = dict(os.environ.items())

    for template in j2_env.list_templates():
        rendered = j2_env.get_template(template).render(env=env)
        output_file = os.path.join(output_dir, template)
        with open(output_file, 'w') as f:
            f.write(rendered)


if __name__ == '__main__':
    main()

