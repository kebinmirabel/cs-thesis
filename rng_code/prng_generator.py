#!/usr/bin/env python3
"""
PRNG Generator using Mersenne Twister
Generates 64-bit random numbers with CSV logging
"""

import random
import time
import csv
from datetime import datetime
import argparse


def generate_prng_data(num_samples, output_file, seed=None):
    """
    Generate PRNG data using Mersenne Twister.
    
    Args:
        num_samples: Number of random samples to generate
        output_file: Output CSV file path
        seed: Random seed (if None, uses system time)
    """
    # Use system time as seed if not provided
    if seed is None:
        seed = int(time.time() * 1000000)  # Microsecond precision
    
    # Initialize Mersenne Twister with seed
    random.seed(seed)
    
    # Log the seed for repeatability
    print(f"Seed used: {seed}")
    print(f"Generating {num_samples} samples...")
    
    # Write seed to a separate log file
    seed_log_file = output_file.replace('.csv', '_seed.txt')
    with open(seed_log_file, 'w') as f:
        f.write(f"Seed: {seed}\n")
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"Samples: {num_samples}\n")
    
    # Generate random numbers and write to CSV
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['number', 'binary', 'timestamp'])
        
        for i in range(num_samples):
            # Generate a 64-bit random number
            random_num = random.getrandbits(64)
            
            # Convert to 64-bit binary string (without '0b' prefix)
            binary_str = format(random_num, '064b')
            
            # Get current timestamp
            timestamp = datetime.now().isoformat()
            
            # Write row to CSV
            writer.writerow([random_num, binary_str, timestamp])
            
            # Progress indicator
            if (i + 1) % 10000 == 0:
                print(f"Generated {i + 1}/{num_samples} samples...")
    
    print(f"Complete! Data written to {output_file}")
    print(f"Seed logged in {seed_log_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Generate PRNG data using Mersenne Twister (64-bit)'
    )
    parser.add_argument(
        '-n', '--num-samples',
        type=int,
        default=76801,
        help='Number of random samples to generate (default: 1000)'
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='prng_output.csv',
        help='Output CSV file path (default: prng_output.csv)'
    )
    parser.add_argument(
        '-s', '--seed',
        type=int,
        default=None,
        help='Random seed (default: uses system time)'
    )
    
    args = parser.parse_args()
    
    generate_prng_data(args.num_samples, args.output, args.seed)


if __name__ == '__main__':
    main()
