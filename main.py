from qrisp_optimization import QAOA, Bruteforce
from qrisp_optimization.problems import QUBO_Problem
import numpy as np

def main():
    problem = QUBO_Problem(
        Q = np.array([  
            [ 1. , -3. , -2. ,  2. ,  1.5,  0. ,  0. ],
            [ 0. ,  2.5, -2. ,  0. , -1.5,  0.5,  0. ],
            [ 0. ,  0. ,  3. , -2.5, -4. ,  1. ,  0. ],
            [ 0. ,  0. ,  0. ,  1. ,  0. ,  0. ,  2. ],
            [ 0. ,  0. ,  0. ,  0. ,  2. ,  0. ,  0. ],
            [ 0. ,  0. ,  0. ,  0. ,  0. ,  1.5,  0. ],
            [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  1. ]    
        ])
    )
    algorithm = Bruteforce(problem=problem)
    print(algorithm.solve())


if __name__ == "__main__":
    main()
