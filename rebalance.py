from dataclasses import dataclass
from enum import Enum

# Se define un ENUM, ya que si dejaramos la accion como un string, podria generar errores, ya que no se validaria la accion,
# podria tomar todos los valores posibles de un string, con el enum solo puede tomar los valores de ahi.
class Action(str, Enum):
    BUY = 'BUY'
    SELL = 'SELL'

@dataclass
class Rebalance:
    """ La clase rebalance, almacena la informacion de un rebalance, tiene un nombre, accion, cantidad de acciones y valor"""

    name: str #nombre
    action: Action #Accion a realizar, BUY o SELL
    shares: float # cantidad de acciones a comprar o vender.
    value: float  

    def __str__(self) -> str:
        return f"{self.action.value} {self.shares:.4f} shares of {self.name} (${self.value:,.2f})"