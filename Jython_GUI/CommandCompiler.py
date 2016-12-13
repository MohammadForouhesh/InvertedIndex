import os
import re
from BST import BST
from LinkedList import LinkedList
from TST import TST
from TreeBuilder import TreeBuilder
from TrieST import TrieST


class CommandLineCompiler:

    def __init__(self, command, directory_field, tree_type):
        self.tree_type = tree_type
        self.files_list = []
        self.directory_text_field = directory_field
        self._sytax_of_command_line(command)

    def _sytax_of_command_line(self, command):
        command_words = command.split()
        current_state = 0
        max_non_error_state = 15
        i = 0
        while i < len(command_words) and current_state < max_non_error_state:
            if current_state == 0:
                if command_words[0].lower() == 'add':
                    current_state = 1
                elif command_words[0].lower() == 'del':
                    current_state = 2
                elif command_words[0].lower() == 'update':
                    current_state = 3
                elif command_words[0].lower() == 'list':
                    current_state = 4
                elif command_words[0].lower() == 'search':
                    current_state = 5
                else:
                    current_state = 14
            elif current_state == 1:
                first_quote = re.match(r'^"(.*)', command_words[1])
                second_quote = re.match(r'(.*)"$', command_words[-1])
                if first_quote and second_quote:
                    if command_words[1] == '\"':
                        del command_words[1]
                    else:
                        command_words[1] = command_words[1].replace('\"', '')
                    if command_words[-1] == '\"':
                        del command_words[-1]
                    else:
                        command_words[-1] = command_words[-1].replace('\"', '')
                    name_of_file = ''
                    for separate_word in command_words[1:]:
                        name_of_file += separate_word
                    file_exist = False
                    for subdir, dirs, files in os.walk(self.directory_text_field.toString()):
                        for file in files:
                            if name_of_file in file:
                                file_exist = True
                    if [name_of_file_added for name_of_file_added in self.files_list \
                        if name_of_file_added.documentName == len(name_of_file)] > 0:
######################################################################################################################
                        write_result('Error : Document already Exists!!!\n---------------\n')
######################################################################################################################
                    elif not file_exist:
######################################################################################################################
                        write_result('Error : Document not Found!!!\n---------------\n')
######################################################################################################################
                    else:

                        treeBuilder = TreeBuilder(self.tree_type, self.directory_text_field)
                        self.wordTree = treeBuilder.word_tree
                        self.files_list = treeBuilder.files_list
######################################################################################################################
                        write_result('File' + name_of_file + 'Added\n---------------\n')
######################################################################################################################
                else:
######################################################################################################################
                    write_result('Error Happend')
######################################################################################################################
                return True
            elif current_state == 2:
                first_quote = re.match(r'^"(.*)', command_words[1])
                second_quote = re.match(r'(.*)"$', command_words[-1])
                if first_quote and second_quote:
                    if command_words[1] == '\"':
                        del command_words[1]
                    else:
                        command_words[1] = command_words[1].replace('\"', '')
                    if command_words[-1] == '\"':
                        del command_words[-1]
                    else:
                        command_words[-1] = command_words[-1].replace('\"', '')
                    name_of_file = ''
                    for separate_word in command_words[1:]:
                        name_of_file += separate_word
                    file_name_found = False
                    files_to_delete = [name_of_file_added for name_of_file_added in self.files_list if
                                       name_of_file_added.documentName == name_of_file]
                    for file_going_to_delete in files_to_delete:
                        file_name_found = True
                        file_going_to_delete.removeAll()
                        self.files_list.remove(file_going_to_delete)
                        del file_going_to_delete
######################################################################################################################
                        write_result('File ' + name_of_file + ' Deleted\n---------------\n')
######################################################################################################################
                    if not file_name_found:
                        self.write_result(self.resultText.insert(tkinter.INSERT,
                                                            'Error : Document not Found!!!\n---------------\n'))
                else:
######################################################################################################################
                    write_result('Error Happend\n---------------\n')
