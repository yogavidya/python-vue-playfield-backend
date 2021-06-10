from functools import reduce
import inspect

def _attr_category(x):
    if x.startswith('__') and x.endswith('__'):
        return '"magic"'
    if x.startswith('__'):
        return 'mangling'
    if x.startswith('_'):
        return 'internal'
    if x.endswith('_'):
        return 'conflict'
    return 'public'

def _members_sort(acc, x):
    category_exists = any(node['name'] == x['category'] for node in acc)
    if category_exists:
        category = next(filter(lambda node: node['name'] == x['category'], acc))
        category['attributes'].append(x['name'])
    else:
        acc.append({'name': x['category'], 'attributes': [x['name']]})
    return acc

def members_names(x):
    members = [{'name': x[0], 'category': _attr_category(x[0])} 
              for x in inspect.getmembers(x)]
    result = reduce(_members_sort, members, list())
    return result

def is_iterable(x):
    try:
        _ = (e for e in x)
        return True
    except TypeError:
        return False

def is_hashable(x):
    try:
        _ = hash(x)
        return True
    except TypeError:
        return False
