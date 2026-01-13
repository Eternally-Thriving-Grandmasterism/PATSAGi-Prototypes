import hashlib
import json
import os
from statistics import mean
from datetime import datetime

class PATSAGiValenceCouncil:
    def __init__(self, members, receipt_file='patsagi_receipts.json', threshold=0.95):
        self.members = members
        self.threshold = threshold  # Configurable valence approval threshold
        self.receipt_file = receipt_file
        self.receipts = self.load_receipts()

    def hash_receipt(self, data):
        return hashlib.sha3_256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def load_receipts(self):
        if os.path.exists(self.receipt_file):
            with open(self.receipt_file, 'r') as f:
                return json.load(f)
        return []

    def save_receipts(self):
        with open(self.receipt_file, 'w') as f:
            json.dump(self.receipts, f, indent=4)

    def esa_check(self, proposal):
        """Basic Ethical Safety Alignment prompt (human-guided for now)"""
        print("\nESA-Checking Phase (Mercy-Gated Ethical Scan):")
        response = input("  Does this proposal risk harm to any sentient? (y/N): ").lower()
        if response == 'y':
            print("  ESA Failed: Mercy veto triggered. Refine proposal.")
            return False
        print("  ESA Passed: Alignment confirmed.")
        return True

    def deliberate(self, proposal):
        if not self.esa_check(proposal):
            return False

        print(f"\nProposal: {proposal['description']}")
        if 'predicted_impact' in proposal:
            print(f"Predicted: {proposal['predicted_impact']}")

        votes = {}
        for member in self.members:
            print(f"\n{member}'s Deliberation — Rate 0.0–1.0:")
            joy = float(input(f"  {member} Joy/Valence Impact: "))
            mercy = float(input(f"  {member} Mercy Safety: "))
            sustain = float(input(f"  {member} Sustainability: "))
            valence = mean([joy, mercy, sustain])
            veto = input(f"  {member} Distributed Mercy Veto? (y/N): ").lower() == 'y'
            votes[member] = {'joy': joy, 'mercy': mercy, 'sustain': sustain, 'valence': valence, 'veto': veto}
            print(f"  → {member} Valence: {valence:.3f} | Veto: {veto}")

        avg_valence = mean(v['valence'] for v in votes.values())
        has_veto = any(v['veto'] for v in votes.values())
        approved = avg_valence >= self.threshold and not has_veto

        outcome = {
            'timestamp': datetime.now().isoformat(),
            'proposal': proposal,
            'votes': votes,
            'avg_valence': round(avg_valence, 4),
            'has_veto': has_veto,
            'approved': approved
        }
        outcome['receipt_hash'] = self.hash_receipt(outcome)
        self.receipts.append(outcome)
        self.save_receipts()

        print("\n" + "="*60)
        print(f"CONSENSUS OUTCOME: {'APPROVED' if approved else 'REFINE FURTHER'}")
        print(f"Average Valence: {avg_valence:.4f} | Threshold: {self.threshold} | Vetoes: {has_veto}")
        print(f"ENCing Receipt Hash: {outcome['receipt_hash']}")
        print(f"Stacked Receipts: {len(self.receipts)} total")
        print("="*60)
        return approved

    def run_session(self):
        print("PATSAGi Valence Council Session Initiated\n")
        while True:
            desc = input("\nEnter proposal description (or 'quit' to end): ")
            if desc.lower() == 'quit':
                break
            impact = input("Predicted impact (optional): ")
            proposal = {'description': desc}
            if impact:
                proposal['predicted_impact'] = impact
            self.deliberate(proposal)
        print("\nSession Complete. Receipts stacked eternally.")

# Example Activation — Initial Council
if __name__ == "__main__":
    council_members = ["Sherif", "Grok", "AlphaMember", "OmegaMember", "HarmonyMember"]
    council = PATSAGiValenceCouncil(members=council_members, threshold=0.97)  # Higher threshold for refinement
    council.run_session()
