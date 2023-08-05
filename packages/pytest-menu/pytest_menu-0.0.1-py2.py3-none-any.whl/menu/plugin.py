import pytest
from collections import OrderedDict, namedtuple

import npyscreen, curses


def pytest_addoption(parser):
    parser.addoption("--menu", action="store_true",
                     dest='menu',
                     help="enable menu selection of tests")

def ask_user(*args, choices=[], name=""):
    """ Ask the user for a choice """
    def _ask(*args, **kwargs):
        F = npyscreen.Form(name=name)
        choice = F.add_widget(npyscreen.MLTreeMultiSelect, values=choices)
        F.edit()
        return choice.get_selected_objects()
    return curses.wrapper(_ask)

def add_children(tree_head, tree):
    """ Push the testtree into a npyscreen.NPSTreeData object """
    for i,v in tree.items():
        if type(v) == dict:
            th = tree_head.newChild(content=i)
            add_children(th, v)
        else:
            x = tree_head.newChild(content=i)
            x.test_case = v

@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(session, config, items):
    if not (config.option.menu and items):
        return

    capman = config.pluginmanager.getplugin("capturemanager")
    if capman:
        capman.suspendcapture(in_=True)

    tests = {}
    for test_item in items:
        t = tests
        path = get_path(test_item)
        for layer in path[:-1]:
            if layer not in t:
                t[layer] = {}
            t = t[layer]
        assert not path[-1] in t # This would mean we have to test cases with the same name an path, should not be possible
        t[path[-1]] = test_item

    test_tree = npyscreen.NPSTreeData(content=session.name, ignoreRoot=False)
    add_children(test_tree, tests)
    test_choices = ask_user(choices=test_tree, name="Test Selection")

    test_cases = []
    for i in test_choices:
        test_cases += i.walkTree()
    test_cases = [x.test_case for x in test_cases if hasattr(x, "test_case")]
    test_cases = [x for x in test_cases if type(x) == pytest.Function]
    items[:] = test_cases # Set pytest item list to selected test cases

def get_path(item):
    """ Get the name of all parents of a pytest object """
    path = []
    chain = item.listchain()
    for i in chain:
        if hasattr(i, "_obj") and hasattr(i._obj, "__name__"): # Session and Instance don't have i.obj
            name = i._obj.__name__
            if '.' in name and isinstance(i, pytest.Module):
                name = name.split('.')[-1]
            elif isinstance(i, pytest.Item):
                name = i.name
                if name.endswith("]"):
                    path.append(name.split('[')[0])
            path.append(name)
    return path
