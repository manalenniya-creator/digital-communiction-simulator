import numpy as np


def sample_signal(frequency, sampling_rate, duration):
    """Stage 2: sample a sinusoidal signal (fe = 1 / Te)."""

    sample_times = np.arange(
        0, duration, 1 / sampling_rate
    )

    samples = np.sin(
        2 * np.pi * frequency * sample_times
    )

    return sample_times, samples


# Run this file alone to see the result of stage 2:  python B-sampler.py
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from _loader import load_module

    generator = load_module("A-signal-generator.py")

    FREQUENCY = 5       # Hz
    SAMPLING_RATE = 40  # fe in Hz
    DURATION = 1        # seconds

    time, signal = generator.generate_signal(FREQUENCY, DURATION)
    sample_times, samples = sample_signal(
        FREQUENCY, SAMPLING_RATE, DURATION
    )

    print("Stage 2 - Sampling")
    print(f"fe = {SAMPLING_RATE} Hz, Te = {1 / SAMPLING_RATE:.4f} s")
    print(f"samples in {DURATION} s: {len(samples)}")
    print("first values:", np.round(samples[:8], 3))

    plt.figure(figsize=(9, 4))
    plt.plot(time, signal, "--", color="gray", label="Analog signal")
    plt.stem(sample_times, samples,
             linefmt="r-", markerfmt="ro", basefmt="k-",
             label="Samples")
    plt.title(f"Stage 2 - Sampling (fe = {SAMPLING_RATE} Hz)")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()
