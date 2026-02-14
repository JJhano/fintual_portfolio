# Portfolio Rebalancer

Sistema de rebalanceo de portafolios de inversión.
Version de Python utilizada = 3.12.9
chat IA: 
https://gemini.google.com/share/2e08bec82cca

## Estructura

- `stock.py` - Clase de una accion con validaciones
- `portfolio.py` - Portafolio con  holdings, allocations, rebalanceo
- `rebalance.py` - Clase que representa acciones de rebalanceo
- `portfolio_reporter.py` - Clase para generar un reporte del portafolio
- `test_portfolio.py` — Test unitarios para clase stock y portafolio, considerando bordes

## Ejecucion

python main.py

## Tests

python test_portfolio.py 


## Decisiones 

Cada archivo representa una clase con un proposito unico. 
Se utilizan enums para evitar errores al escribir codigo, si fueran strings podria tomar cualquier valor. Se utiliza el decorador property para encapsular clases. Se realizan validaciones defensivas en el codigo.
