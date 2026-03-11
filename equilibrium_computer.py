import numpy as np
import matplotlib.pyplot as plt
from atomic_collisional import AtomicDataHandler

plt.style.use('/home/matt/latex_and_matplotlib_styles/matplotlib_styles/physrev.mplstyle')  # Set full path to
# physrev.mplstyle if the file is not in the same in directory as the notebook
plt.rcParams['figure.dpi'] = "300"

m_e = 0.511e6 # ev/c^2
M_p = 938e6 # ev/c^2

atomic_mass_dict = {'H': 1,
                    'D': 2,
                    'T': 3,
                    'He': 4,
                    'C': 12,
                    'Ne': 20.18,
                    'Ar': 39.95}


def find_roots(x, y):
    # Detect sign changes: True where the sign of y[i] and y[i+1] are different
    signs = np.sign(y)
    sign_changes = np.abs(np.diff(signs)).astype(bool)

    # Get the x and y values around the sign change
    x1 = x[:-1][sign_changes]
    x2 = x[1:][sign_changes]
    y1 = y[:-1][sign_changes]
    y2 = y[1:][sign_changes]

    # Linear interpolation to find the exact x-value where y=0
    # Formula derived from similar triangles: root = x1 + (x2 - x1) * |y1| / (|y1| + |y2|)
    roots_x = x1 + (x2 - x1) * np.abs(y1) / (np.abs(y1) + np.abs(y2))
    return roots_x

class Equilibrium:
    def __init__(self, gas_species='He', gas_pressure_torr=1e-4, length=100, radius=40):
        self.species = gas_species
        self.pressure = gas_pressure_torr
        self.length = length
        self.radius = radius
        self.neutral_density = self.n_g(self.pressure)
        atomic_query = AtomicDataHandler(gas_species=test_species)
        self.atomic_data = atomic_query.query_manager()

        self.ion_mean_free_path = self.lambda_mean_free_path(self.pressure)
        self.M = atomic_mass_dict[self.species] * M_p
        self.Te = self.compute_temperature()


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
        C = self.atomic_data.y_data_interpolated / np.sqrt(self.atomic_data.x_data_interpolated)
        rhs = np.sqrt(self.M) * 2 * (self.h_l(self.ion_mean_free_path, self.length) / self.length + self.h_R(self.ion_mean_free_path, self.radius) / self.radius) * (1 / self.n_g(self.pressure))
        roots = find_roots(self.atomic_data.x_data_interpolated, C - rhs)

        return np.min(roots)




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

    CTI_Test_bed_parameters = {'gas_species': 'He',
                               'gas_pressure_torr': 1e-4,
                               'length': 100,
                               'radius': 40
    }

    CTI_test_bed = Equilibrium(**CTI_Test_bed_parameters)

    print(CTI_test_bed.Te)



