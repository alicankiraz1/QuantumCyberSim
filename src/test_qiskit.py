from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator # Qiskit 1.0 ve sonrasında AerSimulator bu şekilde import ediliyor
import numpy as np

# 2 kübitlik bir kuantum devresi oluştur
circuit = QuantumCircuit(2, 2)

# H kapısını ilk kübite uygula (süperpozisyon oluştur)
circuit.h(0)

# CNOT kapısını uygula (dolaşıklık oluştur)
# Kontrol kübiti 0, hedef kübit 1
circuit.cx(0, 1)

# Kübitleri klasik bitlere ölç
circuit.measure([0,1], [0,1])

# Aer simülatörünü kullan
simulator = AerSimulator()

# Devreyi simülatör için derle
compiled_circuit = transpile(circuit, simulator)

# Simülasyonu çalıştır
job = simulator.run(compiled_circuit, shots=1000)

# Sonuçları al
result = job.result()

# Sayımları (counts) yazdır
counts = result.get_counts(circuit)
print("\nTotal count for 00 and 11 are:",counts)

# Devreyi çiz (opsiyonel, terminalde metin tabanlı çizim)
print(circuit.draw(output='text'))

print("Qiskit kurulum testi başarılı!")
