from rebalance import Action, Rebalance
from stock import Stock


class Portfolio:
    """ Clase portafolio, almacena la informacion de un portafolio, tiene un nombre y distintos activos, 
    tiene la capacidad de hace run rebalanceo, y actualizar los precios de los activos"""
    
    def __init__(self, name: str):
        self._name = name
        self._stocks : dict[str, Stock] = {} #Diccionario de acciones disponibles
        self._holdings : dict[str, float] = {} #Cantidad actual de acciones por nombre 
        self._target_allocation : dict[str, float] = {} #Distribucion objetivo -> Debe sumar 1

    @property
    def name(self) -> str:
        return self._name

    @property
    def stocks(self) -> dict[str, Stock]:
        return dict(self._stocks) 

    @property
    def holdings(self) -> dict[str, float]:
        return dict(self._holdings)

    @property
    def target_allocation(self) -> dict[str, float]:
        return dict(self._target_allocation)
        
    def add_stock(self, stock: Stock):
        """ Agrega una accion al portafolio
        """
        self._stocks[stock.name] = stock
        ## Al agregar al stock se incializa en 0
        if stock.name not in self._holdings:
            self._holdings[stock.name] = 0.0
        
    
    def set_holdings(self, stock_name: str, shares: float) -> None:
        ## Primero validacioes para evitar errores, como que la accion no exista o que la cantidad de acciones sea negativa
        if stock_name not in self._stocks:
            raise ValueError("La accion no existe en el portafolio")
        if shares < 0:
            raise ValueError("La cantidad de acciones no puede ser negativa")
        
        self._holdings[stock_name] = shares
    
    def set_target_allocation(self, allocations: dict[str, float]) -> None:
        # Primero validar que todas las acciones existan
        for stock_name in allocations:
            if stock_name not in self._stocks:
                raise ValueError(f"La accion {stock_name} no existe en el portafolio")

        # Validar que no haya valores negativos
        for stock_name, allocation in allocations.items():
            if allocation < 0:
                raise ValueError("La distribución objetivo no puede ser negativa")

        #  Validar que sume ~1
        total = sum(allocations.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError("La suma de las distribuciones debe ser igual a 1")

        # Finalmente se cambia el estado si todo es valido
        self._target_allocation = allocations.copy()
    
    def get_total_value(self) -> float: 
        """ Calcula el valor total del portafolio, multiplicando la cantidad de acciones por el precio actual de cada accion."""
        total = 0.0
        for stock_name, shares in self._holdings.items():
            if stock_name in self._stocks:
                total += shares * self._stocks[stock_name].price
        return total
    
    def get_current_allocation(self) -> dict[str, float]:
        """ Calcula la distribucion actual del portafolio"""
        total_value = self.get_total_value()
        if total_value == 0:
            return {stock_name: 0.0 for stock_name in self._holdings}
        
        current_allocation = {} 
        for stock_name in self._stocks:
            shares = self._holdings.get(stock_name, 0.0)
            value = shares * self._stocks[stock_name].price
            current_allocation[stock_name] = value / total_value
        return current_allocation
    
    def rebalance(self, tolerance: float = 0.01) -> list[Rebalance]:
        """ Calcula las operaciones necesarias para rebalancear el portafolio"""
        """ Priemro se debe calcular el valor total del portafolio.
        Luego para cada accion se debe determinar el valor objetivo, valor actual y la diferencia"""
        
        if not self._target_allocation:
            raise ValueError("No se ha establecido una distribucion objetivo para el portafolio")

        total_value = self.get_total_value()
        if total_value == 0:
            raise ValueError("El valor total del portafolio es 0, no se puede rebalancear")
        
        actions = []
        for stock_name, target_pct in self._target_allocation.items():
            # Valor objetivo para esta accion
            target_value = target_pct * total_value
            # valor actual para esta accion
            current_shares = self._holdings.get(stock_name, 0.0)
            current_price =  self._stocks[stock_name].price
            current_value =  current_shares * current_price
            # Calcula diferencia en valor
            value_diff = target_value - current_value
            
            # diferencia en porcentaje del portafolio total
            # para determinar si se hace el rebalanceo o no.
            porcentage_diff = abs(value_diff) / total_value
            
            # Solo ejecuta si la diferencia es mayor a la tolerancia
            if porcentage_diff > tolerance:
                if value_diff > 0:
                    # Se necesita comprar
                    shares_to_buy = value_diff / current_price
                    actions.append(Rebalance(name=stock_name, action=Action.BUY, shares=shares_to_buy, value=value_diff))
                else:
                    # Se necesita vender
                    shares_to_sell = -value_diff / current_price
                    actions.append(Rebalance(name=stock_name, action=Action.SELL, shares=shares_to_sell, value=-value_diff))
        return actions
