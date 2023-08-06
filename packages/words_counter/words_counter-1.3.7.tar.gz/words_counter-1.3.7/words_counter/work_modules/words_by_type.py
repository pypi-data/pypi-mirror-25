import itertools
import collections
from nltk import pos_tag


def type_check(word):
    if word:
        pos_info = pos_tag([word])
        word_type = pos_info[0][1]
        return word_type


def get_words_in_funcs_list(funcs_list, word_type):
    verbs = []
    for function_name in funcs_list:
        verbs.append([word for word in function_name.split('_')
                      if type_check(word) in word_type])
    cleared_verbs_list = list(itertools.chain.from_iterable(verbs))
    return collections.Counter(cleared_verbs_list)


def get_words_by_type(clear_func_names, word_type):
    words = []
    for func in clear_func_names:
        words_in_func = get_words_in_funcs_list(func['funcs'], word_type)
        words_in_vars = get_words_in_funcs_list(func['vars'], word_type)
        words.append({'project': func['project'],
                      'words_in_func': words_in_func,
                      'words_in_vars': words_in_vars})
    return words
