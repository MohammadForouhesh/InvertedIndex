import java

# Jython swings library
from java.awt import EventQueue
from javax.swing import JSeparator
from java.awt import BorderLayout
from java.awt import FlowLayout
from javax.swing import Box
from javax.swing import JPanel
from javax.swing import JTextArea
from javax.swing import JScrollPane
from javax.swing import JButton
from javax.swing import JFileChooser
from javax.swing import JCheckBox
from javax.swing import JFrame
from javax.swing import JLabel

# Inverted Index library
from TST import TST
from BST import BST
from TrieST import TrieST
from DynamicArray import DynamicArray
from LinkedList import LinkedList
from LinkedQueue import LinkedQueue
from LinkedStack import LinkedStack
from TreeBuilder import TreeBuilder
from CommandCompiler import CommandLineCompiler


class GUI(java.lang.Runnable):
    def __init__(self):
        self.resultText = str()
        self.cmd_compiler = None    # CommandLineCompiler()
        self.tree_builder = None    # TreeBuilder
        self.directory = None
        self.frame = None
        self.area = None
        self.label = None
        self.command_editor = None
        self.chooser = None
        self.check_box = None

    def projectile_pane(self, buffer_txt):
        i = 1
        for text in buffer_txt:
            if i == len(buffer_txt):
                self.area.append(text.element)
                continue
            string = " " + text.element
            if len(string) < 13:
                string += "\t"
            else:
                string += " "
            self.area.append("{}".format(string))
            i += 1
        self.area.append("\n")

    def builder(self, tree_name):
        self.tree_builder = TreeBuilder(tree_name, self.directory)
        # ------------------------------------- projectile -------------------------------------
        buffer_txt = LinkedQueue()
        for txt in self.tree_builder.words_tree.traverse():
            if buffer_txt is None:
                buffer_txt = LinkedQueue()
            buffer_txt.enqueue(txt)
            if len(buffer_txt) > 4:
                self.projectile_pane(buffer_txt)
                buffer_txt = None

        # ------------------------------------- projectile -------------------------------------


















    def run(self):
        self.frame = JFrame(
            'InvertedIndex',
            size=(500, 900),
            layout=FlowLayout(),
            defaultCloseOperation=JFrame.EXIT_ON_CLOSE
        )

        self.chooser = JButton(
                'Browse',
                font = ("Comic Sans MS", 30, 30),
                actionPerformed=self.showFC
        )

        self.area = JTextArea(
            font=("Comic Sans MS", 30, 30),
            editable=False,
            rows=20,
            columns=45
        )

        self.command_editor = JTextArea(
            font=("Comic Sans MS", 30, 30),
            rows=2,
            columns=45,
        )

        panel = [None]*7
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

    def update(self):
        pass

if __name__ in ['__main__', 'main']:
    EventQueue.invokeLater(GUI())
    if 'AdminConfig' in dir():
        raw_input('\nPress <Enter> to terminate the application:\n')