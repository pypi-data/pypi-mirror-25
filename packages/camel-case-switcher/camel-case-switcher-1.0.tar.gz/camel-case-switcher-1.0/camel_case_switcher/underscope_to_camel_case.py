def underscope_to_camel_case(underscope_string: str, leading_upper_if_not_private: bool = False) -> str:
    result = ''
    i = 0
    if (i < len(underscope_string)):
        if (underscope_string[i] == '_'):
            i += 1
            s = underscope_string[i]
        elif (leading_upper_if_not_private):
            s = underscope_string[i].upper()
        else:
            s = underscope_string[i].lower()

        result += s
        i += 1

    while (i < len(underscope_string)):
        s = underscope_string[i]
        if (s == '_'):
            result += underscope_string[i + 1].upper()
            i += 1
        else:
            result += s.lower()
            
        i += 1

    return result
underscopeToCamelCase = underscope_to_camel_case
UnderscopeToCamelCase = underscope_to_camel_case
