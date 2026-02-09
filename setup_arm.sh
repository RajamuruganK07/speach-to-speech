#!/bin/bash

echo "Setting up Speech-to-Speech Translation Project for Arm..."

# 1. Uninstall existing llama-cpp-python to ensure clean install
echo "Uninstalling llama-cpp-python..."
pip uninstall -y llama-cpp-python

# 2. Install with Arm Optimizations (NEON / OpenBLAS)
echo "Installing llama-cpp-python with optimization flags..."

# Check for Apple Silicon vs Generic Arm
if [[ "$(uname -m)" == "arm64" && "$(uname -s)" == "Darwin" ]]; then
    echo "Detected Apple Silicon"
    CMAKE_ARGS="-DLLAMA_Metal=on" pip install llama-cpp-python --no-cache-dir
else
    echo "Detected Generic Arm / Android / Linux"
    # Enable OpenBLAS if available, otherwise fallback to default which often has NEON enabled
    # Users might need to install libopenblas-dev first: sudo apt install libopenblas-dev
    CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_OPENBLAS=ON" pip install llama-cpp-python --no-cache-dir
fi

# 3. Install other dependencies
echo "Installing other dependencies..."
pip install -r requirements.txt

echo "Setup complete! Please ensure you have downloaded the models to the 'models' directory."
