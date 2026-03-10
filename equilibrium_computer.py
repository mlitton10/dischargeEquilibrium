import numpy as np
import matplotlib.pyplot as plt
import pickle
from pycollisiondb.pycollisiondb import PyCollision
from pathlib import Path

plt.style.use('/home/matt/latex_and_matplotlib_styles/matplotlib_styles/physrev.mplstyle')  # Set full path to
# physrev.mplstyle if the file is not in the same in directory as the notebook
plt.rcParams['figure.dpi'] = "300"


class AtomicData:
    def __init__(self, data_dict, file_name):

        self.reaction = data_dict['reaction_name']
        self.y_data_info = data_dict['y_data_info']
        self.x_data_info = data_dict['x_data_info']

        self.y_data = data_dict['y_data']
        self.x_data = data_dict['x_data']

        self.file_name = file_name

        pass

    def save_data(self):
        with open('archived_atomic_data/' + self.file_name, 'wb') as f:
            # Load the data from the file into a Python object
            pickle.dump(self, f)

class AtomicDataHandler:
    def __init__(self, gas_species="He"):
        """
        For now, we can restrict the query to a single species, singly ionized
        First we can check a standardized file name to see if we have already queried the data:

        """

        self.species = gas_species
        self.dataset = self.query_manager()

        pass

    def _format_file_name(self):
        file_name = "atomic_data_" + self.species + ".p"
        return file_name

    def check_for_data(self):
        path = 'archived_atomic_data/' + self._format_file_name()
        if Path(path).is_file():  # check if the file exists in the data archive
            archived_bool = True
        else:
            archived_bool = False

        return archived_bool

    def query_manager(self):
        archived_bool = self.check_for_data()
        if archived_bool:  # if archived data exists, pull it
            file_path = 'archived_atomic_data/' + self._format_file_name()

            # Open the file in read binary mode ('rb')
            with open(file_path, 'rb') as f:
                # Load the data from the file into a Python object
                loaded_object = pickle.load(f)

            return loaded_object

        else:
            query_dict = {'reactants': ['e-', self.species],  # search for reactions involving electrons, Hydrogen atom
                          'data_type': 'rate coefficient',  # return a rate coefficient (averaged over what?)
                          'process_types': ['EIN']}  # Look for electron ionization cross sections

            pycoll_data = PyCollision.get_datasets(query=query_dict)
            minimum_rate_key = self.find_minimum_rate(pycoll_data.datasets)
            formatted_data = self.format_dataset(pycoll_data, minimum_rate_key)

            atomic_data_instance = AtomicData(formatted_data, self._format_file_name())



    def find_minimum_rate(self, data):
        """
        For now, we can take a zeroth order approach to this calculation and find the minimum, presumably limiting
        ionization rate and use that as the starting point for our calculation

        :param data:
        :return:
        """
        average_data_dict = {key: np.mean(value.y) for key, value in
                             data.items()}  # find the average rates for each process/study

        idx = np.argmin(list(average_data_dict.values()))  # index of minimum value
        min_key = list(data.keys())[idx]  # pycoll key for minimum rate
        return min_key

    def format_dataset(self, data, key):

        metadata = data.datasets[key].metadata
        reaction_name = metadata['reaction']
        y_data_type = metadata['columns'][0]
        x_data_type = metadata['columns'][1]

        x_data = data.datasets[key].x
        y_data = data.datasets[key].x

        data_dict = {'reaction': reaction_name,
                     'y_data_info': y_data_type,
                     'x_data_info': x_data_type,
                     'x_data': x_data,
                     'y_data': y_data}

        return data_dict

