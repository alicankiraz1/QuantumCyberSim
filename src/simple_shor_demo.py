"""
Simple Shor Algorithm Demonstration
This script demonstrates the basic components of the Shor algorithm using Qiskit.
"""

from qiskit import QuantumCircuit, transpile
from qiskit.primitives import Sampler
from qiskit_aer import AerSimulator
import numpy as np
from math import gcd
from fractions import Fraction

def quantum_phase_estimation(a, N, precision=3):
    """
    Creates a simple circuit for Quantum Phase Estimation. 
    This is the core component of Shor's algorithm.
    """
    n_count = precision
    n_aux = int(np.ceil(np.log2(N)))
    
    qc = QuantumCircuit(n_count + n_aux, n_count)
    
    for i in range(n_count):
        qc.h(i)
    
    qc.x(n_count)
    
    for counting_qubit in range(n_count):
        angle = 2 * np.pi * (a ** (2 ** counting_qubit)) / N
        qc.cp(angle, counting_qubit, n_count)
    
    for i in range(n_count // 2):
        qc.swap(i, n_count - i - 1)
    
    for j in range(n_count):
        qc.h(j)
        for k in range(j):
            qc.cp(-np.pi / (2 ** (j - k)), k, j)
    
    for i in range(n_count):
        qc.measure(i, i)
    
    return qc

def find_period(a, N, shots=1024):
    """
    Find the period using classical simulation.
    In a real quantum computer this is done with QPE.
    """
    for r in range(1, N):
        if pow(a, r, N) == 1:
            return r
    return None

def shors_algorithm(N):
    """
    A simplified version of Shor's algorithm. 
    Factors the number N.
    """
    print(f"\n{'='*50}")
    print(f"Factoring {N} numbers using Shor's Algorithm")
    print(f"{'='*50}\n")
    
    if N % 2 == 0:
        return 2, N // 2
    
    for b in range(2, int(np.log2(N)) + 1):
        a = int(N ** (1 / b))
        if a ** b == N:
            return a, b
    
    for attempt in range(5):  
        a = np.random.randint(2, N)
        g = gcd(a, N)
        
        print(f"Attempt {attempt + 1}: a = {a}")
        print(f"gcd({a}, {N}) = {g}")
        
        if g > 1:
            print(f"We're in luck! A common divisor was found.")
            return g, N // g
        
        print(f"Searching for period a = {a}...")
        r = find_period(a, N)
        
        if r is None:
            print("No period found.")
            continue
            
        print(f"Periyot r = {r}")
        
        if r % 2 != 0:
            print("Period is odd, new a will be tried.")
            continue
        
        factor1 = gcd(a ** (r // 2) - 1, N)
        factor2 = gcd(a ** (r // 2) + 1, N)
        
        if factor1 > 1 and factor1 < N:
            print(f"\nMultipliers found!")
            return factor1, N // factor1
        elif factor2 > 1 and factor2 < N:
            print(f"\nMultipliers found!")
            return factor2, N // factor2
    
    print("No multiplier found.")
    return None, None

def demonstrate_quantum_circuit():
    """
    A simple quantum circuit demonstration
    """
    print("\nQuantum Circuit Demonstration")
    print("-" * 30)
    
    qc = quantum_phase_estimation(2, 15, precision=4)
    
    print("Quantum circuit created.")
    print(f"Total number of qubits: {qc.num_qubits}")
    print(f"Classical number of bits: {qc.num_clbits}")
    
    print("\nCircuit Structure:")
    print(qc.draw(output='text', fold=80))
    
    simulator = AerSimulator()
    transpiled = transpile(qc, simulator)
    sampler = Sampler()
    
    print("\nStarting simulation...")

def main():
    numbers_to_factor = [15, 21, 35]
    
    print("Quantum Cyber ​​Security - Shor Algorithm Demonstration")
    print("=" * 60)
    print("\nNOTE: This is a simplified version of Shor's algorithm.")
    print("Classical simulation is used instead of true quantum computation.\n")
    
    for N in numbers_to_factor:
        factor1, factor2 = shors_algorithm(N)
        
        if factor1 and factor2:
            print(f"\n✓ Success: {N} = {factor1} × {factor2}")
            print(f"Validation: {factor1} × {factor2} = {factor1 * factor2}")
        else:
            print(f"\n✗ FAILED: Could not factor {N}")
    
    print("\n" + "=" * 60)
    demonstrate_quantum_circuit()

if __name__ == "__main__":
    main()
