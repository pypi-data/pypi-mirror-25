"""String formatting and printing utilities"""

from __future__ import print_function
import os
import sys
from termcolor import colored, cprint


# Disable errors shown by pylint for invalid function name
# pylint: disable=C0103


def format_clowder_command(command):
    """Return formatted clowder command name"""
    return colored(command, attrs=['bold'])


def format_command(command):
    """Return formatted command name"""
    if isinstance(command, list):
        command_output = " ".join(command)
    else:
        command_output = command
    return colored('$ ' + command_output, attrs=['bold'])


def format_depth_error(depth, yaml_file):
    """Return formatted error string for invalid depth"""
    yaml_file = format_symlink_target(yaml_file)
    output_1 = format_path(yaml_file) + '\n'
    output_2 = colored(' - Error: ', 'red')
    output_3 = colored('depth', attrs=['bold'])
    output_4 = colored(' must be a positive integer\n', 'red')
    output_5 = colored('depth: ' + str(depth), attrs=['bold'])
    return output_1 + output_2 + output_3 + output_4 + output_5


def format_empty_yaml_error(yaml_file):
    """Return formatted error string for empty clowder.yaml"""
    yaml_file = format_symlink_target(yaml_file)
    output_1 = format_path(yaml_file) + '\n'
    output_2 = colored(' - Error: No entries in ', 'red')
    output_3 = format_yaml_file('clowder.yaml')
    return output_1 + output_2 + output_3


def format_remote_name_error(fork, project, remote):
    """Return formatted error string for fork with same remote as project"""
    # yaml_file = format_symlink_target(yaml_file)
    # output_1 = format_path(yaml_file) + '\n'
    output_1 = colored(' - Error: fork ', 'red')
    output_2 = colored(fork, attrs=['bold'])
    output_3 = colored(' and project ', 'red')
    output_4 = colored(project, attrs=['bold'])
    output_5 = colored(' have same remote name ', 'red')
    output_6 = colored(remote, attrs=['bold'])
    return output_1 + output_2 + output_3 + output_4 + output_5 + output_6


def format_fork_string(name):
    """Return formatted fork name"""
    return colored(name, 'cyan')


def format_invalid_entries_error(name, collection, yaml_file):
    """Return formatted error string for invalid entry in collection"""
    yaml_file = format_symlink_target(yaml_file)
    output_1 = format_path(yaml_file) + '\n'
    output_2 = colored(' - Error: No entries in ', 'red')
    output_3 = colored(name, attrs=['bold'])
    empty_output = output_1 + output_2 + output_3

    if isinstance(collection, list):
        return empty_output

    dict_entries = ''.join('{}: {}\n'.format(key, val)
                           for key, val in sorted(collection.items())).rstrip()
    length = len(collection)
    if length is 0:
        return empty_output
    elif length > 1:
        output_2 = colored(' - Error: Unknown entries in ', 'red')
    else:
        output_2 = colored(' - Error: Unknown entry in ', 'red')
    output_3 = colored(name + '\n\n' + str(dict_entries), attrs=['bold'])
    return output_1 + output_2 + output_3


def format_missing_entry_error(entry, name, yaml_file):
    """Return formatted error string for missing entry in dictionary"""
    yaml_file = format_symlink_target(yaml_file)
    output_1 = format_path(yaml_file) + '\n'
    output_2 = colored(' - Error: Missing ', 'red')
    output_3 = colored(str(entry), attrs=['bold'])
    output_4 = colored(' in ', 'red')
    output_5 = colored(str(name), attrs=['bold'])
    return output_1 + output_2 + output_3 + output_4 + output_5


def format_missing_imported_yaml_error(path, yaml_file):
    """Return formatted error string for missing imported clowder.yaml"""
    yaml_file = format_symlink_target(yaml_file)
    output_1 = format_path(yaml_file) + '\n'
    output_2 = colored(' - Error: Missing imported file\n', 'red')
    output_3 = format_path(path)
    return output_1 + output_2 + output_3


def format_not_list_error(name, yaml_file):
    """Return formatted error string for value that's not a list"""
    yaml_file = format_symlink_target(yaml_file)
    output_1 = format_path(yaml_file) + '\n'
    output_2 = colored(' - Error: ', 'red')
    output_3 = colored(name, attrs=['bold'])
    output_4 = colored(' type should be ', 'red')
    output_5 = colored('list', 'yellow')
    return output_1 + output_2 + output_3 + output_4 + output_5


def format_not_dictionary_error(name, yaml_file):
    """Return formatted error string for value that's not a dictionary"""
    yaml_file = format_symlink_target(yaml_file)
    output_1 = format_path(yaml_file) + '\n'
    output_2 = colored(' - Error: ', 'red')
    output_3 = colored(name, attrs=['bold'])
    output_4 = colored(' type should be ', 'red')
    output_5 = colored('dict', 'yellow')
    return output_1 + output_2 + output_3 + output_4 + output_5


