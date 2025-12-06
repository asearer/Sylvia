#!/bin/bash

# Ensure we are in the project root
cd "$(dirname "$0")"

# Generate certs if they don't exist
if [ ! -f "cert.pem" ] || [ ! -f "key.pem" ]; then
    ./scripts/generate_cert.sh
fi

echo "Starting Sylvia in SECURE mode (HTTPS)..."
echo "Note: You will see a security warning in your browser. This is normal for self-signed certificates."
echo "Access at: https://localhost:8501"

.venv/bin/streamlit run apps/sylvia_app/src/main.py \
    --server.port 8501 \
    --server.sslCertFile cert.pem \
    --server.sslKeyFile key.pem \
    --server.headless true
