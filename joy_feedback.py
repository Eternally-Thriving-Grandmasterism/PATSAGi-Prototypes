import pandas as pd
import matplotlib.pyplot as plt

def joy_feedback(csv_file):
    df = pd.read_csv(csv_file)  # Columns: timestamp, member, joy_level (1-10), needs_met, comments
    df['joy_normalized'] = df['joy_level'] / 10
    avg_joy = df['joy_normalized'].mean()
    print(f"Collective Joy Valence: {avg_joy:.4f}")

    df.plot(kind='line', x='timestamp', y='joy_normalized', title='Joy Resonance Over Time')
    plt.show()

    return avg_joy
