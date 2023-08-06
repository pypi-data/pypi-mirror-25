"""
This module contains classes implementing the actions and structures
to get the results from the html page, or part of html page.
Classes describing the structure:
    - KeysRealtions; #A class describes the relationship keys or columns.
Classes describing the actions:
    - gtexts; #A class describes the action to get the text of the html item.
    - gattrs; #A class describes the action to get the value attribute of the page element.
    - gvalues; #A class describes the action to get the values for keyvalues pattern from html page.
"""
from functools import reduce
from operator import xor

from .actions import Action

# The string is passed to gvalues as KeysRelationships to produce a dictionary with original keys.
SOURCE_KEYS = 'source_keys'


"""
                                        Structure classes.
==================================================================================================
"""


class KeyRealtionships:
    """
    A class describes the relationship keys or columns.
    The class is the implementation of Hashed dictionary.
    A class used composite pattern.

    keys -> origin names of keys or columns;
    values -> target names of keys or columns;

    For the iteration used method items() of dictionary.
    """
    def __init__(self, relations):
        self.relations = relations

    def __hash__(self):
        hashed_keys = map(hash, self.relations.keys())
        hashed_values = map(hash, self.relations.values())
        return reduce(xor, hashed_keys) ^ reduce(xor, hashed_values)

    def __len__(self):
        return len(self.relations.keys())

    def __getitem__(self, key):
        return self.relations[key]

    def __repr__(self):
        return str(self.relations)

    def __str__(self):
        return str(self.relations)

    def __iter__(self):
        for key, value in self.relations.items():
            yield key, value
        return

    def keys(self):
        """
        Get keys as lists.
        """
        return self.relations.keys()


"""
                                        Action classes.
==================================================================================================
"""


class gtexts(Action):
    """
    A class describes the action to get the text of the html item.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialization action.
        """
        super().__init__(*args, **kwargs)
        if 'separator' in kwargs:
            del self.kwargs['separator']
        self.separator = kwargs.get('separator') or ''

    def __call__(self, parent, key=None):
        """
        Run action.
        Input:
            parent -> tuple of url, BeautifulSoup Tag of parent;
            key -> Key of result dictionary;
        Output:
            result -> if key is not None then dict(key: result_list)
                      else result_list.
                      result_list is list with result texts from html elements;
        """
        parent_url, parent_tag = parent
        result_list = [tag.get_text(separator=self.separator).strip() for tag in
                       parent_tag.find_all(*self.args, **self.kwargs)
                       if self.filter_function(parent_url, tag)]
        result = result_list if len(result_list) > 1 else (result_list[0] if result_list else None)
        return {key: result} if key else result


class gattrs(Action):
    """
    A class describes the action to get the value attribute of the page element.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialization action.
        Input:
            ....
            target_attribute -> Name of target attribute from html element;
        """
        super().__init__(*args, **kwargs)
        if 'target_attribute' in kwargs:
            del self.kwargs['target_attribute']
        self.target_attribute = kwargs.get('target_attribute') or 'alt'

    def __call__(self, parent, key=None):
        """
        Run action.
        Input:
            parent -> tuple of url, BeautifulSoup Tag of parent;
            key -> Key of result dictionary;
        Output:
            result -> if key is not None then dict(key: result_list)
                      else result_list.
                      result_list is list with value of attribute from html elements;
        """
        parent_url, parent_tag = parent
        result_list = [tag[self.target_attribute]
                       for tag in parent_tag.find_all(*self.args, **self.kwargs)
                       if self.filter_function(parent_url, tag)]
        result = result_list if len(result_list) > 1 else (result_list[0] if result_list else None)
        return {key: result} if key else result


class gvalues:
    """
    A class describes the action to get the values for keyvalues pattern from html page.
    """
    def __init__(self, keys_action, values_action):
        """
        Initialization action.
        keys_action -> Action for get keys;
        values_action -> Action for get values;
        """
        self.keys_action = keys_action
        self.values_action = values_action

    def __call__(self, parent, keys_relations):
        """
        Run action.
        Input:
            parent -> tuple of url, BeautifulSoup Tag of parent;
            keys_relations -> Relationships of key. Object of KeyRealtionships
                              or constants such as SOURCE_KEYS;
        Output:
            result -> Dictionary of result;
        """
        result_dict = None
        if keys_relations == SOURCE_KEYS:
            result_dict = {key: value for key, value in zip(self.keys_action(parent),
                                                            self.values_action(parent))}
        else:
            print('Get result from ', parent[0])
            result_dict = {keys_relations[key]: value
                           for key, value in zip(self.keys_action(parent),
                                                 self.values_action(parent))
                           if key in keys_relations.keys()}
        result_dict['url'] = parent[0]
        return result_dict
