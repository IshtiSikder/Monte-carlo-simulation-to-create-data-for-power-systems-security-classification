# Monte-carlo-simulation-to-create-data-for-power-systems-security-classification

1. Solves AC power flow (ACPF) for a 9 bus system with a renewable energy (wind) generator and N-1 contingency for given number of iterations. The 9 bus system data has been loaded using the PYPOWER model for python.
2. The chosen number of iterations is 5000.  
3. Python's multiprocessing module has been used to parallely process 1000 iterations at a time on 5 CPU cores simultaneously.
4. The cloud computing resources provided to UNC Charlotte students has been utilized for the parallel processing. 
5. The total computing time is approximately 3 minutes
6. Out of the 5000 iterations, the ACPF model resolved 3091 times
7. Solved data is downsized into 3x9 matrices and labelled (secure,alarm,not secure) using the formula for composite security index
8. Output is saved as .txt file




