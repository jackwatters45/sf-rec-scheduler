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
    # Remove any surrounding quotes from the value
    line=$(echo "$line" | sed -E "s/['\"]//g")

    # Split the line into key and value
    key=$(echo "$line" | cut -d'=' -f1)
    value=$(echo "$line" | cut -d'=' -f2-)

    if ! flyctl secrets set "$key=$value" &>/dev/null; then
      echo "Error setting secret: $key"
      exit 1
    fi
  fi
done <.env

echo "Successfully synced secrets to Fly.io"
