import ast
import collections
import os
import itertools

from nltk import pos_tag


def get_filepaths(dirpath):
    filepaths = []
    for root, dirs, files in os.walk(dirpath, topdown=True):
        python_files_list = [f for f in files if f.endswith(".py")]
        for file in python_files_list:
            filepaths.append(os.path.join(root, file))
    return filepaths


def get_file_content_list(filepaths):
    files_content_list = []
    for filename in filepaths:
        with open(filename, 'r', encoding='utf-8') as attempt_handler:
            main_file_content = attempt_handler.read()
        files_content_list.append(main_file_content)
    return files_content_list


def get_trees(files_content_list):
    trees = []
    for file_content in files_content_list:
        try:
            tree = ast.parse(file_content)
        except SyntaxError:
            tree = None
        trees.append(tree)
    return trees


def get_func_names_from_trees(trees):
    func_names_list = []
    for tree in trees:
        func_name = [node.name.lower() for node in ast.walk(tree)
                     if isinstance(node, ast.FunctionDef)]
        func_names_list.append(func_name)
    return func_names_list


def get_vars_names(trees):
    vars_names_list = []
    for tree in trees:
        vars_names = [node.id for node in ast.walk(tree)
                      if (isinstance(node, ast.Name) and
                          not isinstance(node.ctx, ast.Load) and
                          not isinstance(node, ast.FunctionDef) and
                          not node.id.isupper())
                      ]
        vars_names_list.append(vars_names)
    return list(itertools.chain.from_iterable(vars_names_list))


def filtering_funcs(func_names_list):
    func_names_list = list(itertools.chain.from_iterable(func_names_list))
    clear_funcs_list = [f for f in func_names_list
                        if not (f.startswith('__') and f.endswith('__'))]
    return clear_funcs_list


def verb_check(word):
    if word:
        pos_info = pos_tag([word])
        word_type = pos_info[0][1]
        return word_type == 'VB'


def get_funcs_and_vars_names(projects):
    clear_funcs_names_list = []
    for project in projects:
        filepaths = get_filepaths(project)
        files_content_list = get_file_content_list(filepaths)
        trees = get_trees(files_content_list)
        vars_names = get_vars_names(trees)
        func_names = get_func_names_from_trees(trees)
        filtred_func_names = filtering_funcs(func_names)
        clear_funcs_names_list.append({'project': project,
                                       'funcs': filtred_func_names,
                                       'vars': vars_names})
    return clear_funcs_names_list


def get_top_names(clear_funcs_names_list, output_choice):
    funcs_list = []
    for s in clear_funcs_names_list:
        funcs_list += s[output_choice]
    return collections.Counter(funcs_list)
