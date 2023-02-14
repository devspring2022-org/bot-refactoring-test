import re


def dict_has_keys(d: dict, k: list) -> bool:
    for key in k:
        if key not in d.keys():
            return False
    return True

def match_list(string: str, reg_list: list) -> bool:
    for regular_string in reg_list:
        if re.fullmatch(regular_string, string):
            return True
    return False
