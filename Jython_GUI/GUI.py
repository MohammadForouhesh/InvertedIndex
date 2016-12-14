import os
import java

# Jython swings library
import re
from java.awt import EventQueue
from javax.swing import JSeparator
from java.awt import BorderLayout
from java.awt import FlowLayout
from javax.swing import Box
from javax.swing import JPanel
from javax.swing import JTextArea
from javax.swing import JTextField
from javax.swing import JScrollPane
from javax.swing import JButton
from javax.swing import JFileChooser
from javax.swing import JCheckBox
from javax.swing import JFrame
from javax.swing import JLabel

# Inverted Index library
from LinkedQueue import LinkedQueue
from TreeBuilder import TreeBuilder


class GUI(java.lang.Runnable):
    def __init__(self):
        self.resultText = str()
        self.cmd_compiler = None  # CommandLineCompiler()
        self.tree_builder = None  # TreeBuilder
        self.files_list = list()
        self.directory = None
        self.frame = None
        self.area = None
        self.label = None
        self.command_editor = None
        self.chooser = None
        self.check_box = None

    def project_warning(self, txt):
        self.area.append(txt + "\n")

    def projectile_pane(self, buffer_txt):
        i = 1
        for text in buffer_txt:
            if i == len(buffer_txt):
                self.area.append(text.element)
                continue
            string = " " + text.element
            if len(string) < 13:
                string += ", "
            else:
                string += " "
            self.area.append("{}".format(string))
            i += 1
        self.area.append("\n")

    def bufferizer(self, iterable):
        buffer_txt = None
        for txt in iterable:
            if buffer_txt is None:
                buffer_txt = LinkedQueue()
        # ------------------------------------- projectile -------------------------------------
            buffer_txt.enqueue(txt)
            if len(buffer_txt) > 10:
                self.projectile_pane(buffer_txt)
                buffer_txt = None

        if buffer_txt is not None:
            self.projectile_pane(buffer_txt)

        self.area.append("--------------------------------------------------------------------------\n")
        # ------------------------------------- projectile -------------------------------------

    def builder(self, tree_name):
        self.files_list = None
        self.tree_builder = TreeBuilder(tree_name, self.directory)
        self.files_list = self.tree_builder.files_list
        # ------------------------------------- projectile -------------------------------------
        number = 1
        for word in self.tree_builder.words_tree.traverse():
            temp_list = list()
            temp_list.append("[*{}*] ".format(number) + str(word) + " *--->  ")
            for doc in self.tree_builder.words_tree.__getitem__(word, trav=True).doc_list:
                if doc[:-4] not in temp_list:
                    print(doc)
                    temp_list.append(doc[:-4])
            self.bufferizer(temp_list)
            number += 1

        self.project_warning("number of words in {} : {}\n".format(self.directory.toString(), number))

        # ------------------------------------- projectile -------------------------------------

    def compiler(self, command, tree_type):
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

                    for separate_word in command_words[1:]:
                        for filename in os.listdir(self.directory.toString()):
                            if filename.endswith('.xtx'):
                                if filename[:-4] == separate_word[:-4]:
                                    infilename = os.path.join(self.directory.toString(), filename)
                                    if not os.path.isfile(infilename):
                                        continue
                                    oldbase = os.path.splitext(filename)
                                    newname = infilename.replace('.xtx', '.txt')
                                    os.rename(infilename, newname)
                                    self.files_list.append(separate_word)
                            else:
                                if filename == separate_word:
                                    self.files_list.append(separate_word)

                    self.tree_builder = TreeBuilder(tree_type, self.directory)
                    self.files_list = self.tree_builder.files_list

                else:
                    self.project_warning('Error Happend')
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

                    for separate_word in command_words[1:]:
                        if self.files_list.__contains__(separate_word):

                            for filename in os.listdir(self.directory.toString()):
                                if filename == separate_word:
                                    infilename = os.path.join(self.directory.toString(), filename)
                                    if not os.path.isfile(infilename):
                                        continue
                                    oldbase = os.path.splitext(filename)
                                    newname = infilename.replace('.txt', '.xtx')
                                    os.rename(infilename, newname)
                                    self.project_warning('File ' + filename + ' Deleted---------------\n')

                            else:
                                self.project_warning("directory is empty ------------------\n")

                            self.files_list.remove(separate_word)
                        else:
                            self.project_warning("no such a file ---------------\n")
                            self.project_warning("or are no file there to delete ------------------\n")

                    self.tree_builder = TreeBuilder(tree_type, self.directory)
                    self.files_list = self.tree_builder.files_list

                else:
                    self.project_warning('Error Happend---------------\n')

                return True

            elif current_state == 3:
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

                    self.tree_builder = TreeBuilder(tree_type, self.directory)
                    self.files_list = self.tree_builder.files_list
                    self.project_warning('File ' + command_words[-1] + ' Updated---------------\n')
                else:
                    self.project_warning('Error Happend---------------\n')

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
                print(type(tree_type))
                if unicode(tree_type) == unicode('TST'):
                    print("success")
                    self.tree_builder.words_tree.validation()
                    self.bufferizer(self.tree_builder.words_tree.traverse())

                elif unicode(tree_type) == unicode('TrieST'):
                    self.tree_builder.words_tree.validation()
                    self.bufferizer(self.tree_builder.words_tree.traverse())

                elif unicode(tree_type) == unicode('BST'):
                    self.tree_builder.words_tree.traverse()
                    self.bufferizer(self.tree_builder.words_tree.content)

                return True
            elif current_state == 10:
                self.bufferizer(self.files_list)
                print("success")
                self.project_warning('\nNumber of listed Docs = ' + str(len(self.files_list)) + '---------------\n')
                return True
            elif current_state == 11:
                queue = []
                for subdir, dirs, files in os.walk(self.directory.toString()):
                    for file in files:
                        if file.endswith('.txt'):
                            queue.append(file[:-4] + ' ')
                self.bufferizer(queue)
                self.project_warning('\nNumber of all Docs = ' + str(len(queue)) + '---------------\n')
                return True

            elif current_state == 12:
                first_quote = re.match(r'^"(.*)', command_words[2])
                second_quote = re.match(r'(.*)"$', command_words[-1])
                if first_quote and second_quote:
                    if not first_quote.group(1) == '\"':
                        command_words[2] = command_words[2].replace('\"', '')
                    if not second_quote.group(1) == '\"':
                        command_words[-1] = command_words[-1].replace('\"', '')
                else:
                    self.project_warning('Error Happend---------------\n')

                if command_words[-1] is command_words[2]:
                    if not self.tree_builder.words_tree[command_words[-1]]:
                        self.project_warning("\nThere is no such phrase !!!\n")
                    else:
                        self.bufferizer(self.tree_builder.words_tree.__getitem__(command_words[-1], get_doc=True))
                for word in command_words[2:]:
                    if self.tree_builder.stopwordsTrie[word] is None and self.tree_builder.words_tree[word] is not None:
                        self.bufferizer(self.tree_builder.words_tree.__getitem__(word, get_doc=True))
                self.project_warning('---------------\n')
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
                    self.project_warning('Error Happend')
                if command_words[-1] is command_words[2]:
                    if not self.tree_builder.words_tree[command_words[-1]]:
                        self.project_warning("\nThere is no such word !!!\n")
                    else:
                        print(self.tree_builder.words_tree.__getitem__(command_words[-1], get_doc=True))
                        self.bufferizer(self.tree_builder.words_tree.__getitem__(command_words[-1], get_doc=True))
                return True
            else:
                self.project_warning('Error : Unkown Command\n')
                return True
        return True

    def run(self):
        self.frame = JFrame(
            'InvertedIndex',
            size=(500, 900),
            layout=FlowLayout(),
            defaultCloseOperation=JFrame.EXIT_ON_CLOSE
        )

        self.chooser = JButton(
            'Browse',
            font=("Comic Sans MS", 30, 30),
            actionPerformed=self.showFC
        )

        self.area = JTextArea(
            font=("Comic Sans MS", 30, 30),
            editable=False,
            rows=20,
            columns=45
        )

        self.command_editor = JTextField(
            font=("Comic Sans MS", 30, 30),
            actionPerformed=self.update
        )

        panel = [None] * 7
        panel[0] = JPanel()
        panel[0].setLayout(BorderLayout())
        panel[0].add(self.chooser)
        panel[1] = JPanel()
        panel[1].setLayout(BorderLayout())
        panel[1].add(JScrollPane(self.area))
        panel[2] = JPanel()
        panel[2].setLayout(BorderLayout())
        panel[2].add(JScrollPane(self.command_editor))
        panel[3] = JPanel()
        panel[3].setLayout(FlowLayout())
        self.label = panel[3].add(JLabel('Nothing selected', font=("Comic Sans MS", 30, 30)))
        panel[4] = JPanel()
        panel[4].setLayout(FlowLayout())
        cp = panel[4]
        self.addCB(cp, 'TST')
        self.addCB(cp, 'BST')
        self.addCB(cp, 'TrieST')
        panel[5] = JPanel()
        panel[5].setLayout(FlowLayout())
        panel[5].add(JLabel(text="powered by", font=("Comic Sans MS", 20, 20)))
        panel[6] = JPanel()
        panel[6].setLayout(FlowLayout())
        panel[6].add(JLabel(text="Mohammad Hossein Forouhesh Tehrani", font=("Comic Sans MS", 30, 30)))

        box = Box.createVerticalBox()
        for pan in panel:
            box.add(Box.createGlue())
            box.add(pan)
            box.add(Box.createVerticalStrut(5))
            box.add(JSeparator())

        box.add(Box.createGlue())

        self.frame.add(box)
        self.frame.pack()
        self.frame.pack()
        self.frame.setVisible(1)

    def addCB(self, pane, text):
        pane.add(
            JCheckBox(
                text,
                font=("Comic Sans MS", 30, 30),
                itemStateChanged=self.toggle  # even handler
            )
        )

    def toggle(self, event):
        cb = event.getItem()
        text = cb.getText()
        state = ['No', 'Yes'][cb.isSelected()]
        self.label.setText('%s selected? %s' % (text, state))
        if state == 'Yes':
            self.builder(text)
            print(text)

    def showFC(self, event):
        Type = 'Open,Save,Custom'.split(',')
        Answer = 'Error,Approve,Cancel'.split(',')
        fc = JFileChooser()
        fc.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY)
        result = fc.showOpenDialog(None)
        if result == JFileChooser.APPROVE_OPTION:
            message = 'result = "%s"' % fc.getSelectedFile()
            self.directory = fc.getSelectedFile()
            print(self.directory)
            print(type(self.directory))
        else:
            message = 'Request canceled by user'
        self.label.setText(message)

    def update(self, event):
        value = event.getActionCommand()
        try:
            val = str(value)
            print(val)
            self.compiler(val, self.tree_builder.tree_type)

        except Exception as err:
            print("khar")
            print(err)


if __name__ in ['__main__', 'main']:
    EventQueue.invokeLater(GUI())
    if 'AdminConfig' in dir():
        raw_input('\nPress <Enter> to terminate the application:\n')
