import logging
import sys

logger = logging.getLogger('pandascore')
logger.addHandler(logging.StreamHandler(sys.stderr))
logger.setLevel(logging.INFO)


def format_params(valid_params=None, **params):
    """
        This function formats filter and range params and logs then removes
        invalid params from dict
    """
    formatted_params = dict()

    for param in params:
        if param not in valid_params:
            logger.info("%s is an invalid parameter for this API call", param)
        elif params[param] is None:
            continue
        else:
            formatted_params[param] = params[param]

    if formatted_params.get('filter'):
        for filter_value in formatted_params.get('filter').split(';'):
            key, val = filter_value.split('=')
            filter_key = 'filter[{}]'.format(key)
            formatted_params[filter_key] = val
        del formatted_params['filter']
    if formatted_params.get('range'):
        for range_value in formatted_params.get('range').split(';'):
            key, val = range_value.split('=')
            range_key = 'range[{}]'.format(key)
            formatted_params[range_key] = val
        del formatted_params['range']
    return formatted_params