def format_not_string_error(name, yaml_file):
    """Return formatted error string for value that's not a string"""
    yaml_file = format_symlink_target(yaml_file)
    output_1 = format_path(yaml_file) + '\n'
    output_2 = colored(' - Error: ', 'red')
    output_3 = colored(name, attrs=['bold'])
    output_4 = colored(' type should be ', 'red')
    output_5 = colored('str', 'yellow')
    return output_1 + output_2 + output_3 + output_4 + output_5


def format_not_bool_error(name, yaml_file):
    """Return formatted error string for value that's not a boolean"""
    yaml_file = format_symlink_target(yaml_file)
    output_1 = format_path(yaml_file) + '\n'
    output_2 = colored(' - Error: ', 'red')
    output_3 = colored(name, attrs=['bold'])
    output_4 = colored(' type should be ', 'red')
    output_5 = colored('bool', 'yellow')
    return output_1 + output_2 + output_3 + output_4 + output_5


def format_path(path):
    """Return formatted path"""
    return colored(path, 'cyan')


def format_ref_string(ref):
    """Return formatted ref name"""
    return colored('(' + ref + ')', 'magenta')


def format_invalid_ref_error(ref, yaml_file):
    """Return formatted error string for incorrect ref"""
    yaml_file = format_symlink_target(yaml_file)
    output_1 = format_path(yaml_file) + '\n'
    output_2 = colored(' - Error: ', 'red')
    output_3 = colored('ref', attrs=['bold'])
    output_4 = colored(' value ', 'red')
    output_5 = colored(ref, attrs=['bold'])
    output_6 = colored(' is not formatted correctly', 'red')
    return output_1 + output_2 + output_3 + output_4 + output_5 + output_6


def format_remote_string(remote):
    """Return formatted remote name"""
    return colored(remote, 'yellow')


def format_symlink_target(path):
    """Returns target path if input is a symlink"""
    if os.path.islink(path):
        return os.readlink(path)
    return path


def format_version(version_name):
    """Return formatted string for clowder.yaml version"""
    return colored(version_name, attrs=['bold'])


def format_yaml_file(yaml_file):
    """Return formatted string for clowder.yaml file"""
    return colored(yaml_file, 'cyan')


def print_command_failed_error(command):
    """Print error message for failed command"""
    output_1 = colored(' - Error: Failed to run command ', 'red')
    output_2 = format_command(command)
    print(output_1 + output_2 + '\n')


def print_error(error):
    """Print error message for generic exception"""
    print(str(error) + '\n')


def print_file_exists_error(path):
    """Print error message for already existing file"""
    output_1 = colored(' - Error: File already exists\n', 'red')
    output_2 = format_path(path)
    return output_1 + output_2


def print_invalid_yaml_error():
    """Print error message for invalid clowder.yaml"""
    clowder_output = format_yaml_file('clowder.yaml')
    print('\n' + clowder_output + ' appears to be invalid')


def print_missing_yaml_error():
    """Print error message for missing clowder.yaml"""
    clowder_output = format_yaml_file('clowder.yaml')
    print(clowder_output + ' appears to be missing')


def print_offline_error():
    """Print error message for no internet connection"""
    cprint('No available internet connection\n', 'red')
    sys.exit(1)


def print_open_file_error(path):
    """Print error message for failing to open file"""
    output_1 = colored(' - Error: Failed to open file\n', 'red')
    output_2 = format_path(path)
    return output_1 + output_2


def print_remote_already_exists_error(remote_name, remote_url, actual_url):
    """Print error message when remote already exists with different url"""
    message_1 = colored(' - Remote ', 'red')
    remote_output = format_remote_string(remote_name)
    message_2 = colored(' already exists with a different url', 'red')
    actual_url_output = format_path(actual_url)
    print(message_1 + remote_output + message_2)
    remote_url_output = format_path(remote_url)
    print(actual_url_output + ' should be ' + remote_url_output + '\n')


def print_save_file_error(path):
    """Print error message for failing to save file"""
    output_1 = colored(' - Error: Failed to save file\n', 'red')
    output_2 = format_path(path)
    return output_1 + output_2


def print_recursive_import_error(depth):
    """Print error message for too many recursive imports"""
    output_1 = colored(' - Error: Too many recursive imports\n', 'red')
    output_2 = colored(str(depth), attrs=['bold'])
    print(output_1 + 'Max imports: ' + output_2)


def print_save_version(version_name, yaml_file):
    """Print message for saving version"""
    output_1 = format_version(version_name)
    output_2 = format_path(yaml_file)
    print(' - Save version ' + output_1 + '\n' + output_2)


def print_save_version_exists_error(version_name, yaml_file):
    """Print error message previous existing saved version"""
    output_1 = colored(' - Error: Version ', 'red')
    output_2 = format_version(version_name)
    output_3 = colored(' already exists\n', 'red')
    output_4 = format_yaml_file(yaml_file)
    print(output_1 + output_2 + output_3 + output_4)


# http://stackoverflow.com/questions/16891340/remove-a-prefix-from-a-string
def remove_prefix(text, prefix):
    """Remove prefix from a string"""
    if text.startswith(prefix):
        return text[len(prefix):]
    return text
