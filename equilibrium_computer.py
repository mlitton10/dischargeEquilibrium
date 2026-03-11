import numpy as np
import matplotlib.pyplot as plt
from atomic_collisional import AtomicDataHandler

plt.style.use('/home/matt/latex_and_matplotlib_styles/matplotlib_styles/physrev.mplstyle')  # Set full path to
# physrev.mplstyle if the file is not in the same in directory as the notebook
plt.rcParams['figure.dpi'] = "300"


class Equilibrium:
    def __init__(self, gas_species, gas_pressure_torr, length, radius):
        self.species = gas_species
        self.pressure = gas_pressure_torr
        self.length = length
        self.radius = radius
        AtomicDataHandler(gas_species=test_species)
        atomic_data = atomic_query.query_manager()

        self.ion_mean_free_path = self.lambda_mean_free_path(self.pressure)


    def lambda_mean_free_path(self, p):
        """
        Ion mean free path (heuristic)
        :param p: neutral gas pressure, Torr
        :return: mean free path, cm
        """
        return 1 / (330 * p)

    def h_l(self, mfp, l):
        """
        Axial shape parameter, low pressure discharge < 100 mTorr; No field
        :param mfp: mean free path, ion
        :param l: length
        :return: spaped axial length
        """
        return 0.86 / np.sqrt(3 + l / (2 * mfp))

    def h_R(self, mfp, R):
        """
        radial shape parameter, low pressure discharge < 100 mTorr; No field
        :param mfp: mean free path, ion
        :param R: Radius
        :return: shaped radius
        """
        return 0.8 / np.sqrt(4 + R / mfp)

    def n_g(self, p):
        """
        heuristic for neutral density

        :param p: neutral pressure in torr
        :return: neutral density, cm^-3
        """
        return 330 * p / 1e-14

    def compute_temperature(self):
         C = self.atomic_data




if __name__ == "__main__":
    test_species = "He"
    atomic_query = AtomicDataHandler(gas_species=test_species)
    atomic_data = atomic_query.query_manager()


    f,a = plt.subplots(1,1)

    a.plot(atomic_data.x_data_interpolated, atomic_data.y_data_interpolated, label=atomic_data.reaction)

    a.set_yscale('log')
    a.set_xscale('log')

    a.set_title("Reaction Rates for " + atomic_data.reaction)

    a.set_xlabel('$T_e$ '+ atomic_data.x_data_info['units'])
    a.set_xlabel('$R_{iz}$ ' + atomic_data.y_data_info['units'])

    plt.show()



