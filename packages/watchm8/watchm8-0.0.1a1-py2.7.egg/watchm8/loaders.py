# -*- coding: utf-8 -*-


def file_loader(config_file):
    '''
    Load config from YAML file

    Args:
        config_file: String path to config file

    Returns:
        Result of yaml.load

    Raises:
        KeyError: If 'jobs' key not defined in config
    '''
    from yaml import load

    with open(config_file, 'r') as fh:
        config = load(fh.read())

    if 'jobs' not in config:
        raise KeyError('No jobs defined. "jobs" key missing.')

    return config
