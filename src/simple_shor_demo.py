"""
Basit Shor Algoritması Demonstrasyonu
Bu betik, Qiskit kullanarak Shor algoritmasının temel bileşenlerini gösterir.
"""

from qiskit import QuantumCircuit, transpile
from qiskit.primitives import Sampler
from qiskit_aer import AerSimulator
import numpy as np
from math import gcd
from fractions import Fraction

def quantum_phase_estimation(a, N, precision=3):
    """
    Kuantum Faz Kestirimi için basit bir devre oluşturur.
    Bu, Shor algoritmasının çekirdek bileşenidir.
    """
    # Kontrol qubit sayısı (precision)
    n_count = precision
    # N'yi temsil etmek için gereken qubit sayısı
    n_aux = int(np.ceil(np.log2(N)))
    
    # Kuantum devresi oluştur
    qc = QuantumCircuit(n_count + n_aux, n_count)
    
    # Kontrol qubitlerini süperpozisyona sok (Hadamard)
    for i in range(n_count):
        qc.h(i)
    
    # Auxiliary registeri |1⟩ durumuna hazırla
    qc.x(n_count)
    
    # Kontrollü U^(2^j) kapıları uygula
    for counting_qubit in range(n_count):
        # U^(2^j) = a^(2^j) mod N işlemini simüle et
        # Bu basitleştirilmiş bir versiyondur
        angle = 2 * np.pi * (a ** (2 ** counting_qubit)) / N
        qc.cp(angle, counting_qubit, n_count)
    
    # Inverse QFT uygula
    for i in range(n_count // 2):
        qc.swap(i, n_count - i - 1)
    
    for j in range(n_count):
        qc.h(j)
        for k in range(j):
            qc.cp(-np.pi / (2 ** (j - k)), k, j)
    
    # Ölçüm
    for i in range(n_count):
        qc.measure(i, i)
    
    return qc

def find_period(a, N, shots=1024):
    """
    Klasik simülasyon kullanarak periyodu bul.
    Gerçek kuantum bilgisayarda bu QPE ile yapılır.
    """
    # Basit klasik periyot bulma
    for r in range(1, N):
        if pow(a, r, N) == 1:
            return r
    return None

def shors_algorithm(N):
    """
    Shor algoritmasının basitleştirilmiş versiyonu.
    N sayısını çarpanlarına ayırır.
    """
    print(f"\n{'='*50}")
    print(f"Shor Algoritması ile {N} sayısını çarpanlarına ayırma")
    print(f"{'='*50}\n")
    
    # Adım 1: N'nin asal sayı veya çift sayı kontrolü
    if N % 2 == 0:
        return 2, N // 2
    
    # Adım 2: N = a^b formunda mı kontrol et
    for b in range(2, int(np.log2(N)) + 1):
        a = int(N ** (1 / b))
        if a ** b == N:
            return a, b
    
    # Adım 3: Rastgele bir a seç (1 < a < N ve gcd(a, N) = 1)
    for attempt in range(5):  # 5 deneme yap
        a = np.random.randint(2, N)
        g = gcd(a, N)
        
        print(f"Deneme {attempt + 1}: a = {a}")
        print(f"gcd({a}, {N}) = {g}")
        
        if g > 1:
            print(f"Şanslıyız! Ortak bölen bulundu.")
            return g, N // g
        
        # Adım 4: Periyodu bul (klasik simülasyon)
        print(f"a = {a} için periyot aranıyor...")
        r = find_period(a, N)
        
        if r is None:
            print("Periyot bulunamadı.")
            continue
            
        print(f"Periyot r = {r}")
        
        # Adım 5: r çift mi kontrol et
        if r % 2 != 0:
            print("Periyot tek sayı, yeni a denenecek.")
            continue
        
        # Adım 6: Çarpanları hesapla
        factor1 = gcd(a ** (r // 2) - 1, N)
        factor2 = gcd(a ** (r // 2) + 1, N)
        
        if factor1 > 1 and factor1 < N:
            print(f"\nÇarpanlar bulundu!")
            return factor1, N // factor1
        elif factor2 > 1 and factor2 < N:
            print(f"\nÇarpanlar bulundu!")
            return factor2, N // factor2
    
    print("Çarpan bulunamadı.")
    return None, None

def demonstrate_quantum_circuit():
    """
    Basit bir kuantum devresi demonstrasyonu
    """
    print("\nKuantum Devresi Demonstrasyonu")
    print("-" * 30)
    
    # Basit QPE benzeri devre oluştur
    qc = quantum_phase_estimation(2, 15, precision=4)
    
    print("Kuantum devresi oluşturuldu.")
    print(f"Toplam qubit sayısı: {qc.num_qubits}")
    print(f"Klasik bit sayısı: {qc.num_clbits}")
    
    # Devre görselleştirmesi (text formatında)
    print("\nDevre Yapısı:")
    print(qc.draw(output='text', fold=80))
    
    # Simülasyon
    simulator = AerSimulator()
    transpiled = transpile(qc, simulator)
    sampler = Sampler()
    
    print("\nSimülasyon başlatılıyor...")
    # Not: Gerçek QPE sonuçları karmaşık olabilir, bu basit bir demo

def main():
    # Test edilecek sayılar
    numbers_to_factor = [15, 21, 35]
    
    print("Kuantum Siber Güvenlik - Shor Algoritması Demonstrasyonu")
    print("=" * 60)
    print("\nNOT: Bu, Shor algoritmasının basitleştirilmiş bir versiyonudur.")
    print("Gerçek kuantum hesaplama yerine klasik simülasyon kullanılmaktadır.\n")
    
    # Her sayı için Shor algoritmasını çalıştır
    for N in numbers_to_factor:
        factor1, factor2 = shors_algorithm(N)
        
        if factor1 and factor2:
            print(f"\n✓ BAŞARILI: {N} = {factor1} × {factor2}")
            print(f"Doğrulama: {factor1} × {factor2} = {factor1 * factor2}")
        else:
            print(f"\n✗ BAŞARISIZ: {N} çarpanlarına ayrılamadı")
    
    # Kuantum devresi demonstrasyonu
    print("\n" + "=" * 60)
    demonstrate_quantum_circuit()

if __name__ == "__main__":
    main()
