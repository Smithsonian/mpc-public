
# Import the MPCORB class from mpc_orb ...
from mpc_orb import MPCORB

# Import the list of JSONs that are expected to pass ...
from mpc_orb.filepaths import test_pass_mpcorb

# Define a filepath to an example json file provided in the package
filepath = test_pass_mpcorb[0]
print(f'filepath=\n {filepath} \n')





# Instantiate an MPCORB object & use it to parse the above json file
# -------------------------------------------------------------------
M = MPCORB(filepath)

# Demonstrate the available variables
print('\n MPCORB instance variables ... ')
for attribute in vars(M):
    print(f'\t{attribute:>20} : {type(M.__dict__[attribute])}')
 # -------------------------------------------------------------------




# There are COM & CAR objects contained within the MPCORB Object
# -------------------------------------------------------------------
# Demonstrate the attributes available in the "COM" coord-object contained
print('\n CAR instance variables ... ')
for attribute in vars(M.CAR):
    print(f'\t{attribute:>20} : {type(M.CAR.__dict__[attribute])}')
# -------------------------------------------------------------------



# Access the orbit elements from the MPCORB object in different ways
# -------------------------------------------------------------------
# Demonstrate access to Cartesian elements
print('\nformat = CAR = Cartesian ... ')
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


# Demonstrate access to Cartesian elements
print('-'*33)
print('\nformat = COM = Cometary ... ')
print('\n\t coefficient names ... ')
print('\t',M.COM.coefficient_names )

print('\n\t coefficient values ... ')
print('\t',M.COM.coefficient_values )

print('\n\t coefficient uncertainties ... ')
print('\t',M.COM.coefficient_uncertainties )

print('\n\t element dictionary with combined values & uncertainties ... ')
print('\t',M.COM.element_dict )

print('\n\t individual element access (e)... ')
print('\t',M.COM.e )

print('\n\t covariance array ... ')
print('\t',M.COM.covariance_array )


# Demonstrate that access to individual elements (Cartesian & Cometary) is also possible from the MPCORB object
print('-'*33)
print('\nMPCORB also has individual-element attributes ... ')

print('\n\t individual element access (x)... ')
print('\t',M.x )

print('\n\t individual element access (e)... ')
print('\t',M.e )
# -------------------------------------------------------------------





# Use the describe function to access information / definitions for each attribute
# -------------------------------------------------------------------
# Demonstrate the available variables
print('\n MPCORB description ... ')
for attribute in vars(M):
    print(f'\n{M.describe(attribute)}')
# -------------------------------------------------------------------
