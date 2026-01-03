from abc import ABC, abstractmethod

class BaseRecipe(ABC):
    """
    Clase base para todas las recetas de Faucets.
    Define la estructura que deben seguir los scripts de automatización.
    """
    
    @property
    @abstractmethod
    def name(self):
        """Nombre identificativo de la receta (ej: 'FreeBitcoin')"""
        pass
    
    @property
    @abstractmethod
    def start_url(self):
        """URL inicial para comenzar la automatización"""
        pass

    @abstractmethod
    def run(self, page, logger):
        """
        Lógica principal de la automatización.
        :param page: Objeto Page de Playwright
        :param logger: Función para registrar eventos (print o logging)
        """
        pass
