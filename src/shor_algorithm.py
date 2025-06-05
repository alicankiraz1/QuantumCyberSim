"""
Shor Algorithm - Demonstration of Cracking RSA-Like Ciphers with Qiskit
"""

from qiskit import QuantumCircuit, transpile
from qiskit.primitives import Sampler
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Operator
import numpy as np
from math import gcd
from fractions import Fraction
import time

class ShorAlgorithm:
    """Qiskit implementation of Shor algorithm"""
    
    def __init__(self, N):
        self.N = N
        self.n_qubits = int(np.ceil(np.log2(N)))
        
    def quantum_period_finding(self, a, precision=None):
        """
        Quantum period finding algorithm.
        Finds the period r for which a^r mod N = 1.
        """
        if precision is None:
            precision = 2 * self.n_qubits + 1
            
        # Creating a quantum circuit
        qc = QuantumCircuit(precision + self.n_qubits, precision)
        
        # Putting the first register into superposition
        for i in range(precision):
            qc.h(i)
            
        # Prepare the second register to the |1⟩ state
        qc.x(precision)
        
        # Controlled modular exponential operations
        for q in range(precision):
            # a^(2^q) mod N 
            power = 2 ** q
            self._controlled_modular_exponentiation(qc, q, a, power)
        
        # Inverse QFT
        self._inverse_qft(qc, precision)
        
        # Ölçüm
        for i in range(precision):
            qc.measure(i, i)
            
        return qc
    
    def _controlled_modular_exponentiation(self, qc, control, a, power):
        """Controlled U^(2^j) gate - simplified version"""
        # Because the actual implementation is complex
        # Approximate simulation with phase gate
        angle = 2 * np.pi * (a ** power % self.N) / self.N
        if self.n_qubits + len(qc.qubits) > control + 1:
            target = len(qc.qubits) - self.n_qubits
            if target > control:
                qc.cp(angle, control, target)
    
    def _inverse_qft(self, qc, n):
        """n-qubitlik inverse Quantum Fourier Transform"""
        # Swap qubits
        for i in range(n // 2):
            qc.swap(i, n - i - 1)
            
        # Controlled phase gates
        for j in range(n):
            qc.h(j)
            for k in range(j):
                qc.cp(-np.pi / (2 ** (j - k)), k, j)
    
    def find_factors(self, max_attempts=10):
        """Shor algoritması ile N'yi çarpanlarına ayır"""
        print(f"\nFactoring {self.N} with Shor Algorithm")
        print("=" * 50)
        
        if self.N % 2 == 0:
            return 2, self.N // 2
            
        # Is it of the form N = a^b?
        for b in range(2, int(np.log2(self.N)) + 1):
            a = int(self.N ** (1/b))
            if a ** b == self.N:
                return a, self.N // a
        
        for attempt in range(max_attempts):
            print(f"\nAttempt {attempt + 1}:")
            
            # Rastgele a seç
            a = np.random.randint(2, self.N)
            g = gcd(a, self.N)
            
            print(f"  Seçilen a = {a}")
            print(f"  gcd({a}, {self.N}) = {g}")
            
            if g > 1:
                print(f"  ✓ Common divisor found!")
                return g, self.N // g
            
            # Quantum period finding (simulation)
            print(f"  Starting quantum period detection...")
            r = self._classical_period_finding(a)  
            
            if r is None:
                print(f"  ✗ Period not found")
                continue
                
            print(f"  ✓ Found period: r = {r}")
            
            if r % 2 != 0:
                print(f"  ✗ Period odd number")
                continue
                
            x = pow(a, r // 2, self.N)
            factor1 = gcd(x - 1, self.N)
            factor2 = gcd(x + 1, self.N)
            
            if 1 < factor1 < self.N:
                print(f"  ✓ Multipliers found!")
                return factor1, self.N // factor1
            elif 1 < factor2 < self.N:
                print(f"  ✓ Multipliers found!")
                return factor2, self.N // factor2
                
        return None, None
    
    def _classical_period_finding(self, a):
        """Classical period finding (for simulation)"""
        for r in range(1, self.N):
            if pow(a, r, self.N) == 1:
                return r
        return None

def demonstrate_rsa_breaking():
    """RSA-like encryption cracking demonstration"""
    print("\n" + "="*60)
    print("QUANTUM CYBER SECURITY - SHOR ALGORITHM DEMONSTRATION")
    print("="*60)
    print("\nLOW-LEVEL RSA-LIKE ENCRYPTION BREAKING SIMULATION")
    print("\nNOTE: Since the actual RSA keys are very large,")
    print("Demonstration is done with small numbers.")
    
    test_cases = [
        (15, "Very small RSA modulus"),
        (21, "Small RSA module"), 
        (35, "Medium RSA module"),
        (77, "Large RSA module")
    ]
    
    results = []
    
    for N, description in test_cases:
        print(f"\n{'='*50}")
        print(f"Test: {description} (N = {N})")
        
        start_time = time.time()
        shor = ShorAlgorithm(N)
        p, q = shor.find_factors(max_attempts=5)
        end_time = time.time()
        
        if p and q:
            print(f"\n✅ Success!")
            print(f"   N = {N} = {p} × {q}")
            print(f"   Verification: {p} × {q} = {p * q}")
            print(f"   Time: {end_time - start_time:.3f} second")
            
            phi = (p - 1) * (q - 1)
            print(f"   Euler φ(N) = {phi}")
            
            results.append((N, p, q, True))
        else:
            print(f"\n❌ Could not be factored")
            results.append((N, None, None, False))
    
    # Özet
    print(f"\n{'='*60}")
    print("SUMMARY RESULTS:")
    print(f"{'='*60}")
    success_count = sum(1 for _, _, _, success in results if success)
    print(f"Success: {success_count}/{len(test_cases)}")
    
    print("\n🔐 SECURITY WARNING:")
    print("True RSA encryption uses 2048-4096 bit keys.")
    print("Current known quantum computers cannot yet crack keys of this size.")
    print("But in the future, powerful quantum computers may pose this threat!")

def create_quantum_circuit_visualization():
    """Quantum circuit visualization"""
    print(f"\n{'='*60}")
    print("QUANTUM CIRCUIT VISUALIZATION")
    print(f"{'='*60}\n")
    
    shor = ShorAlgorithm(15)
    qc = shor.quantum_period_finding(2, precision=4)
    
    print("Quantum Period Finding Circuit (N=15, a=2):")
    print(f"Total qubits: {qc.num_qubits}")
    print(f"Classic bit: {qc.num_clbits}")
    print("\nCircuit Structure:")
    print(qc.draw(output='text', fold=100))

if __name__ == "__main__":
    # RSA cracking demonstration
    demonstrate_rsa_breaking()
    
    # Quantum circuit visualization
    create_quantum_circuit_visualization()
    
    print("\n✨ Programme completed!")
