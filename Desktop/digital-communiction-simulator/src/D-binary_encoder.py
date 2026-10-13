def encode_samples(indices, bits):
    """Stage 4: encode quantization indices into binary strings."""

    binary_codes = [
        format(int(index), f"0{bits}b")
        for index in indices
    ]

    return binary_codes


def calculate_bit_rate(sampling_rate, bits):
    """Calculate the theoretical bit rate in bits per second."""

    return sampling_rate * bits


# Run this file alone to see the result of stage 4:  python D-binary_encoder.py
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from _loader import load_module

    sampler = load_module("B-sampler.py")
    quantizer = load_module("C-quantizer.py")

    FREQUENCY = 5       # Hz
    SAMPLING_RATE = 40  # Hz
    DURATION = 1        # seconds
    BITS = 3            # Nb = log2(L)

    sample_times, samples = sampler.sample_signal(
        FREQUENCY, SAMPLING_RATE, DURATION
    )
    quantized, indices, step = quantizer.quantize_samples(samples, BITS)

    codes = encode_samples(indices, BITS)
    bit_rate = calculate_bit_rate(SAMPLING_RATE, BITS)

    print("Stage 4 - Binary encoding")
    print(f"Nb = {BITS} bits per sample")
    print("n    zone   code")
    for n in range(8):
        print(f"{n:<4d} {indices[n]:<6d} {codes[n]}")
    print(f"Bit rate = fe x Nb = {SAMPLING_RATE} x {BITS} = {bit_rate} bit/s")

    # Draw the first 8 codes as a digital signal (0 and 1)
    stream = "".join(codes[:8])
    bits_list = [int(b) for b in stream]

    plt.figure(figsize=(11, 3.5))
    plt.step(range(len(bits_list) + 1), bits_list + [bits_list[-1]],
             where="post")
    for i, b in enumerate(bits_list):
        plt.text(i + 0.5, 0.5, str(b), ha="center", va="center",
                 fontsize=10)
    for n in range(8):
        plt.axvline(n * BITS, color="red", linestyle="--", linewidth=0.8)
        plt.text(n * BITS + BITS / 2, 1.25, codes[n], ha="center",
                 color="red", fontsize=9)
    plt.ylim(-0.3, 1.5)
    plt.yticks([0, 1])
    plt.title("Stage 4 - Binary stream (8 first samples)")
    plt.xlabel("Bit position")
    plt.ylabel("Bit value")
    plt.tight_layout()
    plt.show()
