import numpy as np


def quantize_samples(samples, bits, minimum=-1.0, maximum=1.0):
    """Stage 3: uniform quantization (same method as the course).

    - [minimum, maximum] is divided into L = 2**bits zones
    - zone width (step) = (maximum - minimum) / L
    - each zone gets an index from 0 to L-1
    - each sample is replaced by the middle of its zone
    """

    levels_count = 2 ** bits
    step = (maximum - minimum) / levels_count

    indices = np.floor(
        (samples - minimum) / step
    ).astype(int)

    indices = np.clip(indices, 0, levels_count - 1)

    quantized = minimum + (indices + 0.5) * step

    return quantized, indices, step


# Run this file alone to see the result of stage 3:  python C-quantizer.py
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from _loader import load_module

    sampler = load_module("B-sampler.py")

    FREQUENCY = 5       # Hz
    SAMPLING_RATE = 40  # Hz
    DURATION = 1        # seconds
    BITS = 3            # L = 2**BITS levels
    MINIMUM, MAXIMUM = -1.0, 1.0

    sample_times, samples = sampler.sample_signal(
        FREQUENCY, SAMPLING_RATE, DURATION
    )
    quantized, indices, step = quantize_samples(
        samples, BITS, MINIMUM, MAXIMUM
    )
    levels_count = 2 ** BITS

    print("Stage 3 - Quantization")
    print(f"L = {levels_count} levels, step = {step:.3f}")
    print("n    sample    zone   quantized")
    for n in range(8):
        print(f"{n:<4d} {samples[n]:+.3f}    {indices[n]:<6d} "
              f"{quantized[n]:+.3f}")

    plt.figure(figsize=(9, 5))
    for k in range(levels_count + 1):
        plt.axhline(MINIMUM + k * step,
                    color="lightgray", linewidth=0.8)
    plt.vlines(sample_times, samples, quantized,
               colors="gray", linestyles=":")
    plt.plot(sample_times, samples, "ro", label="Samples")
    plt.plot(sample_times, quantized, "gs",
             label="Quantized (middle of zone)")
    plt.title(f"Stage 3 - Quantization (L = {levels_count}, "
              f"step = {step:.3f})")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.show()
