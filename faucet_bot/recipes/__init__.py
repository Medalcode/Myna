from .sannysoft_recipe import SannySoftRecipe
from .example_faucet import ExampleFaucetRecipe
from .freebitcoin import FreeBitcoinRecipe
from .cointiply import CointiplyRecipe

# Lista oficial de recetas activas
# Comenta las que no quieras usar
ACTIVE_RECIPES = [
    # SannySoftRecipe(), 
    # FreeBitcoinRecipe(), 
    CointiplyRecipe(), # ¡Nuevo Objetivo!
]
