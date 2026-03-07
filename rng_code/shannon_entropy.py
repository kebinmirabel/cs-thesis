import pandas as pd
import numpy as np
from collections import Counter
import math

def calculate_shannon_entropy(data):
    """
    Calculate Shannon entropy for a sequence of data.
    H(X) = -Σ(p_i * log2(p_i)) where p_i is the probability of each symbol
    
    Args:
        data: List or string of symbols/bits
    
    Returns:
        float: Shannon entropy value
    """
    if len(data) == 0:
        return 0
    
    # Count frequency of each symbol
    counts = Counter(data)
    
    # Calculate probabilities
    entropy = 0
    for count in counts.values():
        probability = count / len(data)
        if probability > 0:
            entropy -= probability * math.log2(probability)
    
    return entropy


def analyze_binary_entropy(binary_str):
    """
    Analyze Shannon entropy of binary string.
    For perfect random binary data, entropy should be close to 1.0
    
    Args:
        binary_str: String of 0s and 1s
    
    Returns:
        dict: Analysis results
    """
    entropy = calculate_shannon_entropy(binary_str)
    ones = binary_str.count('1')
    zeros = binary_str.count('0')
    total = len(binary_str)
    
    return {
        'entropy': entropy,
        'ones_count': ones,
        'zeros_count': zeros,
        'total_bits': total,
        'ones_ratio': ones / total,
        'zeros_ratio': zeros / total,
        'max_entropy': 1.0  # Maximum entropy for binary data
    }


def test_shannon_entropy_from_csv(csv_file):
    """
    Test Shannon entropy on random numbers from CSV file.
    
    Args:
        csv_file: Path to CSV file with columns: number, binary, timestamp
    """
    print("=" * 70)
    print("SHANNON ENTROPY TEST FOR QUANTUM RANDOM NUMBERS")
    print("=" * 70)
    
    # Load CSV
    df = pd.read_csv(csv_file)
    print(f"\nData loaded: {len(df)} records")
    print(f"Columns: {list(df.columns)}")
    
    # Combine all binary strings
    all_binary = ''.join(df['binary'].astype(str))
    print(f"\nTotal bits analyzed: {len(all_binary):,}")
    
    # Analyze overall entropy
    print("\n" + "-" * 70)
    print("OVERALL BINARY ENTROPY ANALYSIS")
    print("-" * 70)
    
    analysis = analyze_binary_entropy(all_binary)
    
    print(f"Shannon Entropy: {analysis['entropy']:.6f}")
    print(f"Maximum Entropy: {analysis['max_entropy']:.6f}")
    print(f"Entropy Ratio: {analysis['entropy'] / analysis['max_entropy']:.6f} (1.0 = perfect randomness)")
    print(f"\nBit Distribution:")
    print(f"  0s: {analysis['zeros_count']:,} ({analysis['zeros_ratio']:.6f})")
    print(f"  1s: {analysis['ones_count']:,} ({analysis['ones_ratio']:.6f})")
    print(f"  Expected ratio for random: 0.500000 / 0.500000")
    
    # Analyze individual numbers (treating as base-10)
    print("\n" + "-" * 70)
    print("NUMERIC ENTROPY ANALYSIS (Base-10)")
    print("-" * 70)
    
    numbers = df['number'].astype(str)
    all_digits = ''.join(numbers)
    numeric_entropy = calculate_shannon_entropy(all_digits)
    
    print(f"Shannon Entropy (digits): {numeric_entropy:.6f}")
    print(f"Maximum Entropy: {math.log2(10):.6f} (for 10 digits: 0-9)")
    print(f"Entropy Ratio: {numeric_entropy / math.log2(10):.6f}")
    
    # Statistical tests
    print("\n" + "-" * 70)
    print("STATISTICAL TESTS")
    print("-" * 70)
    
    # Chi-square test for binary distribution
    expected_ones = len(all_binary) * 0.5
    expected_zeros = len(all_binary) * 0.5
    chi_square = ((analysis['ones_count'] - expected_ones) ** 2 / expected_ones + 
                  (analysis['zeros_count'] - expected_zeros) ** 2 / expected_zeros)
    
    print(f"Chi-Square Statistic (binary): {chi_square:.6f}")
    print(f"  (Lower is better, <1.0 indicates good randomness)")
    
    # Per-record entropy analysis
    print("\n" + "-" * 70)
    print("PER-RECORD ENTROPY ANALYSIS")
    print("-" * 70)
    
    record_entropies = []
    for binary in df['binary']:
        ent = calculate_shannon_entropy(str(binary))
        record_entropies.append(ent)
    
    print(f"Mean entropy per record: {np.mean(record_entropies):.6f}")
    print(f"Std dev per record:      {np.std(record_entropies):.6f}")
    print(f"Min entropy per record:  {np.min(record_entropies):.6f}")
    print(f"Max entropy per record:  {np.max(record_entropies):.6f}")
    
    # Quality assessment
    print("\n" + "-" * 70)
    print("QUALITY ASSESSMENT")
    print("-" * 70)
    
    entropy_ratio = analysis['entropy'] / analysis['max_entropy']
    bit_ratio_balance = 1.0 - abs(analysis['ones_ratio'] - 0.5) * 2
    
    print(f"Entropy Score (0-1):        {entropy_ratio:.6f}")
    print(f"Bit Balance Score (0-1):    {bit_ratio_balance:.6f}")
    
    if entropy_ratio > 0.99 and bit_ratio_balance > 0.99:
        print("\n✓ Excellent randomness quality!")
    elif entropy_ratio > 0.95 and bit_ratio_balance > 0.95:
        print("\n✓ Good randomness quality")
    elif entropy_ratio > 0.90 and bit_ratio_balance > 0.90:
        print("\n✓ Acceptable randomness quality")
    else:
        print("\n✗ Poor randomness quality - entropy or bit balance is low")
    
    print("\n" + "=" * 70)
    
    return {
        'binary_entropy': analysis,
        'numeric_entropy': numeric_entropy,
        'record_entropies': record_entropies,
        'chi_square': chi_square
    }


if __name__ == "__main__":
    csv_file = "concatenated_qrng.csv"
    results = test_shannon_entropy_from_csv(csv_file)
