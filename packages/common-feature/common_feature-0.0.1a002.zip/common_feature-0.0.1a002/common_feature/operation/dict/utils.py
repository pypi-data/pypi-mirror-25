#!/usr/bin/env python
# -*- coding: utf-8 -*-


def _check_key_dict(_dict, _dict_keys_needed):
    for _dict_keys_needed in _dict_keys_needed:
        try:
            _dict[_dict_keys_needed]
        except:
            return False, "", "%s missing" % _dict_keys_needed
    return True, "", ""


def dict_fetchall(cursor):
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]


def get_choice_map(choices, key_value=True):
    """
    Given a CHOICE (e.g. CHOICE_DEFAULT_STATUS), return a dictionary mapping the key to value (or reverse if key_value = False

    e.g.
    DEFAULT_STATUS_CHOICES = (
        ('A', 'Active'),
        ('I', 'Inactive'),
    )

    common_utils.get_choice_map(DEFAULT_STATUS_CHOICES, True)

    returned value is:
    {
        'A': 'Active',
        'I': 'Inactive'
    }
    """
    map = {}
    for choice in choices:
        if key_value:
            map[choice[0]] = choice[1]
        else:
            map[choice[1]] = choice[0]
    return map