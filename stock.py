class Stock:
    """ Clase stock, almacena la informacion de un activo, tiene un nombre y precio"""
    def __init__(self, name: str, price: float):
        # El precio de un stock no puede ser negativo, podria generar errores, por lo tanto hay que validarlo.

        if price < 0:
            raise ValueError("El precio de un stock no puede ser negativo")
        self._price = price
        self._name = name

    # Se crean propiedades para acceder al nombre y precio del stock  
    @property
    def name(self) -> str:
        return self._name

    @property
    def price(self) -> float:
        return self._price

    #Se crea un metodo para actualizar el precio, ya que si se usara la variable directamente,
    # podria no validar el nuevo precio, lo que podria generar errores en el futuro.
    def update_price(self, new_price: float) -> None:
        if new_price < 0:
            raise ValueError("El precio de un stock no puede ser negativo")
        self._price = new_price


    def __repr__(self) -> str:
        return f"Stock(name='{self._name}', price={self._price:.2f})"