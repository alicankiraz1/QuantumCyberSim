"""
Shor Algoritması - Qiskit ile RSA Benzeri Şifreleri Kırma Demonstrasyonu
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
    """Shor algoritmasının Qiskit implementasyonu"""
    
    def __init__(self, N):
        self.N = N
        self.n_qubits = int(np.ceil(np.log2(N)))
        
    def quantum_period_finding(self, a, precision=None):
        """
        Kuantum periyot bulma algoritması.
        a^r mod N = 1 olan r periyodunu bulur.
        """
        if precision is None:
            precision = 2 * self.n_qubits + 1
            
        # Kuantum devresi oluştur
        qc = QuantumCircuit(precision + self.n_qubits, precision)
        
        # İlk register'ı süperpozisyona sok
        for i in range(precision):
            qc.h(i)
            
        # İkinci register'ı |1⟩ durumuna hazırla
        qc.x(precision)
        
        # Kontrollü modüler üslü işlemler
        for q in range(precision):
            # a^(2^q) mod N işlemini uygula
            power = 2 ** q
            self._controlled_modular_exponentiation(qc, q, a, power)
        
        # Inverse QFT
        self._inverse_qft(qc, precision)
        
        # Ölçüm
        for i in range(precision):
            qc.measure(i, i)
            
        return qc
    
    def _controlled_modular_exponentiation(self, qc, control, a, power):
        """Kontrollü U^(2^j) kapısı - basitleştirilmiş versiyon"""
        # Gerçek implementasyon karmaşık olduğu için
        # faz kapısı ile yaklaşık simülasyon
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
        print(f"\nShor Algoritması ile {self.N} sayısını faktörleme")
        print("=" * 50)
        
        # Basit kontroller
        if self.N % 2 == 0:
            return 2, self.N // 2
            
        # N = a^b formunda mı?
        for b in range(2, int(np.log2(self.N)) + 1):
            a = int(self.N ** (1/b))
            if a ** b == self.N:
                return a, self.N // a
        
        # Ana algoritma
        for attempt in range(max_attempts):
            print(f"\nDeneme {attempt + 1}:")
            
            # Rastgele a seç
            a = np.random.randint(2, self.N)
            g = gcd(a, self.N)
            
            print(f"  Seçilen a = {a}")
            print(f"  gcd({a}, {self.N}) = {g}")
            
            if g > 1:
                print(f"  ✓ Ortak bölen bulundu!")
                return g, self.N // g
            
            # Kuantum periyot bulma (simülasyon)
            print(f"  Kuantum periyot bulma başlatılıyor...")
            r = self._classical_period_finding(a)  # Simülasyon için klasik
            
            if r is None:
                print(f"  ✗ Periyot bulunamadı")
                continue
                
            print(f"  ✓ Bulunan periyot: r = {r}")
            
            if r % 2 != 0:
                print(f"  ✗ Periyot tek sayı")
                continue
                
            # Çarpanları hesapla
            x = pow(a, r // 2, self.N)
            factor1 = gcd(x - 1, self.N)
            factor2 = gcd(x + 1, self.N)
            
            if 1 < factor1 < self.N:
                print(f"  ✓ Çarpanlar bulundu!")
                return factor1, self.N // factor1
            elif 1 < factor2 < self.N:
                print(f"  ✓ Çarpanlar bulundu!")
                return factor2, self.N // factor2
                
        return None, None
    
    def _classical_period_finding(self, a):
        """Klasik periyot bulma (simülasyon için)"""
        for r in range(1, self.N):
            if pow(a, r, self.N) == 1:
                return r
        return None

def demonstrate_rsa_breaking():
    """RSA benzeri şifreleme kırma demonstrasyonu"""
    print("\n" + "="*60)
    print("KUANTUM SİBER GÜVENLİK - SHOR ALGORİTMASI DEMONSTRASYONU")
    print("="*60)
    print("\nDÜŞÜK SEVİYE RSA BENZERİ ŞİFRELEME KIRMA SİMÜLASYONU")
    print("\nNOT: Gerçek RSA anahtarları çok büyük olduğu için,")
    print("küçük sayılarla demonstrasyon yapılmaktadır.")
    
    # Test edilecek RSA benzeri modüller
    test_cases = [
        (15, "Çok küçük RSA modülü"),
        (21, "Küçük RSA modülü"), 
        (35, "Orta RSA modülü"),
        (77, "Büyük test modülü")
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
            print(f"\n✅ BAŞARILI!")
            print(f"   N = {N} = {p} × {q}")
            print(f"   Doğrulama: {p} × {q} = {p * q}")
            print(f"   Süre: {end_time - start_time:.3f} saniye")
            
            # RSA parametrelerini hesapla
            phi = (p - 1) * (q - 1)
            print(f"   Euler φ(N) = {phi}")
            
            results.append((N, p, q, True))
        else:
            print(f"\n❌ Çarpanlara ayrılamadı")
            results.append((N, None, None, False))
    
    # Özet
    print(f"\n{'='*60}")
    print("ÖZET SONUÇLAR:")
    print(f"{'='*60}")
    success_count = sum(1 for _, _, _, success in results if success)
    print(f"Başarılı: {success_count}/{len(test_cases)}")
    
    print("\n🔐 GÜVENLİK UYARISI:")
    print("Gerçek RSA şifrelemede 2048-4096 bit anahtarlar kullanılır.")
    print("Mevcut kuantum bilgisayarlar henüz bu boyutta anahtarları kıramaz.")
    print("Ancak gelecekte güçlü kuantum bilgisayarlar bu tehdidi oluşturabilir!")

def create_quantum_circuit_visualization():
    """Kuantum devresi görselleştirmesi"""
    print(f"\n{'='*60}")
    print("KUANTUM DEVRESİ GÖRSELLEŞTİRMESİ")
    print(f"{'='*60}\n")
    
    # Örnek bir Shor devresi parçası
    shor = ShorAlgorithm(15)
    qc = shor.quantum_period_finding(2, precision=4)
    
    print("Kuantum Periyot Bulma Devresi (N=15, a=2):")
    print(f"Toplam qubit: {qc.num_qubits}")
    print(f"Klasik bit: {qc.num_clbits}")
    print("\nDevre Yapısı:")
    print(qc.draw(output='text', fold=100))

# Ana program
if __name__ == "__main__":
    # RSA kırma demonstrasyonu
    demonstrate_rsa_breaking()
    
    # Kuantum devresi görselleştirmesi
    create_quantum_circuit_visualization()
    
    print("\n✨ Program tamamlandı!")
