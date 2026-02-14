from portfolio import Portfolio


class PortfolioReporter:
    """
    Clase encargada de generar representaciones legibles del estado de un portafolio.
    Separa la lógica de presentación de la lógica de negocio.
    """
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio

    def generate_report(self) -> str:
        """Genera un reporte completo en formato texto (tabla + rebalanceo)."""
        lines = []
        lines.append(f"REPORTE DE PORTAFOLIO: {self.portfolio.name.upper()}")
        lines.append("=" * 60)
        
        total_value = self.portfolio.get_total_value()
        lines.append(f"Valor Total: ${total_value:,.2f}")
        lines.append("-" * 60)
        
        # Encabezados de la tabla
        # Ticker | Precio | Cantidad | Valor Total | Actual % | Target %
        header = f"{'Ticker':<10} | {'Precio':>10} | {'Cant.':>8} | {'Valor':>12} | {'Actual %':>8} | {'Target %':>8}"
        lines.append(header)
        lines.append("-" * 60)

        # Obtener datos calculados
        current_allocations = self.portfolio.get_current_allocation()
        target_allocations = self.portfolio.target_allocation
        
        for stock_name, stock in self.portfolio.stocks.items():
            price = stock.price
            shares = self.portfolio.holdings.get(stock_name, 0.0)
            value = shares * price
            curr_pct = current_allocations.get(stock_name, 0.0)
            targ_pct = target_allocations.get(stock_name, 0.0)
            
            # Formateo de fila
            row = (f"{stock_name:<10} | "
                   f"${price:>9.2f} | "
                   f"{shares:>8.2f} | "
                   f"${value:>11.2f} | "
                   f"{curr_pct:>7.1%} | " # Formato porcentaje con 1 decimal
                   f"{targ_pct:>7.1%}")
            lines.append(row)
            
        lines.append("=" * 60)
        
        # Sección de Rebalanceo
        lines.append("SUGERENCIAS DE REBALANCEO:")
        try:
            # Usamos un try-except por si el portafolio está vacío o sin target
            rebalance_actions = self.portfolio.rebalance(tolerance=0.01)
            
            if not rebalance_actions:
                lines.append(" >> El portafolio está balanceado dentro de la tolerancia.")
            else:
                for action in rebalance_actions:
                    # Asumiendo que action tiene .action (Enum), .name, .shares, .value
                    tipo = "COMPRAR" if "BUY" in str(action.action) else "VENDER"
                    lines.append(f" >> {tipo} {action.shares:.2f} acciones de {action.name} "
                                 f"(Valor: ${abs(action.value):.2f})")
        except ValueError as e:
            lines.append(f" >> No se puede calcular rebalanceo: {e}")

        return "\n".join(lines)