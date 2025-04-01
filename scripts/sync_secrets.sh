#!/bin/bash

# Check if .env exists
if [ ! -f .env ]; then
  echo "Error: .env file not found"
  exit 1
fi

# Check if flyctl is installed
if ! command -v flyctl &>/dev/null; then
  echo "Error: flyctl not found. Please install Fly.io CLI first."
  exit 1
fi

# Check if user is logged into fly
if ! flyctl auth whoami &>/dev/null; then
  echo "Error: Not logged into Fly.io. Please run 'fly auth login' first."
  exit 1
fi

echo "Syncing secrets to Fly.io..."

# Read .env file and set each non-empty, non-comment line as a secret
while IFS= read -r line || [ -n "$line" ]; do
  # Skip empty lines and comments
  if [[ -n "$line" && ! "$line" =~ ^[[:space:]]*# ]]; then
    # Split the line into key and value at the first '=' sign
    key=$(echo "$line" | cut -d'=' -f1)
    value=$(echo "$line" | cut -d'=' -f2-)

    # Trim leading/trailing whitespace from key and value (optional but good practice)
    key=$(echo "$key" | awk '{$1=$1};1')
    value=$(echo "$value" | awk '{$1=$1};1')

    # Trim potential surrounding quotes from the value ONLY if they are the very first and last characters
    value=$(echo "$value" | sed -E "s/^(['\"])//" | sed -E "s/(['\"])$//")

    echo "Setting secret: $key"
    # Set the secret using the extracted key and value
    # Pass the value in a way that preserves quotes if needed by flyctl
    if ! flyctl secrets set "$key=$value" --stage &>/dev/null; then
      echo "Error setting secret: $key"
      # exit 1 # Continue trying other secrets even if one fails
    fi
  fi
done <.env

echo "Deploying staged secrets..."
if ! flyctl secrets deploy &>/dev/null; then
  echo "Error deploying secrets."
  exit 1
fi

echo "Successfully synced secrets to Fly.io"
