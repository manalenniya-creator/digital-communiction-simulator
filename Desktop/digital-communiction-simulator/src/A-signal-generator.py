import numpy as np


def generate_signal(frequency, duration, points=1000):
    """Stage 1: generate a sinusoidal analog signal."""

    time = np.linspace(
        0, duration, points, endpoint=False
    )

    signal = np.sin(2 * np.pi * frequency * time)

    return time, signal


# Run this file alone to see the result of stage 1:  python A-signal-generator.py
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    FREQUENCY = 5   # Hz
    DURATION = 1    # seconds

    time, signal = generate_signal(FREQUENCY, DURATION)

    print("Stage 1 - Analog signal")
    print(f"frequency = {FREQUENCY} Hz, duration = {DURATION} s")
    print(f"points    = {len(time)} (looks continuous)")

    plt.figure(figsize=(9, 4))
    plt.plot(time, signal)
    plt.title(f"Stage 1 - Analog signal (f = {FREQUENCY} Hz)")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
