import sys,traceback
import scipy.io as sio
from cued_datalogger.api.channel import Channel, DataSet, ChannelSet
import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout,QPushButton,QLabel,QTreeWidget,
                             QTreeWidgetItem,QHBoxLayout,QFileDialog)
from PyQt5.QtCore import  Qt
import pickle

def import_from_mat(file, channel_set=None):
    """
    A function for importing data and metadata to a ChannelSet from an 
    old-style DataLogger ``.mat`` file.
    
    Parameters
    ----------
    file : path_to_file
        The path to the ``.mat`` file to import data from.
    channel_set : ChannelSet
        The ChannelSet to save the imported data and metadata to. If ``None``, 
        a new ChannelSet is created and returned.
    """
    if channel_set is None:
        new_channel_set = True
        channel_set = ChannelSet()
    else:
        new_channel_set = False
    
    # Load the matlab file as a dict
    file = sio.loadmat(file)

    # Work out how many channels to create
    num_time_series_datasets = file["dt2"][0][0]
    num_spectrum_datasets = file["dt2"][0][1]
    num_sonogram_datasets = file["dt2"][0][2]

    num_channels = np.amax(np.asarray([num_time_series_datasets,
                                       num_spectrum_datasets,
                                       num_sonogram_datasets]))

    # # Extract metadata
    sample_rate = file["freq"][0][0]

    if "tsmax" in file.keys():
        time_series_scale_factor = file["tsmax"][0][0]
    else:
        time_series_scale_factor = 1

    if "npts" in file.keys():
        fft_num_samples = file["npts"]
    else:
        fft_num_samples = None

    if "tfun" in file.keys():
        is_transfer_function = bool(file["tfun"])
    else:
        is_transfer_function = False

    if "step" in file.keys():
        sonogram_fft_step = file["step"]
    else:
        sonogram_fft_step = None

    # # Extract data
    # Transpose the data so it's easier to work with:
    # In the matlab file it is in the form
    # (num_samples_per_channel, num_channels) - each channel is a column
    # Numpy works more easily if it is in the form
    # (num_channels, num_samples_per_channel) - each channel is a row
    if "indata" in file.keys():
        time_series = file["indata"].transpose()
    if "yspec" in file.keys():
        spectrum = file["yspec"].transpose()
    if "yson" in file.keys():
        sonogram_amplitude = file["yson"].transpose()
    if "yphase" in file.keys():
        sonogram_phase = file["yphase"].transpose()

    # # Save everything
    for i in np.arange(num_channels,dtype = np.int):
        # Create a new channel
        channel_set.add_channels()

        # Set channel metadata
        channel_set.set_channel_metadata(i, {"name": "Imported {}".format(i),
                                             "sample_rate": sample_rate,
                                             "calibration_factor":
                                                 time_series_scale_factor})

        # Set channel data
        if i < num_time_series_datasets:
            channel_set.add_channel_dataset(i,
                                            "time_series",
                                            time_series[i])

        # Differentiate between TF and FFT
        if i < num_spectrum_datasets:
            if is_transfer_function:
                channel_set.add_channel_dataset(i,
                                                "TF",
                                                 spectrum[i],
                                                 ' ')
            else:
                channel_set.add_channel_dataset(i,
                                                "spectrum",
                                                 spectrum[i],
                                                 'Hz')
            print(channel_set.channels[i].data("frequency"))
            
        if i < num_sonogram_datasets:
            channel_set.add_channel_dataset(i,
                                            "sonogram",
                                            sonogram_amplitude[i])
            channel_set.add_channel_dataset(i,
                                            "sonogram_phase",
                                            sonogram_phase[i],
                                            'rad')
    if new_channel_set:
        return channel_set
            
