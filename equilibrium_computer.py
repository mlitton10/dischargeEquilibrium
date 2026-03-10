import numpy as np
import matplotlib.pyplot as plt
from atomic_collisional import AtomicDataHandler

plt.style.use('/home/matt/latex_and_matplotlib_styles/matplotlib_styles/physrev.mplstyle')  # Set full path to
# physrev.mplstyle if the file is not in the same in directory as the notebook
plt.rcParams['figure.dpi'] = "300"




if __name__ == "__main__":
    test_species = "He"
    atomic_query = AtomicDataHandler(gas_species=test_species)
    atomic_data = atomic_query.query_manager()


    f,a = plt.subplots(1,1)

    a.plot(atomic_data.x_data, atomic_data.y_data, label=atomic_data.reaction)

    a.set_yscale('log')
    a.set_xscale('log')

    a.set_title("Reaction Rates for " + atomic_data.reaction)

    a.set_xlabel('$T_e$ '+ atomic_data.x_data_info['units'])
    a.set_xlabel('$R_{iz}$ ' + atomic_data.y_data_info['units'])

    plt.show()



