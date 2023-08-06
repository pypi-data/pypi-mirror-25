from camel_case_switcher.camel_case_to_underscope import camel_case_to_underscope
from camel_case_switcher.underscope_to_camel_case import underscope_to_camel_case

def dict_keys_underscope_to_camel_case(dict_object, recursive=False, leading_upper_if_not_private: bool = None):
    if (not isinstance(dict_object, dict)):
        raise TypeError("Argument should be a normal dict")
    result = dict()

    for key in dict_object:
        new_key = key
        new_obj = dict_object[key]
        if (isinstance(key, str)):
            if (leading_upper_if_not_private is None):
                new_key = underscope_to_camel_case(new_key)
            else:
                new_key = underscope_to_camel_case(new_key, leading_upper_if_not_private=leading_upper_if_not_private)

        if (recursive and isinstance(new_obj, dict)):
            new_obj = dict_keys_underscope_to_camel_case(new_obj, recursive=recursive, leading_upper_if_not_private=leading_upper_if_not_private)

        result[new_key] = new_obj
    return result

def dict_keys_camel_case_to_underscope(dict_object, recursive=False, leading_lower_is_private:bool=None, process_acronyms=None):
    if (not isinstance(dict_object, dict)):
        raise TypeError("Argument should be a normal dict")
    result = dict()

    for key in dict_object:
        new_key = key
        new_obj = dict_object[key]
        if (isinstance(key, str)):

            if (leading_lower_is_private is None and process_acronyms is None):
                new_key = camel_case_to_underscope(new_key)
            elif (leading_lower_is_private is None):
                new_key = camel_case_to_underscope(new_key, process_acronyms=process_acronyms)
            elif (process_acronyms is None):
                new_key = camel_case_to_underscope(new_key, leading_lower_is_private=leading_lower_is_private)
            else:
                new_key = camel_case_to_underscope(new_key, process_acronyms=process_acronyms, leading_lower_is_private=leading_lower_is_private)

        if (recursive and isinstance(new_obj, dict)):
            new_obj = dict_keys_camel_case_to_underscope(new_obj, recursive=recursive, process_acronyms=process_acronyms, leading_lower_is_private=leading_lower_is_private)

        result[new_key] = new_obj
    return result