"""
G-main.py - runs the whole simulation using files A to F.

Run (from the src folder):   python G-main.py
Needs:                       pip install numpy matplotlib

File names contain "-" so they cannot be imported with a normal
"import" line. load_module() loads them from their file path instead.
"""

import importlib.util
import os


def load_module(file_name):
    """Load a python file that sits next to this one."""

    folder = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(folder, file_name)

    module_name = os.path.splitext(file_name)[0].replace("-", "_")
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


signal_generator = load_module("A-signal-generator.py")
sampler = load_module("B-sampler.py")
quantizer = load_module("C-quantizer.py")
binary_encoder = load_module("D-binary_encoder.py")
reconstructor = load_module("E-signal_reconstructor.py")
visualizer = load_module("F-visualizer.py")


# ------------------------------------------------------------------
# Parameters (change them to experiment)
# ------------------------------------------------------------------
FREQUENCY = 5        # signal frequency (Hz)
SAMPLING_RATE = 40   # fe (Hz) -> must be > 2 * FREQUENCY (Shannon)
DURATION = 1         # seconds
BITS = 3             # Nb -> L = 2**BITS quantization levels


def main():
    if SAMPLING_RATE <= 2 * FREQUENCY:
        print("Warning: fe <= 2 * f, the signal cannot be rebuilt correctly.")

    # 1. Analog signal
    time, original_signal = signal_generator.generate_signal(
        FREQUENCY, DURATION
    )

    # 2. Sampling
    sample_times, samples = sampler.sample_signal(
        FREQUENCY, SAMPLING_RATE, DURATION
    )

    # 3. Quantization
    quantized_samples, indices, step = quantizer.quantize_samples(
        samples, BITS
    )

    # 4. Binary encoding
    binary_codes = binary_encoder.encode_samples(indices, BITS)
    bit_rate = binary_encoder.calculate_bit_rate(SAMPLING_RATE, BITS)

    # 5. Reconstruction
    reconstructed_signal = reconstructor.reconstruct_signal(
        sample_times, quantized_samples, time
    )

    # Terminal output
    print(f"fe = {SAMPLING_RATE} Hz, Te = {1 / SAMPLING_RATE:.4f} s")
    print(f"L = {2 ** BITS} levels, step = {step:.4f}, Nb = {BITS} bits")
    print(f"Number of samples: {len(samples)}")
    print(f"Bit rate: {bit_rate} bit/s")
    print("First codes:", binary_codes[:10])

    # Graphs
    visualizer.plot_results(
        time,
        original_signal,
        sample_times,
        samples,
        quantized_samples,
        indices,
        binary_codes,
        reconstructed_signal,
        SAMPLING_RATE,
        BITS,
        step,
        bit_rate
    )


if __name__ == "__main__":
    main()
