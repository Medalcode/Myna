
import sys
import os

print(f"Propósito: Diagnosticar error de importación.")
print(f"CWD: {os.getcwd()}")
print(f"Sys Path: {sys.path}")

try:
    import faucet_bot
    print("✅ 'import faucet_bot' exitoso")
except ImportError as e:
    print(f"❌ 'import faucet_bot' falló: {e}")

try:
    from faucet_bot.main import FaucetBot
    print("✅ 'from faucet_bot.main import FaucetBot' exitoso")
except ImportError as e:
    print(f"❌ 'from faucet_bot.main' falló: {e}")

try:
    sys.path.append(os.path.join(os.getcwd(), 'faucet_bot'))
    import main
    print("✅ 'import main' (con path modificado) exitoso")
except ImportError as e:
    print(f"❌ 'import main' falló: {e}")
