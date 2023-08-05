import ast
import os
import collections
import argparse
from nltk import pos_tag

PROJECTS = [
    'django',
    'flask',
    'pyramid',
    'reddit',
    'requests',
    'sqlalchemy',
]


def get_all_projects(addon_projects):
    all_projects = []
    for project in addon_projects:
        if project.lower() not in PROJECTS:
            all_projects.append(project.lower())
    return all_projects+PROJECTS


def get_existing_projects(all_projects):
    existing_projects = []
    for project in all_projects:
        dirpath = os.path.join('.', project)
        if os.path.exists(dirpath):
            existing_projects.append(dirpath)
    return existing_projects


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


def get_all_names(trees):
    all_names = []
    for tree in trees:
        all_names.append(node.id for node in ast.walk(tree)
                         if isinstance(node, ast.Name))
    return all_names


def get_func_names(trees):
    func_names_list = []
    for tree in trees:
        func_name = [node.name.lower() for node in ast.walk(tree)
                     if isinstance(node, ast.FunctionDef)]
        func_names_list.append(func_name)
    return func_names_list


def filtering_funcs(func_names_list):
    clear_funcs_list = [f for f in func_names_list
                        if not (f.startswith('__') and f.endswith('__'))]
    return clear_funcs_list


def verb_check(word):
    pos_info = pos_tag([word])
    word_type = pos_info[0][1]
    return word_type == 'VB'


def print_all_project_funcs_names(funcs_names_list):
    print('All funcs names:')
    for func in funcs_names_list:
        print('"{func}"'.format(func=func))


def print_total_funcs_names_info(all_funcs_names):
    print('total funcs names: {count}\nunique funcs names: {unique}'.format(
        count=len(all_funcs_names), unique=len(set(all_funcs_names))))


def print_verbs_info(top_verbs):
    print('total verbs: {words}\nunique verbs: {unique}'.format(
        words=len(top_verbs), unique=len(set(top_verbs))))
    for word, occurence in collections.Counter(
            top_verbs).most_common():
        print('"{verb}" in {occurence} projects'.format(verb=word,
                                                        occurence=occurence))


def create_parser_for_user_arguments():
    parser = argparse.ArgumentParser(description='Work with funcs names.')
    parser.add_argument('-a', '--all_names', action='store_true',
                        help='Print ')
    parser.add_argument('-p', '--projects', nargs='+', required=False,
                        type=str, help='Adding projects')
    return parser.parse_args()


def output_to_cli():
    user_argument = create_parser_for_user_arguments()
    if user_argument.projects:
        all_projects = get_all_projects(user_argument.projects)
    else:
        all_projects = PROJECTS
    top_verbs = []
    all_funcs_names = []
    existing_projects = get_existing_projects(all_projects)
    for project in existing_projects:
        print('dirpath: {dirpath}:'.format(dirpath=project))
        filepaths = get_filepaths(project)
        print('total ".py" files count: {count}'.format(count=len(filepaths)))
        files_content_list = get_file_content_list(filepaths)
        trees = get_trees(files_content_list)
        func_names = get_func_names(trees)
        funcs_names_list = sum(func_names, [])
        clear_func_names_list = filtering_funcs(funcs_names_list)
        if user_argument.all_names:
            print_all_project_funcs_names(funcs_names_list)
        verbs = []
        for function_name in clear_func_names_list:
            verbs.append([word for word in function_name.split('_')
                          if verb_check(word)])
        verbs_counter = collections.Counter(sum(verbs, []))
        for verb in verbs_counter:
            print('verb "{verb}" count: {count}'.format(
                verb=verb, count=verbs_counter[verb]))
        all_funcs_names += funcs_names_list
        top_verbs += verbs_counter
        print('------------')
    if user_argument.all_names:
        print_total_funcs_names_info(all_funcs_names)
    print_verbs_info(top_verbs)


if __name__ == '__main__':
    output_to_cli()
