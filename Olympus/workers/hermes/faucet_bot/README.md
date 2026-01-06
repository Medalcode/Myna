# Faucet Automation Bot

This bot automates faucet claims using Playwright with proxy rotation and stealth techniques to avoid detection.

## Setup

1.  **Install Dependencies**:
    Dependencies are already installed in the virtual environment `venv`.
    If you need to reinstall:

    ```bash
    source venv/bin/activate
    pip install -r requirements.txt
    playwright install chromium
    ```

2.  **Configure Proxies**:
    Edit the `proxies.txt` file and add your proxies, one per line.
    Supported formats:

    - `http://user:pass@ip:port`
    - `http://ip:port`
    - `socks5://user:pass@ip:port`

3.  **Run the Bot**:
    ```bash
    source venv/bin/activate
    python main.py
    ```

## Features

- **Proxy Rotation**: Cycles through the list of proxies for each session.
- **Stealth Mode**: Uses `playwright-stealth` to mask automation traces.
- **Human Behavior**: Simulates random mouse movements and scrolling.
- **Random Timing**: Includes random delays between actions and cycles.
