import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from typing import Tuple, List

def calculate_autocorrelation(data: np.ndarray, max_lag: int = 100) -> np.ndarray:
    """
    Calculate autocorrelation function (ACF) for a sequence.
    
    For random data, ACF should be ~0 at all non-zero lags and 1.0 at lag 0.
    
    Args:
        data: Input sequence (array or list)
        max_lag: Maximum lag to calculate
    
    Returns:
        Array of autocorrelation values for lags 0 to max_lag
    """
    data = np.asarray(data, dtype=float)
    data_mean = np.mean(data)
    c0 = np.sum((data - data_mean) ** 2) / len(data)
    
    acf_values = np.ones(max_lag + 1)
    
    for lag in range(1, max_lag + 1):
        c_lag = np.sum((data[:-lag] - data_mean) * (data[lag:] - data_mean)) / len(data)
        acf_values[lag] = c_lag / c0
    
    return acf_values


def confidence_interval_bounds(n: int, confidence: float = 0.95) -> float:
    """
    Calculate confidence interval bounds for autocorrelation under null hypothesis.
    Bounds: ±z * sqrt(1/n) where z is critical value
    
    Args:
        n: Sample size
        confidence: Confidence level (default 95%)
    
    Returns:
        float: Upper bound of confidence interval
    """
    z = stats.norm.ppf((1 + confidence) / 2)
    return z / np.sqrt(n)


def analyze_binary_autocorrelation(binary_str: str, max_lag: int = 100) -> dict:
    """
    Analyze autocorrelation of binary sequence.
    
    Args:
        binary_str: String of 0s and 1s
        max_lag: Maximum lag to analyze
    
    Returns:
        dict: Autocorrelation analysis results
    """
    binary_array = np.array([int(bit) for bit in binary_str])
    acf = calculate_autocorrelation(binary_array, max_lag)
    
    # Confidence bounds (95%)
    ci_bound = confidence_interval_bounds(len(binary_array))
    
    # Count significant spikes (outside CI)
    significant_lags = np.sum(np.abs(acf[1:]) > ci_bound)
    
    # Calculate mean absolute autocorrelation (excluding lag 0)
    mean_abs_acf = np.mean(np.abs(acf[1:]))
    
    return {
        'acf': acf,
        'ci_bound': ci_bound,
        'significant_lags': significant_lags,
        'total_lags': max_lag,
        'mean_abs_acf': mean_abs_acf,
        'max_acf': np.max(np.abs(acf[1:])),
        'percent_significant': (significant_lags / max_lag) * 100
    }


def analyze_numeric_autocorrelation(numbers: np.ndarray, max_lag: int = 100) -> dict:
    """
    Analyze autocorrelation of numeric sequence.
    
    Args:
        numbers: Array of numeric values
        max_lag: Maximum lag to analyze
    
    Returns:
        dict: Autocorrelation analysis results
    """
    acf = calculate_autocorrelation(numbers, max_lag)
    ci_bound = confidence_interval_bounds(len(numbers))
    significant_lags = np.sum(np.abs(acf[1:]) > ci_bound)
    mean_abs_acf = np.mean(np.abs(acf[1:]))
    
    return {
        'acf': acf,
        'ci_bound': ci_bound,
        'significant_lags': significant_lags,
        'total_lags': max_lag,
        'mean_abs_acf': mean_abs_acf,
        'max_acf': np.max(np.abs(acf[1:])),
        'percent_significant': (significant_lags / max_lag) * 100
    }


