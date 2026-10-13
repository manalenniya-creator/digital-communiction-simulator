import matplotlib.pyplot as plt


def plot_results(
    time,
    original_signal,
    sample_times,
    samples,
    quantized_samples,
    indices,
    binary_codes,
    reconstructed_signal,
    sampling_rate,
    bits,
    step,
    bit_rate,
    minimum=-1.0
):
    """Display every stage of the simulation on its own graph."""

    levels_count = 2 ** bits

    # constrained_layout re-arranges the plots when the window is resized
    fig = plt.figure(figsize=(12, 9), constrained_layout=True)
    grid = fig.add_gridspec(3, 2, height_ratios=[1, 1, 1])

    # 1) Analog signal
    ax1 = fig.add_subplot(grid[0, 0])
    ax1.plot(time, original_signal, label="Analog signal")
    ax1.set_title("1. Signal analogique")
    ax1.set_xlabel("Time (s)")
    ax1.set_ylabel("Amplitude")
    ax1.grid(True)
    ax1.legend(loc="upper right")

    # 2) Sampling
    ax2 = fig.add_subplot(grid[0, 1])
    ax2.plot(time, original_signal, "--", color="gray",
             label="Analog signal")
    ax2.stem(sample_times, samples,
             linefmt="r-", markerfmt="ro", basefmt="k-",
             label="Samples")
    ax2.set_title(
        f"2. Echantillonnage (fe = {sampling_rate} Hz, "
        f"Te = {1 / sampling_rate:.3f} s)"
    )
    ax2.set_xlabel("Time (s)")
    ax2.set_ylabel("Amplitude")
    ax2.grid(True)
    ax2.legend(loc="upper right")

    # 3) Quantization
    ax3 = fig.add_subplot(grid[1, 0])
    for k in range(levels_count + 1):
        ax3.axhline(minimum + k * step,
                    color="lightgray", linewidth=0.8)
    ax3.vlines(sample_times, samples, quantized_samples,
               colors="gray", linestyles=":")
    ax3.plot(sample_times, samples, "ro", label="Samples")
    ax3.plot(sample_times, quantized_samples, "gs",
             label="Quantized samples")
    ax3.set_title(
        f"3. Quantification (L = {levels_count}, "
        f"pas = {step:.3f})"
    )
    ax3.set_xlabel("Time (s)")
    ax3.set_ylabel("Amplitude")
    ax3.legend(loc="lower right")

    # 4) Binary encoding (table of the first samples)
    ax4 = fig.add_subplot(grid[1, 1])
    ax4.axis("off")
    ax4.set_title(f"4. Codage binaire (Nb = {bits} bits par echantillon)")

    count = min(6, len(samples))
    lines = ["n    value     level   code"]
    for n in range(count):
        lines.append(
            f"{n:<4d} {samples[n]:+.3f}    {indices[n]:<7d} "
            f"{binary_codes[n]}"
        )
    lines.append("...")

    # one single text block, so the lines can never overlap each other
    stream = "".join(binary_codes[:8])
    lines.append("")
    lines.append("Bit stream (8 first samples):")
    lines.append(f"{stream}...")
    lines.append(
        f"Bit rate = fe x Nb = {sampling_rate} x {bits} "
        f"= {bit_rate} bit/s"
    )
    ax4.text(0.0, 1.0, "\n".join(lines),
             family="monospace", fontsize=8, va="top")

    # 5) Reconstruction
    ax5 = fig.add_subplot(grid[2, :])
    ax5.plot(time, original_signal, color="gray",
             label="Original signal")
    ax5.step(sample_times, quantized_samples,
             where="post", color="green", alpha=0.6,
             label="Quantized samples")
    ax5.plot(time, reconstructed_signal, "--", color="red",
             label="Reconstructed signal")
    ax5.set_title("5. Reconstruction")
    ax5.set_xlabel("Time (s)")
    ax5.set_ylabel("Amplitude")
    ax5.grid(True)
    ax5.legend(loc="lower right")

    plt.show()


# Run this file alone to see all the stages together:  python F-visualizer.py
if __name__ == "__main__":
    from _loader import load_module

    load_module("G-main.py").main()