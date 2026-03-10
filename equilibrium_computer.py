import numpy as np
import matplotlib.pyplot as plt
import pickle
from pycollisiondb.pycollisiondb import PyCollision
from pathlib import Path

plt.style.use('/home/matt/latex_and_matplotlib_styles/matplotlib_styles/physrev.mplstyle')  # Set full path to
# physrev.mplstyle if the file is not in the same in directory as the notebook
plt.rcParams['figure.dpi'] = "300"


class AtomicData:
    def __init__(self, gas_species="He"):
        """
        For now, we can restrict the query to a single species, singly ionized
        First we can check a standardized file name to see if we have already queried the data:

        """

        self.species = gas_species
        pass

    def _format_file_name(self):
        file_name = "atomic_data_" + self.species + ".p"


    def check_for_data(self):
