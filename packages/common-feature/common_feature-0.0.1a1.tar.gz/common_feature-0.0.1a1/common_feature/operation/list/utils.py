#!/usr/bin/env python
# -*- coding: utf-8 -*-


def _check_key_list(_lists, _lists_keys_needed):
    for _list in _lists_keys_needed:
        if _list not in _lists:
            return False, "", "%s missing" % _list
    return True, "", ""


def _compare_list_with_display_fields(lists, display_fields, fields):
    if len(fields) == len(display_fields):
        new_dicts = dict(zip(fields, display_fields))
        new_dicts2 = {}
        new_dicts3 = {}
        for display_field in display_fields:
            new_dicts2[display_field] = lists.index(display_field)
        for new_dict in new_dicts:
            for new_dict2 in new_dicts2:
                if new_dicts[new_dict] == new_dict2:
                    new_dicts3[new_dict] = new_dicts2[new_dict2]
        return new_dicts3  # key: value
    else:
        return {}