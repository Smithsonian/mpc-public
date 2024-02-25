# tests 

Directory to store various tests of the python code in */mpc-public/mpc_orb/mpc_orb/*


## Test Execution 
To execute the tests, run 
> cd tests

> pytest -v


## Expected Test Results 
As of April 2023, the expected results of running the above test are ...

collected 14 items                                                                                                                                                   

 - test_filepaths.py::test_filepaths_A PASSED                                                                                                                     [  7%]
 - test_interpret.py::test_interpret_A PASSED                                                                                                                     [ 14%]
 - test_interpret.py::test_interpret_B XFAIL                                                                                                                      [ 21%]
 - test_interpret.py::test_interpret_C XFAIL                                                                                                                      [ 28%]
 - test_interpret.py::test_interpret_D PASSED                                                                                                                     [ 35%]
 - test_parse.py::test_MPCORB_A PASSED                                                                                                                            [ 42%]
 - test_parse.py::test_MPCORB_B PASSED                                                                                                                            [ 50%]
 - test_parse.py::test_parse_C PASSED                                                                                                                             [ 57%]
 - test_parse.py::test_parse_D PASSED                                                                                                                             [ 64%]
 - test_parse.py::test_describe_A PASSED                                                                                                                          [ 71%]
 - test_validation.py::test_schema PASSED                                                                                                                         [ 78%]
 - test_validation.py::test_validation_A PASSED                                                                                                                   [ 85%]
 - test_validation.py::test_validation_B PASSED                                                                                                                   [ 92%]
 - test_validation.py::test_validation_C XFAIL                                                                                                                    [100%]

=== 11 passed, 3 xfailed in 0.20s ===