######################################################################################################################

                return True
            elif current_state == 3:
                first_quote = re.match(r'^"(.*)', command_words[1])
                second_quote = re.match(r'(.*)"$', command_words[-1])
                if first_quote and second_quote:
                    if not first_quote.group(1) == '\"':
                        command_words[1] = command_words[1].replace('\"', '')
                    if not second_quote.group(1) == '\"':
                        command_words[-1] = command_words[-1].replace('\"', '')
                else:
######################################################################################################################
                    write_result('Error Happend\n---------------\n')
######################################################################################################################
                return True
            elif current_state == 4:
                if command_words[1] == '-w':
                    current_state = 9
                elif command_words[1] == '-l':
                    current_state = 10
                elif command_words[1] == '-f':
                    current_state = 11
            elif current_state == 5:
                if command_words[1] == '-s':
                    current_state = 12
                elif command_words[1] == '-w':
                    current_state = 13
            elif current_state == 6:
                return True
            elif current_state == 7:
                return True
            elif current_state == 8:
                return True
            elif current_state == 9:
                print(type(self.tree_type))
                if type(self.tree_type) == TST:
                    print("success")
                    self.wordTree.validation()
                    for i in self.wordTree.traverse():
                        self.write_result(i)
                elif type(self.tree_type) == TrieST:
                    self.wordTree.validation()
                    for i in self.wordTree.traverse():
                        self.write_result(i)

                elif type(self.tree_type) == BST:
                    self.wordTree.traverse()
                    for i in self.wordTree.content:
                        self.write_result(i.key)

                return True
            elif current_state == 10:
                for file in self.files_list:
                    self.write_result(file + ' ')
                    print("success")
                    self.write_result('\nNumber of listed Docs = ' + str(len(self.files_list)) + '\n---------------\n')
                return True
            elif current_state == 11:
                number_of_files = 0
                for subdir, dirs, files in os.walk(self.directory_text_field.get()):
                    for file in files:
                        if file.endswith('.txt'):
                            self.write_result(file[:-4] + ' ')
                            number_of_files += 1
                self.write_result('\nNumber of all Docs = ' + str(number_of_files) + '\n---------------\n')
                return True

            elif current_state == 12:
                first_quote = re.match(r'^"(.*)', command_words[2])
                print('1')
                second_quote = re.match(r'(.*)"$', command_words[-1])
                print('2')
                if first_quote and second_quote:
                    print('3')
                    if not first_quote.group(1) == '\"':
                        command_words[2] = command_words[2].replace('\"', '')
                    print('4')
                    if not second_quote.group(1) == '\"':
                        command_words[-1] = command_words[-1].replace('\"', '')
                    print('5')
                else:
######################################################################################################################
                    write_result('Error Happend\n---------------\n')
######################################################################################################################

                if command_words[-1] is command_words[2]:
                    if not self.wordTree[command_words[-1]]:
                        self.write_result('\nAny word found !!!\n---------------\n')
                    else:
                        self.write_result(self.wordTree[command_words[-1]].refrence.getAll())
                current_state = 20  # <-- This live has to change -->
                return True
            elif current_state == 13:
                first_quote = re.match(r'^"(.*)', command_words[2])
                second_quote = re.match(r'(.*)"$', command_words[-1])
                if first_quote and second_quote:
                    if not first_quote.group(1) == '\"':
                        command_words[2] = command_words[2].replace('\"', '')
                    if not second_quote.group(1) == '\"':
                        command_words[-1] = command_words[-1].replace('\"', '')
                else:
######################################################################################################################
                    write_result('Error Happend')
######################################################################################################################
                if command_words[-1] is command_words[2]:
                    if not self.wordTree[command_words[-1]]:
                        self.write_result('\nAny word found !!!\n')
                    else:
                        self.write_result(self.wordTree[command_words[-1]].refrence.getAll())
                current_state = 20  # <-- This live has to change -->
                return True
            else:
######################################################################################################################
                write_result('Error : Unkown Command\n')
######################################################################################################################
                return True
        return True
