#!/bin/bash

# Hermes Quick Start Script
# Use this to quickly start Hermes with common configurations

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╦ ╦╔═╗╦═╗╔╦╗╔═╗╔═╗  ╦  ╦╦ ╦"
echo "╠═╣║╣ ╠╦╝║║║║╣ ╚═╗  ╚╗╔╝╚═╣"
echo "╩ ╩╚═╝╩╚═╩ ╩╚═╝╚═╝   ╚╝  ╩"
echo -e "${NC}"
echo "Autonomous Faucet Bot - V4.0"
echo ""

# Check if venv exists
if [ -d "venv" ]; then
    echo -e "${GREEN}✅ Virtual environment found${NC}"
    source venv/bin/activate
else
    echo -e "${YELLOW}⚠️ No virtual environment found${NC}"
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo -e "${GREEN}✅ Virtual environment created${NC}"
    
    echo "Installing dependencies..."
    pip install -r faucet_bot/requirements.txt
    playwright install chromium
    echo -e "${GREEN}✅ Dependencies installed${NC}"
fi

# Check if config exists
if [ ! -f "faucet_bot/config.json" ]; then
    echo -e "${YELLOW}⚠️ No configuration found${NC}"
    echo "The wizard will guide you through setup on first run."
fi

# Check if proxies exist
if [ ! -f "faucet_bot/proxies.txt" ] || [ ! -s "faucet_bot/proxies.txt" ]; then
    echo -e "${RED}❌ No proxies configured!${NC}"
    echo "Please add proxies to: faucet_bot/proxies.txt"
    echo "Format: ip:port or user:pass@ip:port (one per line)"
    echo ""
    read -p "Press ENTER to continue anyway or Ctrl+C to exit..."
fi

# Create necessary directories
mkdir -p data logs faucet_bot/sessions

echo ""
echo -e "${GREEN}🚀 Starting Hermes...${NC}"
echo ""

# Run Hermes
python3 hermes.py
