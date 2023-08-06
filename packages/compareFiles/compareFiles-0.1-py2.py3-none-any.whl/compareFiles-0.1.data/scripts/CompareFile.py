# -*- coding: utf-8 -*-
from subprocess import PIPE
import subprocess #https://docs.python.org/2/library/subprocess.html

import os
import copy
from robot.api import logger
class CompareFile():
    def __init__(self):
        self.option = [""]


    ROBOT_LIBRARY_DOC_FORMAT = 'ROBOT'
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    __version__ = '1.0.0'

    def compare_text_files(self,reference_file_path ,compare_file_path, result_file_path):
        """
         This keyword is used to compare text files with the options previously
         chosen by setting the "Ignore space options" and the "Set Context Lines" keywords.

             | *Argument* | *Description* | *Example* |
             | reference_file_path | reference file path | C:\\file1.txt |
             | compare_file_path |path of file to compare| C:\\file2.txt |
             | result_file_path |result file path C:\\outputFile.txt |
         Examples:
            | Compare Text Files  | ${FileReference} |   ${FileCompare} | ${Fileoutput} |
        """


        reference_file_path = self._assert_file_path(reference_file_path)
        compare_file_path = self._assert_file_path(compare_file_path)

        result_file_path = self._assert_directory_path(result_file_path)


        my_path = os.path.dirname(__file__)

        git_command = "git diff "

        path_converter_html = my_path+"\\diff2html.py "
        self._assert_file_path(path_converter_html)

        converter = "| python {}\\diff2html.py -o".format(my_path)


        option = ""
        for myoption in self.option:
            option = option+" " + myoption


        commande = '{} {} {} {} {} {}'.format(git_command,option , reference_file_path , compare_file_path,converter ,result_file_path)



        subprocess.call(commande,shell=True)



    def ignore_option_spaces(self,ignore_all_whitespace = False,ignore_blanklines=False,ignore_spaces_change = False ,ignore_spaces_at_end_of_lines=False):
        """
        This keyword is used to set the different options to ignore whitespace and blanklines.
        It should only be used before the "Compare Text Files" keyword.

        | *Argument* | *Description* | *Example* |
        | ignore_all_whitespace | choosing to ignore all whitespace | ${True}/${False} |
        | ignore_blankline | choosing to ignore blank lines | ${True}/${False} |
        | ignore_spaces_change | choosing to ignore spaces change | ${True}/${False} |
        | ignore_spaces_at_end_of_lines | choosing to ignore spaces at end of lines | ${True}/${False} |

        Examples:
            | Ignore Option Spaces | ${True}  |   ${True} |${False} |  ${False} |
        """

        if ignore_all_whitespace:
            self.option.append("-w")
        if ignore_blanklines:
            self.option.append("--ignore-blank-lines ")
        if ignore_spaces_change:
            self.option.append("-b")#
        if ignore_spaces_at_end_of_lines :
            self.option.append("--ignore-space-at-eol")




    def set_context_lines(self,line_number=False):
        """
         This keyword sets the number of context lines we want.
         It should only be used before the "Compare Text Files" keyword.
        | *Argument* | *Description* | *Example* |
        | line_number | the number of context lines to display | 03 |
        """
        line_number_str = "0"+str(int(line_number))
        self.option.append("--unified={}".format(line_number_str))

    def _assert_file_path(self, file_path):
        my_path= os.path.normpath(file_path)
        if os.path.isfile(my_path):
            return my_path
        else :
            raise AssertionError("Could not find a file '{}'".format(file_path))

    def _assert_directory_path(self, file_path):

        path_list = file_path.split(os.sep)
        if path_list[0] == file_path:
            path_list = file_path.split("/")


        my_list = copy.deepcopy(path_list)
        my_file = my_list[-1]
        my_file_splited = my_file.split(".")
        extension = my_file_splited[-1]


        if extension==my_file_splited[0]:
            extension="html"

        if extension!="html":
            extension = "html"
            new_file = "{}.{}".format(my_file_splited[0], extension)
            logger.debug("output file was '{}' it will be changed to '{}' ".format(my_file, new_file))

        new_file = "{}.{}".format(my_file_splited[0], extension)

        del path_list[-1]


        parent_directory_path = ""
        for part in path_list:
            parent_directory_path += part+"\\"


        if not os.path.isdir(parent_directory_path):
            raise AssertionError("Could not find this path '{}'".format(parent_directory_path))
        else:

            return parent_directory_path + new_file
