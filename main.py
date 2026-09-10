import numpy as np
from qrisp import QuantumArray

from qrisp_optimization import (
    Bruteforce, 
    Bruteforce_Requirements, 
    QAOA, 
    QAOA_Requirements
)

from qrisp_optimization.problems import QUBO_Problem
from qrisp_optimization.utils import QuantumBinary

"""
This file is intended to be an example and is intentionally more detailed as it would be needed 
"""


def main():
    """
        Entrypoint for this script,
        1. Instantiate a Problem (in this case QUBO from a given matrix)
        2. Solve the problem with both Bruteforce and QAOA (this works since problem implements both requirements)
        3. print the solutions
    """
    Q = np.array([  
        [ 1. , -3. , -2. ,  2. ,  1.5,  0. ,  0. ],
        [ 0. ,  2.5, -2. ,  0. , -1.5,  0.5,  0. ],
        [ 0. ,  0. ,  3. , -2.5, -4. ,  1. ,  0. ],
        [ 0. ,  0. ,  0. ,  1. ,  0. ,  0. ,  2. ],
        [ 0. ,  0. ,  0. ,  0. ,  2. ,  0. ,  0. ],
        [ 0. ,  0. ,  0. ,  0. ,  0. ,  1.5,  0. ],
        [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  1. ]    
    ])
    problem = QUBO_Problem(Q=Q)                 # At this point problem does not know which algorithm will be used,
                                                # it only knows that it satisfies the requirements for QAOA and Bruteforce

    algorithm_bf = Bruteforce(
        problem=problem                         # using polymorphism: here the problem is a bruteforce-able problem
    )
    optimal = algorithm_bf.solve()              # keep this for printing the results in a nice way


    algorithm = QAOA(                           
        problem=problem,                        # using polymorphism: here the same problem is a qaoa-able problem
        qarg=QuantumArray(
            qtype=QuantumBinary(),
            shape=len(Q)   
        )
    )
    theta = np.array([0.5]*6)                   # This could be a warm start or just random parameter initialization
    #theta = algorithm.optimize(theta)          # This is not implemented in the current stage, but it would be the way to do it later
    qarg = algorithm.ansatz(theta)              # This gives access to the qarg after the qaoa algorithm is applied
    meas = qarg.get_measurement()

    # this has nothing to do with the solving, 
    # just print the results in a nicer way
    for bitstring, prob in meas.items():        
        is_optimal = bitstring in optimal       # check if a given bitstring is in the classicaly obtained optimal solutions list
        print(f""" \
            {bitstring} with cost = {problem.cl_cost_function(bitstring)} \
            \t{prob = :.4f}\
            {"  <" + "-"*20 + " optimal solution" if is_optimal else ""} \
        """)


if __name__ == "__main__":
    main()
