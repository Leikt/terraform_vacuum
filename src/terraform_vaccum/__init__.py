import argparse
import os.path

from .template_processor import Template, register_modules


def _run(data_filename: str, template_filename: str, variable_filename: str = None) -> int:
    for filename in [data_filename, template_filename, variable_filename]:
        if filename is not None and not os.path.exists(filename):
            raise FileNotFoundError('No such file as "{}"'.format(filename))

    register_modules()

    template = Template()
    template.load_data(data_filename)
    template.load_template(template_filename)
    if variable_filename is not None:
        template.load_variables(variable_filename)

    renderers = template.run()
    for renderer in renderers:
        renderer.adjust_indent().save()

    return 0


def cli(argv):
    parser = argparse.ArgumentParser(prog='Terraform Vacuum')
    parser.add_argument('-T', '--template', type=str, required=True, metavar='FILE',
                        help='Template file to use.')
    parser.add_argument('-D', '--data', type=str, required=True, metavar='FILE',
                        help='Data file to use.')
    parser.add_argument('-V', '--variables', type=str, default=None, metavar='FILE',
                        help='Variables files to use.')
    args = parser.parse_args(argv)
    return _run(args.data, args.template, args.variables)
