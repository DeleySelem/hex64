#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Check if the script is run with superuser (root) privileges
if [ "$EUID" -ne 0 ]; then
  echo "Please run this script as root (use sudo)"
  exit 1
fi

# Define variables
PROGRAM_NAME="hex64.py"       # Replace with your Python program file name
INSTALL_DIR="/usr/share/hex64" # Directory to store the program
COMMAND_NAME="hex64"          # Command name to execute the program
COMMAND_PATH="/usr/bin/$COMMAND_NAME" # Path to the command file

# Check for the program file in the current directory
if [ ! -f "$PROGRAM_NAME" ]; then
  echo "Error: $PROGRAM_NAME not found in the current directory."
  exit 1
fi

# Create the installation directory
echo "Creating installation directory at $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"

# Copy the program to the installation directory
echo "Copying $PROGRAM_NAME to $INSTALL_DIR..."
cp "$PROGRAM_NAME" "$INSTALL_DIR/"

# Make sure the program has a valid shebang (e.g., #!/usr/bin/env python3)
if ! head -n 1 "$INSTALL_DIR/$PROGRAM_NAME" | grep -q "^#!"; then
  echo "Adding shebang to $INSTALL_DIR/$PROGRAM_NAME..."
  sed -i '1i#!/usr/bin/env python3' "$INSTALL_DIR/$PROGRAM_NAME"
fi

# Make the program executable
echo "Making $INSTALL_DIR/$PROGRAM_NAME executable..."
chmod +x "$INSTALL_DIR/$PROGRAM_NAME"

# Create the command file in /usr/bin
echo "Creating command file at $COMMAND_PATH..."
echo "#!/bin/bash" > "$COMMAND_PATH"
echo "python3 $INSTALL_DIR/$PROGRAM_NAME \"\$@\"" >> "$COMMAND_PATH"

# Make the command file executable
chmod +x "$COMMAND_PATH"

# Verify installation
if command -v "$COMMAND_NAME" >/dev/null 2>&1; then
  echo "Installation complete! You can now run the program using the command: $COMMAND_NAME"
else
  echo "Error: The program was not installed successfully."
  exit 1
fi
