#!/usr/bin/env bash
# Exit on error
set -o errexit

echo ">>> Step 1: Building React Vite Frontend..."
cd frontend
npm install
npm run build
cd ..

echo ">>> Step 2: Installing Python Backend Dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

echo ">>> Deployment Build Complete!"