class DataImportWidget(QWidget):
    def __init__(self,parent):
        super().__init__(parent)
        self.new_cs = ChannelSet()
        self.init_UI()
        
    def init_UI(self):
        layout = QVBoxLayout(self)
        
        self.import_btn = QPushButton('Import Mat Files',self)
        self.import_btn.clicked.connect(self.import_files)
        self.pickle_btn = QPushButton('Import Pickle Files',self)
        self.pickle_btn.clicked.connect(self.load_pickle)
        layout.addWidget(self.import_btn)
        layout.addWidget(self.pickle_btn)
        layout.addWidget(QLabel('New ChannelSet Preview',self))
        
        self.tree = QTreeWidget(self)
        self.tree.setHeaderLabels(["Channel Number", "Name", "Units",
                                   "Comments", "Tags", "Sample rate",
                                   "Calibration factor",
                                   "Transfer function type"])
    
        layout.addWidget(self.tree)
        
        self.add_data_btn = QPushButton('Add ChannelSet to existing ChannelSet',self)
        self.rep_data_btn = QPushButton('Replace existing ChannelSet',self)
        layout.addWidget(self.add_data_btn)
        layout.addWidget(self.rep_data_btn)
        
    def set_channel_set(self, channel_set):
        print("Setting channel set...")
        self.tree.clear()

        #self.cs = channel_set

        self.channel_items = []

        for channel_number, channel in enumerate(channel_set.channels):
            # Create a tree widget item for this channel
            channel_item = QTreeWidgetItem(self.tree)
            #channel_item.setFlags(channel_item.flags() | Qt.ItemIsEditable)
            channel_item.setData(0, Qt.DisplayRole, channel_number)
            channel_item.setData(1, Qt.DisplayRole, channel.name)
            channel_item.setData(3, Qt.DisplayRole, channel.comments)
            channel_item.setData(4, Qt.DisplayRole, channel.tags)
            channel_item.setData(5, Qt.DisplayRole, '%.2f' % channel.sample_rate )
            channel_item.setData(6, Qt.DisplayRole, '%.2f' % channel.calibration_factor)
            channel_item.setData(7, Qt.DisplayRole, channel.transfer_function_type)
            # Add it to the list
            self.channel_items.append(channel_item)

            # Create a child tree widget item for each of the channel's datasets
            for dataset in channel.datasets:
                dataset_item = QTreeWidgetItem(channel_item)
                #dataset_item.setFlags(dataset_item.flags() | Qt.ItemIsEditable)
                dataset_item.setData(1, Qt.DisplayRole, dataset.id_)
                dataset_item.setData(2, Qt.DisplayRole, dataset.units)
        print("Done.")
        
    def import_files(self):
        # Get a list of URLs from a QFileDialog
        url = QFileDialog.getOpenFileNames(self, "Load transfer function", "addons",
                                               "MAT Files (*.mat)")[0]        
        try:
            import_from_mat(url[0], self.new_cs)
        except:
            t,v,tb = sys.exc_info()
            print(t)
            print(v)
            print(traceback.format_tb(tb))
            print('Load failed.')
            return
    
        self.set_channel_set(self.new_cs)
    
    def load_pickle(self):
        '''
        This is probably a temporary solution to loading data.
        Probably have to write a better way of storing data.
        PLEASE DO NOT OPEN ANY UNTRUSTED PICKLE FILES.
        UNPICKLING A FILE CAN EXECUTE ARBITRARY CODE, WHICH IS DANGEROUS TO YOUR COMPUTER.
        
        '''
        url = QFileDialog.getOpenFileName(self, "Load Channel Set", "addons",
                                               "Pickle Files (*.pickle)")[0]
        with open(url,'rb') as f:
            self.new_cs = pickle.load(f)
        self.set_channel_set(self.new_cs)
    
    def clear(self):
        self.new_cs = ChannelSet()
        self.set_channel_set(self.new_cs)
        
if __name__ == '__main__':
    cs = ChannelSet()
    import_from_mat("//cued-fs/users/general/tab53/ts-home/Documents/owncloud/Documents/urop/labs/4c6/transfer_function_clean.mat",
                    cs)
        
    print(cs.channel_ids(0))

