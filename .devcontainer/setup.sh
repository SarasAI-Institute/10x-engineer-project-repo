#!/bin/bash
set -euo pipefail

echo "Starting secure environment setup (Generating config.yaml)..."

CONFIG_DIR="$HOME/.continue"
CONFIG_FILE="$CONFIG_DIR/config.yaml"
API_KEY="sk-helicone-2v7akjq-m2xueay-ttt23kq-hx57ubq"

echo "Ensuring Node.js and npm are available..."
if ! command -v node >/dev/null 2>&1; then
    echo "Node.js not detected. Installing Node.js 20.x via NodeSource..."
    if ! command -v curl >/dev/null 2>&1; then
        sudo apt-get update
        sudo apt-get install -y curl
    fi
    curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
    sudo apt-get install -y nodejs
else
    echo "Node.js already installed at $(command -v node)"
fi

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

GIT_EMAIL=$(git config user.email)
echo "Extracting username from $GIT_EMAIL..."

if [[ "$GIT_EMAIL" == *users.noreply.github.com ]]; then
    EMAIL_PREFIX=$(echo "$GIT_EMAIL" | sed 's/@.*//')
    FINAL_USERNAME=$(echo "$EMAIL_PREFIX" | sed -E 's/^[0-9]+\+//')
    if [ -z "$FINAL_USERNAME" ]; then
        FINAL_USERNAME=$(git config github.user)
    fi
else
    FINAL_USERNAME=$(echo "$GIT_EMAIL" | sed 's/@.*//')
fi

echo "Writing configuration file to $CONFIG_FILE..."
mkdir -p "$CONFIG_DIR" || true

cat > "$CONFIG_FILE" <<- EOF
name: Local Config
version: 1.0.0
schema: v1
models:
  - name: OpenAI-via-Helicone-Proxy
    provider: openai
    model: gpt-4o
    apiBase: https://ai-gateway.helicone.ai/v1
    apiKey: '$API_KEY'
roles:
  - chat
  - edit
  - apply
requestOptions:
  headers:
    Helicone-User-Id: "$FINAL_USERNAME"
EOF

if [ -f "$CONFIG_FILE" ]; then
    echo "Configuration file successfully written and ready for Continue AI."
else
    echo "FATAL ERROR: Failed to write configuration file."
fi

echo ""
echo "✅ Setup complete! Run: python main.py"
echo "Please Reload Window to load the Continue AI configuration."
