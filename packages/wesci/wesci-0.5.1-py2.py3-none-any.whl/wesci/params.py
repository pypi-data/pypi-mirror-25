import decimal
import json
import numbers
from pandas import DataFrame
import six
import warnings
from wesci.hash import Hash
from wesci.imports import StringIO


class Params(object):
    DEFAULT_INPUT_PARAMS_NAME = 'input_params'
    DEFAULT_OUTPUT_PARAMS_NAME = 'output_params'
    DATAFRAME_MAX_SIZE = 10

    @staticmethod
    def generate_data_for_log(params):
        return Params.__validate_and_transform_params(params)

    @staticmethod
    def __validate_and_transform_params(params):
        res = {}
        for name, val in params.items():
            param_dict = Params.__to_dict(val)
            if Params.__can_be_json_encoded(param_dict):
                res[name] = param_dict
            else:
                Params.__warn_about_non_valid_param(name, param_dict['type'])
        return res

    @staticmethod
    def __to_dict(val):
        param_hash = None
        param_metadata = None
        # To prevent empty strings in DynamoDB, we need to encode to json
        # the following types: string, list, set, dict, tuple
        is_val_json = False
        if isinstance(val, numbers.Number):
            if isinstance(val, decimal.Decimal):
                param_val = float(val)
            else:
                param_val = val
            param_type = 'number'
        elif isinstance(val, six.string_types):
            param_val = json.dumps(val, indent=4)
            is_val_json = True
            param_type = 'string'
        elif isinstance(val, list):
            param_val = json.dumps(val, indent=4)
            is_val_json = True
            param_type = 'list'
        elif isinstance(val, dict):
            param_val = json.dumps(val, indent=4)
            is_val_json = True
            param_type = 'dictionary'
        elif isinstance(val, tuple):
            param_val = json.dumps(val, indent=4)
            is_val_json = True
            param_type = 'tuple'
        elif isinstance(val, set):
            param_val = json.dumps(list(val), indent=4)
            is_val_json = True
            param_type = 'set'
        elif isinstance(val, DataFrame):
            param_val = val.iloc[:Params.DATAFRAME_MAX_SIZE,
                                 :Params.DATAFRAME_MAX_SIZE]
            param_val = param_val.to_string()
            is_val_json = False
            param_type = 'pandas dataframe'
            param_hash = Hash.hash(val.to_string().encode('ascii'))
            param_metadata = Params.__get_pandas_dataframe_info(val)
        else:
            param_val = val
            is_val_json = False
            param_type = type(val).__name__
        return {
            'hash': param_hash,
            'metadata': param_metadata,
            'value': param_val,
            'is_val_json': is_val_json,
            'type': param_type}

    @staticmethod
    def __get_pandas_dataframe_info(dataframe):
        info = StringIO()
        dataframe.info(buf=info)
        return info.getvalue()

    @staticmethod
    def __can_be_json_encoded(val):
        try:
            json.dumps(val)
            return True
        except Exception:
            return False

    @staticmethod
    def __warn_about_non_valid_param(name, param_type):
        message = "Param '%s' of type %s isn't "\
                  "supported yet and wasn't logged"\
                  % (name, param_type)
        warnings.formatwarning = Params.__warning_formatter
        warnings.warn(message, UserWarning, 7)

    @staticmethod
    def __warning_formatter(message, category, filename, lineno, line):
        return "WARNING: [%s:%s] %s\n" % (filename, lineno, str(message))
