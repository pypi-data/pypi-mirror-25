import sys
if __name__ == '__main__':
    sys.path.append('../')

from PyQt5.QtCore import Qt, QThread, QObject, pyqtSignal,QFileInfo
from PyQt5.QtWidgets import (QWidget, QApplication, QVBoxLayout, QTreeWidget,
                             QTreeWidgetItem, QTextEdit, QLineEdit, QPushButton,
                             QLabel, QHBoxLayout, QFileDialog,QTabWidget,
                             QFormLayout,QGridLayout,QListWidget,QSizePolicy,
                             QComboBox)
from PyQt5.QtGui import QFontMetrics,QFont

# Queue module version name changed between Python 2 & 3, so this allows
# for both
if sys.version[0] == '2':
    from Queue import Queue
else:
    from queue import Queue

import os,traceback,sys

import re

from cued_datalogger.api.channel import ChannelSet


class AddonManager(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.addon_functions = {}

        self.addon_local_vars = {}
        self.addon_global_vars = {}

        self.addon_writer = None
        self.init_ui()

        # # Addon Execution Initialisation
        # When the addon is run, stdout must be redirected
        # Create a buffer for redirecting stdout
        self.stdout_buffer = Queue()
        # Create a writestream - this is a wrapper for the buffer, that behaves
        # like stdout (ie it has a write function)
        self.writestream = WriteStream(self.stdout_buffer)
        # Create the object that writes to the textedit
        self.text_receiver = TextReceiver(self.stdout_buffer)
        self.text_receiver.sig_text_received.connect(self.output.append)

        ### Should just create a Thread once???
        # Create a thread for the receiver
        self.receiver_thread = QThread()
        # Run the receiver
        self.receiver_thread.started.connect(self.text_receiver.run)
        # Move the receiver to the thread
        self.text_receiver.moveToThread(self.receiver_thread)


    def init_ui(self):
        '''
        Initialise the UI components
        '''
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        writer_btn = QPushButton("Open Addon Writer")
        writer_btn.clicked.connect(self.open_writer)
        self.layout.addWidget(writer_btn)

        search_hbox = QHBoxLayout()
        search_label = QLabel("Search:")
        search_hbox.addWidget(search_label)
        self.search = QLineEdit(self)
        search_hbox.addWidget(self.search)
        self.layout.addLayout(search_hbox)

        self.tree = QTreeWidget(self)
        self.tree.setHeaderLabels(["Name", "Author", "Description"])
        self.import_export = QTreeWidgetItem(self.tree)
        self.import_export.setText(0, "Import/Export")
        self.analysis = QTreeWidgetItem(self.tree)
        self.analysis.setText(0, "Analysis")
        self.plotting = QTreeWidgetItem(self.tree)
        self.plotting.setText(0, "Plotting")
        self.tree.itemDoubleClicked.connect(self.run_selected)
        self.layout.addWidget(self.tree)

        self.load_btn = QPushButton(self)
        self.load_btn.setText("Load Addon")
        self.load_btn.clicked.connect(self.load_new)
        self.layout.addWidget(self.load_btn)

        self.run_btn = QPushButton(self)
        self.run_btn.setText("Run selected")
        self.run_btn.clicked.connect(self.run_selected)
        self.layout.addWidget(self.run_btn)

        output_label = QLabel("Output:")
        self.layout.addWidget(output_label)
        self.output = QTextEdit(self)
        self.output.setReadOnly(True)
        self.layout.addWidget(self.output)


    def discover_addons(self, path):
        """Find any addons contained in path and load them"""
        print("Discovering addons...")
        if os.path.exists(path):
            path_to_search = path
        elif os.path.exists('./addons/'):
            print("Path does not exist. Searching ./addons instead.")
            path_to_search = './addons/'
        else:
            print("Path does not exist. Searching current directory instead.")
            path_to_search = './'

        addon_list = []

        for file in os.listdir(path_to_search):
            if file.endswith(".py"):
                with open(path_to_search + file, 'r') as f:
                    line1 = f.readline()
                if line1 == "#cued_datalogger_addon\n":
                    addon_list.append(path_to_search+file)

        if addon_list:
            print("\t Found:")
            for addon in addon_list:
                print("\t\t " + addon)
                self.add_addon(addon)
        else:
            print("None found.")

    def load_new(self):
        # Get a list of URLs from a QFileDialog
        url_list = QFileDialog.getOpenFileNames(self, "Load new addon", "addons",
                                               "CUED DataLogger Addons (*.py)")[0]

        # For each url, add it to the tree
        for url in url_list:
            self.add_addon(url)

    def add_addon(self, addon_url):
        # Read the file
        try:
            with open(addon_url) as a:
                # Execute the file
                # WARNING: THIS IS RATHER DANGEROUS - there could be anything
                # in there!
                exec(a.read(), self.addon_local_vars, self.addon_global_vars)
        except:
            print('Error detected in code!')
            t,v,tb = sys.exc_info()
            print(t)
            print(v)
            print(traceback.format_tb(tb))
            return

        # Extract the metadata
        metadata = self.addon_global_vars["addon_metadata"]

        # Add the addon to the tree
        if metadata["category"] == "Import/Export":
            parent = self.import_export
        elif metadata["category"] == "Analysis":
            parent = self.analysis
        elif metadata["category"] == "Plotting":
            parent = self.plotting
        else:
            parent = self.tree

        addon_item = QTreeWidgetItem(parent, [metadata["name"],
                                              metadata["author"],
                                              metadata["description"]])

        # Save the addon function
        self.addon_functions[metadata["name"]] = self.addon_global_vars["run"]

    def run_selected(self):
        # Get the addon metadata from the tree
        name = self.tree.currentItem().data(0, Qt.DisplayRole)
        author = self.tree.currentItem().data(1, Qt.DisplayRole)
        description = self.tree.currentItem().data(2, Qt.DisplayRole)
        # # Run the addon function, but redirect the stdout
        # Redirect stdout to the writestream
        stdout_old = sys.stdout
        sys.stdout = self.writestream

        # Start the receiver
        self.start_receiver_thread()

        # Print some info about the addon
        print("###\n {} by {}\n {}\n###".format(name, author, description))
        # Execute the addon
        try:
            self.addon_functions[name](self.parent)
        except:
            t,v,tb = sys.exc_info()
            print(t)
            print(v)
            print(traceback.format_tb(tb))
            print('Error in Code!')
        # Tidy up
        # TODO maybe need to have a more robust way of ensuring that everything
        # closes properly eg. if application quits before these lines reached
        self.receiver_thread.quit()
        sys.stdout = stdout_old

    def start_receiver_thread(self):
        self.receiver_thread.start()

    def open_writer(self):
        if not self.addon_writer:
            self.addon_writer = AddonWriter()
            self.addon_writer.done.connect(self.done_writer)
        else:
            self.addon_writer.show()

    def done_writer(self):
        self.addon_writer.done.disconnect()
        self.addon_writer = None

class WriteStream(object):
    """A simple object that writes to a queue - replace stdout with this"""
    def __init__(self, queue):
        self.queue = queue

    def write(self, text):
        self.queue.put(text)


class TextReceiver(QObject):
    """Sits blocking until data is written to stdout_buffer, which it then
    emits as a signal. To be run in a QThread."""
    sig_text_received = pyqtSignal(str)

    def __init__(self, stdout_buffer):
        super().__init__()
        self.stdout_buffer = stdout_buffer

    def run(self):
        while True:
            # Get text from stdout (block until there's something to get)
            # If we got something, send the text received signal
            # Blocking actually crashes the program :(
            stdout_text = self.stdout_buffer.get(block = False)
            self.sig_text_received.emit(stdout_text)

                #break

class AddonWriter(QWidget):
    '''
    Opens a window to write an addon, following the template. Still in alpha stage.
    The window is also able to load an addon for editting.

    Attributes
    ----------
    done: pyqtsignal
        Emits when the window is closed
    '''
    done = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setGeometry(500,300,600,500)
        self.setWindowTitle('AddonWriter')
        self.init_UI()
        self.show()

    def init_UI(self):
        '''
        Construct the window
        '''
        main_layout = QVBoxLayout(self)

        btn_layout = QHBoxLayout()
        save_btn = QPushButton('Save',self)
        save_btn.clicked.connect(self.create_addon)
        btn_layout.addWidget(save_btn)
        load_btn = QPushButton('Load',self)
        load_btn.clicked.connect(self.read_addon)
        btn_layout.addWidget(load_btn)
        run_btn = QPushButton('Run',self)
        run_btn.setDisabled(True)
        btn_layout.addWidget(run_btn)
        clear_btn = QPushButton('Clear',self)
        clear_btn.setDisabled(True)
        btn_layout.addWidget(clear_btn)

        main_layout.addLayout(btn_layout)

        self.tabs = QTabWidget(self)
        main_layout.addWidget(self.tabs)

        metadata_widget = QWidget(self)
        m_widget_layout = QVBoxLayout(metadata_widget)
        title_label = QLabel('Code Metadata')
        m_widget_layout.addWidget(title_label)
        metadata_layout = QFormLayout()

        self.meta_configs = []
        for mdata in ("File Name","Name","Author","Category"):
            if mdata == "Category":
                cbox = QComboBox(metadata_widget)
                cbox.addItems(["Import/Export","Analysis","Plotting"])
            else:
                cbox = QLineEdit(metadata_widget)
            metadata_layout.addRow(QLabel(mdata,metadata_widget),cbox)
            self.meta_configs.append(cbox)
        m_widget_layout.addLayout(metadata_layout)

        desc_label = QLabel('Description')
        m_widget_layout.addWidget(desc_label)

        desc_box = QTextEdit(metadata_widget)
        m_widget_layout.addWidget(desc_box)
        self.meta_configs.append(desc_box)

        code_widget = QWidget(self)
        c_widget_layout = QVBoxLayout(code_widget)

        font_metrics = QFontMetrics(QFont())
        w = font_metrics.width(' ')

        main_code_label = QLabel('Run Code',code_widget)
        self.main_code_text = QTextEdit(code_widget)
        self.main_code_text.setTabStopWidth(w*4)

        c_widget_layout.addWidget(main_code_label)
        c_widget_layout.addWidget(self.main_code_text)

        self.tabs.addTab(metadata_widget,'Metadata')
        self.tabs.addTab(code_widget,'Code')

    def closeEvent(self,event):
        '''
        Reimplemented from QWidget to emit the done signal
        '''
        self.done.emit()
        event.accept()
        self.deleteLater()

    def create_addon(self):
        '''
        Create the addon in the given template
        '''
        file_name = self.meta_configs[0].text().replace(' ','')
        if not file_name:
            print('Please give a file name')
            return
        metadata = [self.meta_configs[1].text(),
                    self.meta_configs[2].text(),
                    self.meta_configs[3].currentText(),
                    self.meta_configs[4].toPlainText()]
        metadata[3] = metadata[3].replace("\n"," ")
        metadata = ["\"" + md + "\""  for md in metadata]

        with open("./addons/%s.py" % file_name,'w',encoding='ASCII') as file:
            file.write('#cued_datalogger_addon\n')
            file.write("""addon_metadata = {"name": %s,\n"author": %s,\n"category": %s,\n"description": %s}\n\n""" %
                       tuple(metadata))
            main_code = self.main_code_text.toPlainText()
            if not main_code:
                main_code = 'pass'
            full_code = "def run(parent_window):\n" + main_code
            full_code = full_code.replace('\n','\n\t')
            file.write(full_code)

    def read_addon(self):
        '''
        Read the addon
        '''
        url_list = QFileDialog.getOpenFileNames(self, "Load addon", "addons",
                                               "DataLogger Addons (*.py)")[0][0]
        
        if url_list:
            f = QFileInfo(url_list)
            self.meta_configs[0].setText(f.fileName().strip('.py'))
            with open(url_list) as file:
                data = file.readlines()
            func_re = re.compile(r'def run(\S*):')
            func_search = [True if func_re.search(s) else False for s in data ].index(True)
            self.main_code_text.clear()
            indentRE = re.compile(r'(\s){4}|\t')
            for line in data[func_search+1:]:
                self.main_code_text.append(indentRE.sub('',line.strip('\n'),1))

            try:
                addon_local_vars = {}
                addon_global_vars = {}
                with open(url_list) as file:
                    exec(file.read(), addon_local_vars, addon_global_vars)
            except:
                print('Error detected in code!')
                t,v,tb = sys.exc_info()
                print(t)
                print(v)
                print(traceback.format_tb(tb))
                return
            
            metadata = addon_global_vars["addon_metadata"]
            # Extract the metadata
            self.meta_configs[1].setText(metadata["name"])
            self.meta_configs[2].setText(metadata["author"])
            self.meta_configs[3].setCurrentText(metadata["category"])
            self.meta_configs[4].setText(metadata["description"])

        else:
            print('No data')

'''
if __name__ == '__main__':
    app = 0
    app = QApplication(sys.argv)

    w = AnalysisWindow()
    w.addon_widget.discover_addons("../addons/")

    w.show()

    sys.exit(app.exec_())
'''