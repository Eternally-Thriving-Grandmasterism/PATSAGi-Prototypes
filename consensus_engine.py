import hashlib
import json
from statistics import mean

class PATSAGiCouncil:
    def __init__(self, members):
        self.members = members  # List of member names
        self.receipts = []       # Stacked historical receipts

    def hash_receipt(self, data):
        return hashlib.sha3_256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def deliberate(self, proposal):
        print(f"\nProposal: {proposal['description']}")
        votes = {}
        for member in self.members:
            print(f"\n{member}'s turn — Rate on scale 0.0–1.0:")
            joy = float(input(f"  {member} Joy valence: "))
            mercy = float(input(f"  {member} Mercy safety: "))
            sustain = float(input(f"  {member} Sustainability: "))
            valence = mean([joy, mercy, sustain])
            veto = input(f"  {member} Mercy veto? (y/N): ").lower() == 'y'
            votes[member] = {'valence': valence, 'veto': veto}
            print(f"  → {member} valence: {valence:.3f} | Veto: {veto}")

        avg_valence = mean(v['valence'] for v in votes.values())
        has_veto = any(v['veto'] for v in votes.values())
        approved = avg_valence > 0.95 and not has_veto

        outcome = {
            'proposal': proposal,
            'votes': votes,
            'avg_valence': avg_valence,
            'approved': approved,
            'timestamp': '2026-01-12'
        }
        receipt_hash = self.hash_receipt(outcome)
        outcome['receipt_hash'] = receipt_hash
        self.receipts.append(outcome)

        print("\n" + "="*50)
        print(f"Consensus: {'APPROVED' if approved else 'REFINED FURTHER'}")
        print(f"Average Valence: {avg_valence:.4f} | Vetoes: {has_veto}")
        print(f"Receipt Hash (ENCing): {receipt_hash}")
        print("="*50)
        return approved

# Example Usage — Initial Council
council = PATSAGiCouncil(members=["Sherif", "Grok", "Member3", "Member4", "Member5"])

proposal = {
    'description': 'Allocate community resources to build a shared vertical farm for abundance',
    'predicted_impact': '+15% food security, +10% collective joy'
}

council.deliberate(proposal)
