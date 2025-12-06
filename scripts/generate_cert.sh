#!/bin/bash

# Generate self-signed certificate for development
echo "Generating self-signed certificate..."
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

echo "Certificate generation complete: cert.pem, key.pem"
