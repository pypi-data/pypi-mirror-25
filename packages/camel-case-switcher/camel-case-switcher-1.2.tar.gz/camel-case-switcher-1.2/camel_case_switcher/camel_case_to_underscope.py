def camel_case_to_underscope(camel_case_string:str, leading_lower_is_private:bool=False, process_acronyms:bool=True) -> str:
    
    result = ''
    i = 0
    if (i < len(camel_case_string)):
        s = camel_case_string[i]
        if (leading_lower_is_private):
            if (s != s.upper()):
                s = '_' + s.lower()
            else:
                s = s.lower()
        else:
            s = s.lower()

        result += s
        i += 1

    while (i < len(camel_case_string)):
        s = camel_case_string[i]
        if (s != s.lower()):
            if (process_acronyms
                and (i < 1 or camel_case_string[i-1] != camel_case_string[i-1].lower())
                and (i + 1 >= len(camel_case_string) or camel_case_string[i+1] != camel_case_string[i+1].lower())):
                s = s.lower()
            else:
                s = '_' + s.lower()

        result += s
        i += 1

    return result
CamelCaseToUnderscope = camel_case_to_underscope
camelCaseToUnderscope = camel_case_to_underscope
