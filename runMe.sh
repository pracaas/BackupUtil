#!/bin/bash

# Install Python dependencies from requirements.txt
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if the installation was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to install Python dependencies."
    exit 1
fi

# Run the Python script
echo "Running the Python script..."
python3 DataSafeGuard.py

# Check if the Python script executed successfully
if [ $? -ne 0 ]; then
    echo "Error: Failed to run the DataSafeGuard script."
    exit 1
fi

echo "Script execution completed successfully."
