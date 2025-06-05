# Quantum Cybersecurity Simulation Tool 🔐⚛️

A Python-based quantum simulation tool focused on cybersecurity applications, specifically implementing Shor's algorithm for integer factorization using Qiskit.

## 🎯 Project Overview

This project demonstrates how quantum computing poses a threat to current cryptographic systems, particularly RSA encryption, by implementing Shor's algorithm - a quantum algorithm that can efficiently factorize large integers.

### Key Features

- ✅ Custom implementation of Shor's algorithm
- ✅ Quantum Phase Estimation (QPE) circuit generation
- ✅ RSA-like modulus factorization demonstration
- ✅ Visual quantum circuit representation
- ✅ Classical simulation for educational purposes

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ (tested on Python 3.13)
- macOS, Linux, or Windows
- Basic understanding of quantum computing concepts

### Installation

1. Clone the repository:
```bash
git clone https://github.com/[your-username]/QuantumCyberSim.git
cd QuantumCyberSim
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## 📁 Project Structure

```
QuantumCyberSim/
├── src/
│   ├── shor_algorithm.py      # Main Shor algorithm implementation
│   ├── simple_shor_demo.py    # Basic demonstration script
│   └── test_qiskit.py         # Qiskit installation test
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── .gitignore                # Git ignore rules
```

## 🔧 Usage

### Running the Shor Algorithm

```bash
python src/shor_algorithm.py
```

This will:
- Factorize test numbers (15, 21, 35, 77)
- Display the quantum circuit structure
- Show RSA security implications

### Running the Simple Demo

```bash
python src/simple_shor_demo.py
```

This provides a simplified demonstration of the algorithm's core concepts.

## 📊 Example Output

```
============================================================
QUANTUM CYBERSECURITY - SHOR ALGORITHM DEMONSTRATION
============================================================

Test: Small RSA module (N = 21)

✅ SUCCESS!
   N = 21 = 3 × 7
   Verification: 3 × 7 = 21
   Time: 0.001 seconds
   Euler φ(N) = 12
```

## 🛡️ Security Implications

This project demonstrates why quantum computing poses a significant threat to current cryptographic systems:

- **Current RSA**: Uses 2048-4096 bit keys
- **Classical computers**: Would take billions of years to break
- **Quantum computers**: Could break them in hours/days (once powerful enough)
- **Post-quantum cryptography**: New algorithms needed for quantum-resistant security

## ⚠️ Limitations

- Current implementation uses classical simulation (not actual quantum hardware)
- Limited to small numbers due to computational constraints
- Educational purposes only - not for production use

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with [Qiskit](https://qiskit.org/) - IBM's open-source quantum computing framework
- Inspired by Peter Shor's groundbreaking algorithm (1994)

## 📚 References

- [Shor's Algorithm - Qiskit Textbook](https://qiskit.org/textbook/ch-algorithms/shor.html)
- [Post-Quantum Cryptography - NIST](https://csrc.nist.gov/projects/post-quantum-cryptography)
- [Original Paper - Polynomial-Time Algorithms for Prime Factorization](https://arxiv.org/abs/quant-ph/9508027)

---
⭐ If you find this project helpful, please consider giving it a star on GitHub!