def test_autocorrelation_from_csv(csv_file: str, max_lag: int = 100) -> dict:
    """
    Perform autocorrelation analysis on quantum random numbers from CSV.
    
    Args:
        csv_file: Path to CSV file
        max_lag: Maximum lag to analyze
    
    Returns:
        dict: Complete autocorrelation analysis results
    """
    print("=" * 80)
    print("AUTOCORRELATION ANALYSIS FOR QUANTUM RANDOM NUMBERS")
    print("=" * 80)
    
    # Load CSV
    df = pd.read_csv(csv_file)
    print(f"\nData loaded: {len(df)} records")
    
    # ==================== BINARY ANALYSIS ====================
    print("\n" + "=" * 80)
    print("BINARY SEQUENCE AUTOCORRELATION")
    print("=" * 80)
    
    all_binary = ''.join(df['binary'].astype(str))
    print(f"Total bits analyzed: {len(all_binary):,}")
    
    binary_results = analyze_binary_autocorrelation(all_binary, max_lag)
    
    print(f"\nAutocorrelation Analysis (lag 0 to {max_lag}):")
    print(f"  Confidence Interval (95%): ±{binary_results['ci_bound']:.6f}")
    print(f"  Mean absolute ACF: {binary_results['mean_abs_acf']:.6f}")
    print(f"  Max absolute ACF: {binary_results['max_acf']:.6f}")
    print(f"  Significant spikes: {binary_results['significant_lags']}/{binary_results['total_lags']} ({binary_results['percent_significant']:.2f}%)")
    
    print(f"\nAutocorrelation values at key lags:")
    for lag in [1, 2, 5, 10, 20, 50, 100]:
        if lag <= max_lag:
            acf_val = binary_results['acf'][lag]
            status = "(SIGNIFICANT)" if abs(acf_val) > binary_results['ci_bound'] else ""
            print(f"  Lag {lag:3d}: {acf_val:10.6f} {status}")
    
    # ==================== NUMERIC ANALYSIS ====================
    print("\n" + "=" * 80)
    print("NUMERIC SEQUENCE AUTOCORRELATION")
    print("=" * 80)
    
    numbers = df['number'].values
    print(f"Total numbers analyzed: {len(numbers):,}")
    print(f"Number range: {numbers.min()} to {numbers.max()}")
    
    numeric_results = analyze_numeric_autocorrelation(numbers, max_lag)
    
    print(f"\nAutocorrelation Analysis (lag 0 to {max_lag}):")
    print(f"  Confidence Interval (95%): ±{numeric_results['ci_bound']:.6f}")
    print(f"  Mean absolute ACF: {numeric_results['mean_abs_acf']:.6f}")
    print(f"  Max absolute ACF: {numeric_results['max_acf']:.6f}")
    print(f"  Significant spikes: {numeric_results['significant_lags']}/{numeric_results['total_lags']} ({numeric_results['percent_significant']:.2f}%)")
    
    print(f"\nAutocorrelation values at key lags:")
    for lag in [1, 2, 5, 10, 20, 50, 100]:
        if lag <= max_lag:
            acf_val = numeric_results['acf'][lag]
            status = "(SIGNIFICANT)" if abs(acf_val) > numeric_results['ci_bound'] else ""
            print(f"  Lag {lag:3d}: {acf_val:10.6f} {status}")
    
    # ==================== INTERPRETATION ====================
    print("\n" + "=" * 80)
    print("INTERPRETATION")
    print("=" * 80)
    
    print(f"\nFor truly random data:")
    print(f"  - ACF should be ~0 at all non-zero lags")
    print(f"  - <5% of lags should exceed confidence bounds (by chance alone)")
    print(f"  - No patterns in the ACF plot")
    
    binary_quality = binary_results['percent_significant']
    numeric_quality = numeric_results['percent_significant']
    
    print(f"\nYour results:")
    print(f"  Binary sequence: {binary_quality:.1f}% significant lags", end="")
    if binary_quality < 8:
        print(" ✓ EXCELLENT (below expected 5%)")
    elif binary_quality < 15:
        print(" ✓ GOOD")
    elif binary_quality < 25:
        print(" ⊙ ACCEPTABLE")
    else:
        print(" ✗ POOR (indicates correlation)")
    
    print(f"  Numeric sequence: {numeric_quality:.1f}% significant lags", end="")
    if numeric_quality < 8:
        print(" ✓ EXCELLENT (below expected 5%)")
    elif numeric_quality < 15:
        print(" ✓ GOOD")
    elif numeric_quality < 25:
        print(" ⊙ ACCEPTABLE")
    else:
        print(" ✗ POOR (indicates correlation)")
    
    print(f"\nConclusion:")
    if binary_quality < 10 and numeric_quality < 10:
        print("  ✓ No significant autocorrelation detected.")
        print("    The sequence shows excellent independence between samples.")
    elif binary_quality < 15 and numeric_quality < 15:
        print("  ✓ Minimal autocorrelation detected.")
        print("    The sequence shows good independence between samples.")
    else:
        print("  ⚠ Moderate autocorrelation detected.")
        print("    Investigate for potential temporal dependencies.")
    
    print("\n" + "=" * 80)
    
    # Create visualizations
    create_acf_plots(binary_results, numeric_results, csv_file)
    
    return {
        'binary_results': binary_results,
        'numeric_results': numeric_results,
        'csv_file': csv_file
    }


def create_acf_plots(binary_results: dict, numeric_results: dict, csv_file: str):
    """
    Create ACF visualization plots.
    
    Args:
        binary_results: Binary autocorrelation results
        numeric_results: Numeric autocorrelation results
        csv_file: CSV file name for title
    """
    fig, axes = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle(f'Autocorrelation Analysis - {csv_file}', fontsize=14, fontweight='bold')
    
    lags = np.arange(len(binary_results['acf']))
    
    # Binary ACF plot
    ax = axes[0]
    ax.stem(lags, binary_results['acf'], linefmt='C0-', markerfmt='C0o', basefmt=' ')
    ax.axhline(y=binary_results['ci_bound'], color='r', linestyle='--', label='95% CI')
    ax.axhline(y=-binary_results['ci_bound'], color='r', linestyle='--')
    ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax.set_xlabel('Lag')
    ax.set_ylabel('ACF Value')
    ax.set_title(f'Binary Sequence ACF ({binary_results["percent_significant"]:.1f}% significant)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Numeric ACF plot
    ax = axes[1]
    ax.stem(lags, numeric_results['acf'], linefmt='C1-', markerfmt='C1o', basefmt=' ')
    ax.axhline(y=numeric_results['ci_bound'], color='r', linestyle='--', label='95% CI')
    ax.axhline(y=-numeric_results['ci_bound'], color='r', linestyle='--')
    ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax.set_xlabel('Lag')
    ax.set_ylabel('ACF Value')
    ax.set_title(f'Numeric Sequence ACF ({numeric_results["percent_significant"]:.1f}% significant)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    # Save plot
    output_file = csv_file.replace('.csv', '_autocorrelation.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n✓ ACF plot saved to: {output_file}")
    
    plt.close()


if __name__ == "__main__":
    csv_file = "concatenated_qrng.csv"
    results = test_autocorrelation_from_csv(csv_file, max_lag=100)
