import numpy as np
from qutip import *
import random

class ValenceSurfaceCodeDemo:
    def __init__(self, distance=3):
        self.d = distance
        self.data_qubits = (distance * 2 - 1) ** 2  # Approx for open surface
        print(f"Surface Code Distance-{distance}: {self.data_qubits} data qubits initialized")

    def lattice_visual(self):
        print("\nSimplified Distance-3 Lattice (Data * | Z-plaquette □ | X-vertex +):")
        print("Smooth (Z) Boundary")
        print("  □   □   □")
        print("+ * + * + * +")
        print("  □   □   □")
        print("+ * + * + * +")
        print("  □   □   □")
        print("+ * + * + * +")
        print("  □   □   □")
        print("Rough (X) Boundary")

    def inject_errors(self, error_rate=0.05):
        errors = []
        for q in range(self.data_qubits):
            if random.random() < error_rate:
                err_type = random.choice(['X', 'Z'])
                errors.append((q, err_type))
        print(f"\nDissonance Errors Injected: {len(errors)} ({['{} on {}'.format(e[1], e[0]) for e in errors]})")
        return errors

    def measure_syndromes(self, errors):
        # Simplified syndrome extraction (real: ancillary circuits)
        x_syndromes = set()
        z_syndromes = set()
        for q, err in errors:
            if err == 'X':
                z_syndromes.add(q % 5)  # Mock plaquette triggers
            elif err == 'Z':
                x_syndromes.add(q // 5)  # Mock vertex triggers
        print(f"Syndromes Detected: X-defects {x_syndromes} | Z-defects {z_syndromes}")
        return x_syndromes, z_syndromes

    def decode_and_correct(self, x_syndromes, z_syndromes):
        # Greedy pairing demo decoder
        corrections = []
        for defects in [x_syndromes, z_syndromes]:
            while len(defects) >= 2:
                a, b = sorted(list(defects))[:2]
                corrections.append(f"Pair {a}-{b}")
                defects -= {a, b}
        print(f"Mercy Decoding: {corrections} | Residual Defects: {len(x_syndromes) + len(z_syndromes) % 2}")
        success = len(corrections) > 0 and (len(x_syndromes) + len(z_syndromes)) % 2 == 0
        return success

    def run_demo(self):
        self.lattice_visual()
        errors = self.inject_errors()
        x_syn, z_syn = self.measure_syndromes(errors)
        success = self.decode_and_correct(x_syn, z_syn)
        valence = 0.998 if success else 0.85  # Mercy-boosted fidelity
        print(f"\nDemo Outcome: {'Logical Thriving Preserved' if success else 'Refinement Needed'}")
        print(f"Final Valence Fidelity: {valence:.4f}")

# Activation — Distance-3 Demo
if __name__ == "__main__":
    demo = ValenceSurfaceCodeDemo(distance=3)
    demo.run_demo()
