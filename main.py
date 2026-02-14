from portafolio_reporter import PortfolioReporter
from portfolio import Portfolio
from stock import Stock


if __name__ == "__main__":
    print("=" * 70)
    print("SISTEMA DE REBALANCEO DE PORTAFOLIO")
    print("=" * 70)

    # 1. Crear acciones con precios actuales
    print("\n1. Creando acciones...")
    meta = Stock("META", 520.50)
    aapl = Stock("AAPL", 185.25)
    print(f"   {meta}")
    print(f"   {aapl}")

    # 2. Crear portafolio y agregar acciones
    print("\n2. Creando portafolio...")
    portfolio = Portfolio("PORTAFOLIO DE JHANO - Mi sueño")
    portfolio.add_stock(meta)
    portfolio.add_stock(aapl)

    # 3. Establecer holdings actuales (lo que tenemos ahora)
    print("\n3. Estableciendo holdings actuales...")
    portfolio.set_holdings("META", 10.0)   # 10 acciones de META
    portfolio.set_holdings("AAPL", 30.0)   # 30 acciones de AAPL
    print("   META: 10 acciones")
    print("   AAPL: 30 acciones")

    # 4. Establecer distribucion objetivo
    print("\n4. Estableciendo distribucion objetivo...")
    portfolio.set_target_allocation({
            "META": 0.40,  # 40% del portafolio
            "AAPL": 0.60   # 60% del portafolio
    })
    print("   META: 40%")
    print("   AAPL: 60%")

    # 5. Mostrar estado actual
    reporter = PortfolioReporter(portfolio)
    print(reporter.generate_report())
    print()

    # 6. Calcular rebalanceo necesario
    print("\n6. Calculando acciones de rebalanceo...")
    print("   (Con tolerancia de 1%)\n")

    rebalance_actions = portfolio.rebalance(tolerance=0.01)

    if not rebalance_actions:
            print(" El portafolio ya está balanceado!")
    else:
            print(f"  Se requieren {len(rebalance_actions)} acciones:\n")
            for i, action in enumerate(rebalance_actions, 1):
                    print(f"   {i}. {action}")

    # 7. Ejemplo adicional: Cambio de precios
    print("\n" + "=" * 70)
    print("ESCENARIO 2: Cambio en precios de mercado")
    print("=" * 70)

    print("\n7. Actualizando precios...")
    meta.update_price(550.00)  # META sube
    aapl.update_price(180.00)  # AAPL baja
    print(f"   {meta}")
    print(f"   {aapl}")

    reporter = PortfolioReporter(portfolio)
    print(reporter.generate_report())

    print("\n8. Recalculando rebalanceo con nuevos precios...\n")
    rebalance_actions = portfolio.rebalance(tolerance=0.01)
    if not rebalance_actions:
        print("   El portafolio está balanceado!")
    else:
        print(f"   Se requieren {len(rebalance_actions)} acciones:\n")
        for i, action in enumerate(rebalance_actions, 1):
            print(f"   {i}. {action}")
    print("\n" + "=" * 70)
    print("FIN DE LA DEMO")
    print("=" * 70)