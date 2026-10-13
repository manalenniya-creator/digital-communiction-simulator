import numpy as np


def reconstruct_signal(sample_times, quantized_samples, time):
    """Stage 5: reconstruct a signal using linear interpolation."""

    reconstructed = np.interp(
        time,
        sample_times,
        quantized_samples
    )

    return reconstructed


# Run this file alone to see the result of stage 5:  python E-signal_reconstructor.py
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from _loader import load_module

    generator = load_module("A-signal-generator.py")
    sampler = load_module("B-sampler.py")
    quantizer = load_module("C-quantizer.py")

    FREQUENCY = 5       # Hz
    SAMPLING_RATE = 40  # Hz
    DURATION = 1        # seconds
    BITS = 3

    time, signal = generator.generate_signal(FREQUENCY, DURATION)
    sample_times, samples = sampler.sample_signal(
        FREQUENCY, SAMPLING_RATE, DURATION
    )
    quantized, indices, step = quantizer.quantize_samples(samples, BITS)

    reconstructed = reconstruct_signal(sample_times, quantized, time)
    # compare only inside the sampled range (after the last sample
    # there is nothing left to interpolate)
    inside = time <= sample_times[-1]
    max_error = np.max(np.abs(signal[inside] - reconstructed[inside]))

    print("Stage 5 - Reconstruction")
    print(f"max error vs original signal = {max_error:.3f}")
    print("(error comes from quantization and from the straight "
          "lines between samples)")

    plt.figure(figsize=(9, 4.5))
    plt.plot(time, signal, color="gray", label="Original signal")
    plt.step(sample_times, quantized, where="post",
             color="green", alpha=0.6, label="Quantized samples")
    plt.plot(time, reconstructed, "--", color="red",
             label="Reconstructed signal")
    plt.title("Stage 5 - Reconstruction")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.show()
