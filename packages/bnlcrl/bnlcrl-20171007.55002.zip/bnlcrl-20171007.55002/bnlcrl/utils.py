import json
import os
from pykern import pkjinja


def defaults_file(suffix=None, defaults_file_path=None):
    script_path = os.path.dirname(os.path.realpath(__file__))

    # Fix for Jython:
    try:
        script_path = script_path.replace(
            os.path.join(format(os.environ['HOME']), '.jython-cache/cachedir/classes'),
            ''
        )
    except:
        pass

    dat_dir = os.path.join(script_path, 'package_data', 'dat')
    config_dir = os.path.join(script_path, 'package_data', 'json')
    if not defaults_file_path:
        file_name = 'defaults_{}.json'.format(suffix) if suffix else 'defaults.json'
        defaults_file = os.path.join(config_dir, file_name)
    else:
        defaults_file = defaults_file_path

    return {
        'dat_dir': dat_dir,
        'config_dir': config_dir,
        'defaults_file': defaults_file,
    }


def console(class_name, parameters_file):
    import argparse

    data = read_json(parameters_file)
    description = data['description']
    parameters = convert_types(data['parameters'])

    # Processing arguments:
    required_args = []
    optional_args = []

    for key in sorted(parameters.keys()):
        if parameters[key]['default'] is None:
            required_args.append(key)
        else:
            optional_args.append(key)

    parser = argparse.ArgumentParser(description=description)

    for key in required_args + optional_args:
        args = []
        if 'short_argument' in parameters[key]:
            args.append('-{}'.format(parameters[key]['short_argument']))
        args.append('--{}'.format(key))

        kwargs = {
            'dest': key,
            'default': parameters[key]['default'],
            'required': False,
            'type': parameters[key]['type'],
            'help': '{}.'.format(parameters[key]['help']),
        }
        if parameters[key]['default'] is None:
            kwargs['required'] = True

        if parameters[key]['type'] == bool:
            kwargs['action'] = 'store_true'
            del (kwargs['type'])

        if parameters[key]['type'] == str:
            pass

        if parameters[key]['type'] in [list, tuple]:
            kwargs['type'] = parameters[key]['element_type']
            kwargs['nargs'] = '*'  # '*' - zero or more elements, '+' - one or more elements

        parser.add_argument(*args, **kwargs)

    args = parser.parse_args()
    for key in args.__dict__.keys():
        if type(args.__dict__[key]) == str and args.__dict__[key] == 'None':
            args.__dict__[key] = None

    class_name(**args.__dict__)


def convert_types(input_dict):
    """Convert types of values from specified JSON file."""
    # Eval `type` and `element_type` first:
    for key in input_dict.keys():
        if input_dict[key]['type'] == 'tuple':
            input_dict[key]['type'] = 'list'
        for el_key in ['type', 'element_type']:
            if el_key in input_dict[key].keys():
                input_dict[key][el_key] = eval(input_dict[key][el_key])

    # Convert values:
    for key in input_dict.keys():
        if 'default' in input_dict[key].keys() and input_dict[key]['default'] is not None:
            if 'element_type' in input_dict[key].keys():
                if input_dict[key]['type'] == list:
                    for i in range(len(input_dict[key]['default'])):
                        input_dict[key]['default'][i] = input_dict[key]['element_type'](input_dict[key]['default'][i])
            else:
                input_dict[key]['default'] = input_dict[key]['type'](input_dict[key]['default'])

    return input_dict


