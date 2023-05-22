#!/bin/bash

# Navigate to the directory where the files are located
directory=$1
cd "$directory" || exit

# Remove files ending in .gz
rm -f *.gz

# Print a message after the removal
echo "Files with .gz extension have been removed."

