
import argparse
import os
import shutil
import unittest
from io import StringIO
from unittest import TestCase
from unittest.mock import patch, mock_open

from words_counter.words_counter import main


class TestInfoOutputToCli(TestCase):
    def setUp(self):
        os.mkdir('myproject')
        os.mkdir('myproject/myproject2')
        test_verb_func_1 = 'def get_data():\n   test_var="test_value"'
        test_verb_func_2 = 'def give_content():\n    pass'
        test_not_verb_func_1 = 'def check_data():\n    pass'
        test_not_verb_func_2 = 'def output_content():\n    test_var2="test_value2"'
        with patch("__main__.open", mock_open()):
            with open('myproject/app_file.py', 'w') as file1:
                file1.write(test_verb_func_1 + '\n' + test_not_verb_func_2)
            with open('myproject/myproject2/app_file3.py', 'w') as file2:
                file2.write(test_verb_func_2 + '\n' + test_not_verb_func_1)

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(projects=['myproject'],
                                           all_names=True, by_type=False,
                                           clone=False, top_names=False,
                                           type=['VB'], download=False,
                                           data_type='funcs', cli=True,
                                           json=False, csv=False))
    def test_output_to_cli_all_funcs_and_vars_names(self, mock_args):
        expected_result = '\nproject: myproject' \
                          '\nfuncs names:\n' \
                          '\t get_data\n' \
                          '\t output_content\n' \
                          '\t give_content\n' \
                          '\t check_data\n' \
                          'vars names:\n' \
                          '\t test_var\n' \
                          '\t test_var2\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            self.assertEqual(fake_out.getvalue(), expected_result)

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(projects=['myproject'],
                                           all_names=False, by_type=True,
                                           clone=False, top_names=False,
                                           type=['VB'], download=False,
                                           data_type='funcs', cli=True,
                                           json=False, csv=False))
    def test_verbs_in_all_names(self, mock_args):
        expected_result = '\nproject: myproject' \
                          '\nwords in funcs:\n' \
                          '\t"get" count: 1\n' \
                          '\t"give" count: 1\n' \
                          'words in vars:\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            self.assertEqual(fake_out.getvalue(), expected_result)

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(projects=['myproject'],
                                           all_names=False, by_type=True,
                                           clone=False, top_names=False,
                                           type=['NN'], download=False,
                                           data_type='funcs', cli=True,
                                           json=False, csv=False))
    def test_noun_in_all_names(self, mock_args):
        expected_result = '\nproject: myproject' \
                          '\nwords in funcs:\n' \
                          '\t"output" count: 1\n' \
                          '\t"content" count: 2\n' \
                          '\t"check" count: 1\n' \
                          'words in vars:\n' \
                          '\t"test" count: 2\n' \
                          '\t"var" count: 1\n' \
                          '\t"var2" count: 1\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
        self.assertEqual(fake_out.getvalue(), expected_result)

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(projects=['myproject'],
                                           all_names=False, by_type=True,
                                           clone=False, top_names=False,
                                           type=['VB', 'NN', 'NNS'], download=False,
                                           data_type='funcs', cli=True,
                                           json=False, csv=False))
    def test_all_words_types_in_all_names(self, mock_args):
        expected_result = '\nproject: myproject' \
                          '\nwords in funcs:\n' \
                          '\t"get" count: 1\n' \
                          '\t"data" count: 2\n' \
                          '\t"output" count: 1\n' \
                          '\t"content" count: 2\n' \
                          '\t"give" count: 1\n' \
                          '\t"check" count: 1\n' \
                          'words in vars:\n' \
                          '\t"test" count: 2\n' \
                          '\t"var" count: 1\n' \
                          '\t"var2" count: 1\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            self.assertEqual(fake_out.getvalue(), expected_result)

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(projects=['myproject'],
                                           all_names=False, by_type=False,
                                           clone=False, top_names=True,
                                           type=['VB', 'NN', 'NNS'], download=False,
                                           data_type='funcs', cli=True,
                                           json=False, csv=False))
    def test_funcs_names_count(self, mock_args):
        expected_result = '"get_data" count: 1\n' \
                          '"output_content" count: 1\n' \
                          '"give_content" count: 1\n' \
                          '"check_data" count: 1\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            self.assertEqual(fake_out.getvalue(), expected_result)

    @patch('argparse.ArgumentParser.parse_args',
           return_value=argparse.Namespace(projects=['myproject'],
                                           all_names=False, by_type=False,
                                           clone=False, top_names=True,
                                           type=['VB', 'NN', 'NNS'], download=False,
                                           data_type='vars', cli=True,
                                           json=False, csv=False))
    def test_vars_names_count(self, mock_args):
        expected_result = '"test_var" count: 1\n' \
                          '"test_var2" count: 1\n'
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            self.assertEqual(fake_out.getvalue(), expected_result)

    def tearDown(self):
        shutil.rmtree('myproject')

if __name__ == "__main__":
    unittest.main()