def create_cli_function(function_name, parameters, config):
    """The function creates the content of the CLI functions with the input from JSON config.

    Args:
        function_name (str): name of the function.
        parameters (dict): dictionary with the parameters of the arguments (default value, help info, type).
        config (dict): dictionary with the parameters (descriptions, used class name, returns, parameters (optional)).

    Returns:
        str: resulted function represented as a string.
    """

    # argh_decorators:
    argh_args = ''
    argh_kwargs = ''
    for key in sorted(parameters.keys()):
        if parameters[key]['default'] is None:
            if parameters[key]['type'] in [list, tuple]:
                argh_args += "@argh.arg('{}', nargs='*', type={})\n".format(key,
                                                                            parameters[key]['element_type'].__name__)
            else:
                argh_args += "@argh.arg('{}', type={})\n".format(key, parameters[key]['type'].__name__)
        else:
            if parameters[key]['type'] in [list, tuple]:
                argh_kwargs += "@argh.arg('--{}', nargs='+', type={})\n".format(key, parameters[key][
                    'element_type'].__name__)
        if 'choices' in parameters[key]:
            argh_kwargs += "@argh.arg('--{}', choices=[{}])\n".format(
                key,
                ', '.join(["\'{}\'".format(x) for x in parameters[key]['choices'].keys()])
            )
    argh_decorators = '{}{}'.format(argh_args, argh_kwargs)

    # function_arguments:
    str_args = ''
    str_kwargs = ''
    for key in sorted(parameters.keys()):
        a = parameters[key]['default']
        if parameters[key]['default'] is None:
            str_args += '    {},\n'.format(key)
            continue
        if parameters[key]['type'] == str:
            a = "\'{}\'".format(parameters[key]['default'])
        str_kwargs += '    {}={},\n'.format(key, a)
    function_arguments = '\n{}{}'.format(str_args, str_kwargs)

    # descriptions:
    description_short = config['description_short']
    description_long = config['description_long']

    # arguments_description:
    arguments_description = ''
    for key in sorted(parameters.keys()):
        format_str = '        {} ({}): {}.\n'
        format_values = [
            key,
            parameters[key]['type'].__name__,
            parameters[key]['help'],
        ]
        if 'choices' in parameters[key]:
            format_str = '        {} ({}): {} ({}).\n'
            choices_str = ''
            comma = ', '
            for i, choices_key in enumerate(sorted(parameters[key]['choices'].keys())):
                if i == len(parameters[key]['choices'].keys()) - 1:
                    comma = ''
                choices_str += "``{}`` - {}{}".format(choices_key, parameters[key]['choices'][choices_key], comma)
            format_values.append(choices_str)
        arguments_description += format_str.format(*format_values)

    # class_name:
    class_name = config['class_name']

    # class_arguments:
    class_arguments = ''
    for key in sorted(parameters.keys()):
        class_arguments += '        {}={},\n'.format(key, key)

    # return_dict
    return_dict = ''
    if type(config['returns']) == list:
        for r in config['returns']:
            return_dict += "        '{}': c.{},\n".format(r, r)
        return_dict = '{{\n{}    }}'.format(return_dict)
    else:
        return_dict = config['returns']

    v = {
        'argh_decorators': argh_decorators,
        'function_name': function_name,
        'function_arguments': function_arguments,
        'description_short': description_short,
        'description_long': description_long,
        'arguments_description': arguments_description,
        'class_name': class_name,
        'class_arguments': class_arguments,
        'return_dict': return_dict,
    }
    return pkjinja.render_resource('cli_function', v)


def get_cli_functions(config):
    """Get list of CLI functions' content with the input from JSON config.

    Args:
        config (dict): dictionary with the configuration in JSON format.

    Returns:
        list: list of functions' contents.
    """
    functions_list = []
    for key in config['cli_functions'].keys():
        if 'parameters' in config['cli_functions'][key]:
            parameters = convert_types(config['cli_functions'][key]['parameters'])
        else:
            parameters = convert_types(config['parameters'])
        content = create_cli_function(key, parameters, config['cli_functions'][key])
        functions_list.append(content)
    return functions_list


def read_json(file_name):
    try:
        with open(file_name, 'r') as f:
            data = json.load(f)
    except IOError:
        raise Exception('The specified file <{}> not found!'.format(file_name))
    except ValueError:
        raise Exception('Malformed JSON file <{}>!'.format(file_name))
    return data
