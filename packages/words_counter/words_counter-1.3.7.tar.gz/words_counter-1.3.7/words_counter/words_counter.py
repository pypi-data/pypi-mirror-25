import argparse
import csv
import json
import os
from itertools import chain
from six import string_types

from .work_modules import get_words_by_type, clone_repo_from_github, get_funcs_and_vars_names, get_top_names


def load_outsource_base_from_json():
    with open('outsource.json') as outsource_base:
        return json.load(outsource_base)


def choose_outsource(user_argument, outsource_base):
    url = user_argument[0]
    code_source = None
    for key, value in outsource_base.items():
        if key in url:
            code_source = value
            break
    if code_source == 'github':
        code_source = clone_repo_from_github
    return code_source


def get_existing_projects(all_projects):
    existing_projects = []
    for project in all_projects:
        if os.path.exists(project):
            existing_projects.append(project)
    return set(existing_projects)


def output_to_json_file(content, filepath):
    with open(filepath, 'w') as outfile:
        json.dump(content, outfile, ensure_ascii=False)


def create_parser_for_user_arguments():
    parser = argparse.ArgumentParser(description='Work with funcs names.')
    parser.add_argument('--all_names', action='store_true',
                        required=False, help='Get all vars and funcs names')
    parser.add_argument('--by_type', action='store_true',
                        required=False, help='Get all info by word type.')
    parser.add_argument('--top_names', action='store_true',
                        required=False, help='Get top names ')
    parser.add_argument('-t', '--type', nargs='+',
                        required=False, help='Add word type for search.'
                                             'Avaliable: NN, NNS, VB')
    parser.add_argument('-p', '--projects', nargs='+', required=False,
                        type=str, help='Add projects.')
    parser.add_argument('-d', '--download', nargs='+', required=False,
                        type=str, help='Clone code from outsource')
    parser.add_argument('--data_type', nargs='?', required=False,
                        type=str, help='Funcs or vars search')
    parser.add_argument('--cli', action='store_true',
                        required=False, help='Output to cli')
    parser.add_argument('--json', nargs='?', required=False,
                        type=str, help='Save to json file')
    parser.add_argument('--csv', nargs='?', required=False,
                        type=str, help='Save to csv file')
    return parser.parse_args()


def print_all_names(projects):
    for project in projects:
        print('\nproject: {prj}'.format(prj=project['project']))
        print('funcs names:')
        for func in project['funcs']:
            print('\t', func)
        print('vars names:')
        for var in project['vars']:
            print('\t', var)


def print_top_names(words):
    for word in words:
        print('"{word}" count: {count}'.format(
            word=word, count=words[word]))


def print_by_type(projects):
    for project in projects:
        print('\nproject: {prj}'.format(prj=project['project']))
        print('words in funcs:')
        for func in project['words_in_func']:
            print('\t"{word}" count: {count}'.format(
                word=func, count=project['words_in_func'][func]))
        print('words in vars:')
        for var in project['words_in_vars']:
            print('\t"{word}" count: {count}'.format(
                word=var, count=project['words_in_vars'][var]))


def output_to_csv(content, pathfile):
    # getting by https://github.com/vladikk/JSON2CSV
    with open(pathfile, "w") as pathfile:
        def build_row(dict_obj, keys):
            return [dict_obj.get(k, "") for k in keys]

        keys = sorted(set(chain.from_iterable([o.keys() for o in content])))
        rows = [build_row(d, keys) for d in content]
        cw = csv.writer(pathfile)
        cw.writerow(keys)
        for row in rows:
            cw.writerow([c if isinstance(c, string_types) else c for c in row])


def output_to_cli(content_for_output, content_type):
    if content_type == 'all_names':
        print_all_names(content_for_output)
    if content_type == 'top_names':
        print_top_names(content_for_output)
    if content_type == 'words_counter':
        print_by_type(content_for_output)


def main():
    user_argument = create_parser_for_user_arguments()
    if user_argument.download:
        outsource_base = load_outsource_base_from_json()
        outsource_choice = choose_outsource(user_argument.download,
                                            outsource_base)
        outsource_choice(user_argument.download)
    if user_argument.type:
        word_type = [word.upper() for word in user_argument.type]
        existing_projects = get_existing_projects(user_argument.projects)
        output_choice = user_argument.data_type
        projects_funcs_vars_names = get_funcs_and_vars_names(existing_projects)
        words_counter = get_words_by_type(projects_funcs_vars_names, word_type)
        top_names = get_top_names(projects_funcs_vars_names, output_choice)
        if user_argument.all_names:
            content_to_output = projects_funcs_vars_names
            content_type = 'all_names'
        if user_argument.top_names:
            content_to_output = top_names
            content_type = 'top_names'
        if user_argument.by_type:
            content_to_output = words_counter
            content_type = 'words_counter'
        if user_argument.cli:
            output_to_cli(content_to_output, content_type)
        if user_argument.json:
            output_to_json_file(content_to_output, user_argument.json)
        if user_argument.csv:
            output_to_csv(content_to_output, user_argument.csv)
    else:
        print('No arguments(verb_counter --help)')


if __name__ == '__main__':
    main()
