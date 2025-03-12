import argparse
import os
import subprocess

# Trigram symbols
trigram_symbols = {
    '000': '☰',  # Heaven
    '001': '☱',  # Wind
    '010': '☲',  # Fire
    '011': '☳',  # Lake
    '100': '☵',  # Water
    '101': '☶',  # Mountain
    '110': '☴',  # Thunder
    '111': '☷',  # Earth
}

# Hexagram symbols for all 64 hexagrams
hexagram_symbols = {
    '000000': '䷀', '000001': '䷁', '000010': '䷂', '000011': '䷃',
    '000100': '䷄', '000101': '䷅', '000110': '䷆', '000111': '䷇',
    '001000': '䷈', '001001': '䷉', '001010': '䷊', '001011': '䷋',
    '001100': '䷌', '001101': '䷍', '001110': '䷎', '001111': '䷏',
    '010000': '䷐', '010001': '䷑', '010010': '䷒', '010011': '䷓',
    '010100': '䷔', '010101': '䷕', '010110': '䷖', '010111': '䷗',
    '011000': '䷘', '011001': '䷙', '011010': '䷚', '011011': '䷛',
    '011100': '䷜', '011101': '䷝', '011110': '䷞', '011111': '䷟',
    '100000': '䷠', '100001': '䷡', '100010': '䷢', '100011': '䷣',
    '100100': '䷤', '100101': '䷥', '100110': '䷦', '100111': '䷧',
    '101000': '䷨', '101001': '䷩', '101010': '䷪', '101011': '䷫',
    '101100': '䷬', '101101': '䷭', '101110': '䷮', '101111': '䷯',
    '110000': '䷰', '110001': '䷱', '110010': '䷲', '110011': '䷳',
    '110100': '䷴', '110101': '䷵', '110110': '䷶', '110111': '䷷',
    '111000': '䷸', '111001': '䷹', '111010': '䷺', '111011': '䷻',
    '111100': '䷼', '111101': '䷽', '111110': '䷾', '111111': '䷿',
}

def text_to_binary(text):
    """Convert text to binary string using UTF-8 encoding."""
    utf_bytes = text.encode('utf-8')
    return ''.join(f"{byte:08b}" for byte in utf_bytes)

def binary_to_trigrams(binary):
    """Split binary into trigrams, handling padding."""
    pad_len = (3 - (len(binary) % 3)) % 3
    if pad_len > 0:
        binary += '1' + '0' * (pad_len - 1)
    return [binary[i:i+3] for i in range(0, len(binary), 3)]

def trigrams_to_hexagrams(trigrams):
    """Convert trigrams to hexagrams, ensuring even pairs."""
    if len(trigrams) % 2 != 0:
        trigrams.append('000')
    return [trigrams[i] + trigrams[i+1] for i in range(0, len(trigrams), 2)]

def save_hexagrams(filename, hexagram_symbols_list):
    with open(f'hexed_{filename}', 'w') as f:
        f.write(''.join(hexagram_symbols_list))  # Save on one line

def decode_binary(binary_str):
    """Convert binary string back to text, removing padding."""
    pad_pos = binary_str.rfind('1')
    if pad_pos != -1 and all(c == '0' for c in binary_str[pad_pos + 1:]):
        binary_str = binary_str[:pad_pos]
    byte_array = bytearray()
    for i in range(0, len(binary_str), 8):
        byte_bits = binary_str[i:i + 8]
        if len(byte_bits) < 8:
            continue
        byte_array.append(int(byte_bits, 2))
    return byte_array.decode('utf-8', errors='ignore')

def main():
    parser = argparse.ArgumentParser(description='Convert a file to I Ching hexagrams and back.')
    parser.add_argument('-f', '--file', type=str, help='Input file to convert to hexagrams.')
    parser.add_argument('-d', '--decode', type=str, help='Decode hexagrams back to original text.')
    parser.add_argument('-r', '--run', type=str, help='Run a program using the provided hexed file.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print detailed encoding/decoding phases.')
    args = parser.parse_args()

    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            content = f.read()

        binary = text_to_binary(content)
        trigrams = binary_to_trigrams(binary)
        hexagrams = trigrams_to_hexagrams(trigrams)

        if args.verbose:
            print(f'Original Text:\n{content}')
            print(f'Binary Representation: {binary}')
            print(f'Trigram Symbols: {"".join(trigram_symbols.get(t, "?") for t in trigrams)}')

        hex_symbols = [hexagram_symbols.get(h, '?') for h in hexagrams]

        if args.verbose:
            print(f'Hexagram Symbols: {"".join(hex_symbols)}')

        save_hexagrams(args.file, hex_symbols)

        if args.verbose:
            print(f'Hexagrams saved as hexed_{os.path.basename(args.file)}.')

    elif args.decode:
        with open(args.decode, 'r') as f:
            hex_symbols = f.read().strip()  # Read entire line and strip whitespace

        # Create binary string from hex symbols
        binary_str = ''.join(
            next((k for k, v in hexagram_symbols.items() if v == hs), '000000')
            for hs in hex_symbols
        )

        if args.verbose:
            print(f'Hexagram Symbols:\n{"".join(hex_symbols)}')
            print(f'Decoded Binary (Raw): {binary_str}')

        trigrams_decoded = [binary_str[i:i + 3] for i in range(0, len(binary_str), 3)]
        trigram_symbols_decoded = [trigram_symbols.get(t, '?') for t in trigrams_decoded]

        if args.verbose:
            print(f'Decoded Trigram Symbols: {"".join(trigram_symbols_decoded)}')

        text = decode_binary(binary_str)

        if args.verbose:
            print(f'Decoded Text:\n{text}')

        decoded_file = f'decoded_{os.path.basename(args.decode)}'
        with open(decoded_file, 'w', encoding='utf-8') as f:
            f.write(text)

        if args.verbose:
            print(f'Decoded text saved as {decoded_file}.')

    elif args.run:
        with open(args.run, 'r') as f:
            hex_symbols = f.read().strip()  # Read entire line and strip whitespace

        binary_str = ''.join(
            next((k for k, v in hexagram_symbols.items() if v == hs), '000000')
            for hs in hex_symbols
        )

        trigrams_decoded = [binary_str[i:i + 3] for i in range(0, len(binary_str), 3)]
        trigram_symbols_decoded = [trigram_symbols.get(t, '?') for t in trigrams_decoded]

        if args.verbose:
            print(f'Decoded Trigram Symbols:\n{"".join(trigram_symbols_decoded)}')
            print(f'Decoded Binary (Raw):\n{binary_str}')

        text = decode_binary(binary_str)
        decoded_file = f'decoded_{os.path.basename(args.run)}'
        with open(decoded_file, 'w', encoding='utf-8') as f:
            f.write(text)

        if args.verbose:
            print(f'Decoded text saved as {decoded_file}.')

        try:
            subprocess.run(['python3', decoded_file], check=True)
        except subprocess.CalledProcessError as e:
            print(f'Error running script: {e}')

if __name__ == '__main__':
    main()
