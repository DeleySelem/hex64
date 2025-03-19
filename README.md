# HEX64: I-Ching Hexagram Encoder and Decoder

HEX64 is a Python tool that encodes text files into I-Ching hexagrams and decodes them back into their original form. It also supports executing encoded Python and Bash scripts. The project includes an installation script for system-wide access as a command-line tool.

## Features

- **Encoding**: Convert text files into I-Ching hexagrams.
- **Decoding**: Restore encoded hexagram files to their original content.
- **Execution**: Run Python and Bash scripts encoded in hexagrams directly.
- **Verbose Mode**: View detailed encoding/decoding steps for debugging.
- **Global Installation**: Deploy HEX64 as a command-line tool (`hex64`).

## Installation

Use the provided Bash script (`install.sh`) to install HEX64 as a global command.

### Steps to Install

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/hex64.git
   cd hex64
   ```

2. Run the installation script with superuser privileges:
   ```bash
   sudo ./install.sh
   ```

3. Once installed, you can use the `hex64` command anywhere on your system.

## Usage

You can use HEX64 for encoding, decoding, or executing hexagram-encoded files.

### Command-Line Options

```text
Usage: hex64.py [options]

Options:
  -f, --file        Encode a file to I-Ching hexagrams.
  -d, --decode      Decode hexagrams back to the original text.
  -rp, --run-python Run an encoded Python program as a Python3 program.
  -rb, --run-bash   Run an encoded Bash program as a Bash script.
  -v, --verbose     Print detailed encoding/decoding phases.
  -h, --help        Display this help screen.
```

### Examples

#### Encoding a File
Convert a file (`example.txt`) into hexagrams:
```bash
hex64 -f example.txt
```
The encoded file will be saved as `hexed_example.txt`.

#### Decoding a File
Restore the original content from an encoded file:
```bash
hex64 -d hexed_example.txt
```
The decoded content will be saved as `decoded_hexed_example.txt`.

#### Running an Encoded Python Script
Decode and execute a hexagram-encoded Python script:
```bash
hex64 -rp encoded_script.txt
```

#### Verbose Mode
To view detailed steps during encoding or decoding:
```bash
hex64 -f example.txt -v
```

## How It Works

1. **Encoding**:
   - Converts text into binary using UTF-8 encoding.
   - Splits the binary into trigrams and maps them to I-Ching symbols.
   - Groups trigrams into hexagrams and saves them as an encoded file.

2. **Decoding**:
   - Converts hexagrams back into binary.
   - Reconstructs the original text from binary.

3. **Execution**:
   - Decodes hexagram-encoded Python or Bash scripts.
   - Executes the decoded scripts using Python or Bash interpreters.

## File Descriptions

### `hex64.py`
The main Python script for encoding, decoding, and executing hexagram-encoded files.

### `install.sh`
A Bash script to install HEX64 as a system-wide command (`hex64`).

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Author

**Deley Selem**  
Feel free to contribute, open issues, or suggest improvements!

