"""
mpc_orb/demo.py
 - Code to provide a quick demo (post-install) of how to use the MPCORB
   class
   
Author(s)
MJP
"""


# local imports
# -----------------------
from mpc_orb.parse import MPCORB, COORD

def tprint(lft,rght,width=20):
    print(f'\t{lft:<{width}}:\t{rght}')

def demo():
    """
    Demonstration function to
    (a) read in a sample mpc_orb.json file, and
    (b) illustrate the available attributes of an MPCORB object
    
    inputs:
    -------
    None
    
    returns:
    --------
    ???
    
    """
    # Define a filepath to an example json file provided in the package
    demo_filepath = 'demo_json/2012HN13_mpcorb_yarkovski.json'
    print(f'\nAccessing a sample json file:\n\t{demo_filepath}')

    # Instantiate an MPCORB object & use it to parse the above json file
    # & Demonstrate the available variables
    M = MPCORB(demo_filepath)
    print(f'\nWe instantiated an MPCORB object using the sample json')
    tprint('code','MPCORB(demo_filepath)')
    tprint('type(M)','type(M)')

    print('An MPCORB object has variables ... ')
    for attribute in vars(M):
        tprint(attribute,type(M.__dict__[attribute]))

    # There are COM & CAR objects contained within the MPCORB Object
    # Demonstrate the attributes available in the "COM" coord-object contained
    print('\nWe now examine the CAR object within the MPCORB object ... ')
    print('A CAR instance has variables ... ')
    for attribute in vars(M.CAR):
        tprint(attribute,type(M.CAR.__dict__[attribute]))

    # Demonstrate access to Cartesian elements
    print('\nWe now examine a selection of the variables within the CAR object ... ')
    print('\n\t coefficient names ... ')
    print('\t',M.CAR.coefficient_names )

    print('\n\t coefficient values ... ')
    print('\t',M.CAR.coefficient_values )

    print('\n\t coefficient uncertainties ... ')
    print('\t',M.CAR.coefficient_uncertainties )

    print('\n\t element dictionary with combined values & uncertainties ... ')
    print('\t',M.CAR.element_dict )

    print('\n\t individual element access (x)... ')
    print('\t',M.CAR.x )

    print('\n\t covariance array ... ')
    print('\t',M.CAR.covariance_array )

if __name__ == '__main__':
    demo()
