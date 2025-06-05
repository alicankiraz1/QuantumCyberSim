from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator 
import numpy as np

circuit = QuantumCircuit(2, 2)

circuit.h(0)

circuit.cx(0, 1)

circuit.measure([0,1], [0,1])

simulator = AerSimulator()

compiled_circuit = transpile(circuit, simulator)

job = simulator.run(compiled_circuit, shots=1000)

result = job.result()

counts = result.get_counts(circuit)
print("\nTotal count for 00 and 11 are:",counts)

print(circuit.draw(output='text'))

print("Qiskit installation test successful!")
