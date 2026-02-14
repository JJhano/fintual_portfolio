import unittest
from rebalance import Action, Rebalance 
from stock import Stock
from portfolio import Portfolio 

class TestStock(unittest.TestCase):
    """Test cases para la clase Stock"""

    def test_create_valid_stock(self):
        """Prueba la creación correcta de una accion"""
        s = Stock("AAPL", 150.0)
        self.assertEqual(s.name, "AAPL")
        self.assertEqual(s.price, 150.0)

    def test_create_negative_price_stock(self):
        """Caso de Borde: Precio negativo al inicio debe fallar"""
        with self.assertRaises(ValueError):
            Stock("BAD", -10.0)

    def test_update_price_valid(self):
        """Prueba la actualización de precio"""
        s = Stock("AAPL", 150.0)
        s.update_price(155.0)
        self.assertEqual(s.price, 155.0)

    def test_update_price_negative(self):
        """Caso de Borde: Actualizar a precio negativo debe fallar"""
        s = Stock("AAPL", 150.0)
        with self.assertRaises(ValueError):
            s.update_price(-5.0)
        # Aseguramos que el precio no cambió tras el error
        self.assertEqual(s.price, 150.0)


class TestPortfolio(unittest.TestCase):
    """Test cases para la clase Portfolio"""

    def setUp(self):
        """Se ejecuta antes de cada test. Prepara un entorno limpio."""
        self.p = Portfolio("Retirement Fund")
        self.s1 = Stock("AAPL", 100.0)
        self.s2 = Stock("GOOG", 200.0)
        self.p.add_stock(self.s1)
        self.p.add_stock(self.s2)

    def test_initial_state(self):
        """Verifica que el portafolio inicie vacío de holdings pero con stocks disponibles"""
        self.assertEqual(self.p.name, "Retirement Fund")
        self.assertEqual(self.p.holdings["AAPL"], 0.0)
        self.assertEqual(self.p.holdings["GOOG"], 0.0)

    # --- Tests de Holdings (Tenencias) ---

    def test_set_holdings_valid(self):
        self.p.set_holdings("AAPL", 10)
        self.assertEqual(self.p.holdings["AAPL"], 10)

    def test_set_holdings_invalid_stock(self):
        """Caso de Borde: Intentar setear holdings de una acción que no se ha agregado"""
        with self.assertRaises(ValueError):
            self.p.set_holdings("TSLA", 5) # TSLA no existe en el setup

    def test_set_holdings_negative(self):
        """Caso de Borde: Holdings negativos"""
        with self.assertRaises(ValueError):
            self.p.set_holdings("AAPL", -5)

    # --- Tests de Target Allocation (Distribución Objetivo) ---

    def test_set_target_allocation_valid(self):
        target = {"AAPL": 0.6, "GOOG": 0.4}
        self.p.set_target_allocation(target)
        self.assertEqual(self.p.target_allocation, target)

    def test_set_target_allocation_does_not_sum_one(self):
        """Caso de Borde: La suma no es 1 (ej: 0.8)"""
        target = {"AAPL": 0.4, "GOOG": 0.4} # Suma 0.8
        with self.assertRaisesRegex(ValueError, "La suma de las distribuciones debe ser igual a 1"):
            self.p.set_target_allocation(target)

    def test_set_target_allocation_unknown_stock(self):
        """Caso de Borde: Configurar target para stock inexistente"""
        target = {"AAPL": 0.5, "TSLA": 0.5} 
        with self.assertRaises(ValueError):
            self.p.set_target_allocation(target)

    def test_set_target_allocation_negative_percent(self):
        """Caso de Borde: Porcentaje negativo (aunque sume 1 matemáticamente)"""
        # AAPL: 1.2, GOOG: -0.2 -> Suma 1.0, pero es inválido por lógica de negocio
        target = {"AAPL": 1.2, "GOOG": -0.2}
        with self.assertRaises(ValueError):
            self.p.set_target_allocation(target)

    # --- Tests de Cálculos y Rebalanceo ---

    def test_get_total_value(self):
        self.p.set_holdings("AAPL", 10) # 10 * 100 = 1000
        self.p.set_holdings("GOOG", 5)  # 5 * 200 = 1000
        # Total esperado: 2000
        self.assertEqual(self.p.get_total_value(), 2000.0)

    def test_get_current_allocation_zero_value(self):
        """Caso de Borde: Portafolio vacío, evitar división por cero"""
        alloc = self.p.get_current_allocation()
        self.assertEqual(alloc["AAPL"], 0.0)
        self.assertEqual(alloc["GOOG"], 0.0)

    def test_rebalance_empty_target(self):
        """Caso de Borde: Intentar rebalancear sin haber definido objetivos"""
        with self.assertRaisesRegex(ValueError, "No se ha establecido una distribucion objetivo"):
            self.p.rebalance()

    def test_rebalance_zero_value(self):
        """Caso de Borde: Intentar rebalancear un portafolio sin dinero"""
        self.p.set_target_allocation({"AAPL": 0.5, "GOOG": 0.5})
        with self.assertRaisesRegex(ValueError, "El valor total del portafolio es 0"):
            self.p.rebalance()

    def test_rebalance_logic_buy_sell(self):
        """
        Prueba Integradora de lógica de rebalanceo:
        Escenario:
        - AAPL: Precio 100, Cantidad 10 -> Valor 1000
        - GOOG: Precio 200, Cantidad 15 -> Valor 3000
        - Valor Total: 4000
        
        Objetivo: 50% / 50%
        - Meta AAPL: 2000 (Faltan 1000 -> Comprar 10 acciones)
        - Meta GOOG: 2000 (Sobran 1000 -> Vender 5 acciones)
        """
        self.p.set_holdings("AAPL", 10)
        self.p.set_holdings("GOOG", 15)
        self.p.set_target_allocation({"AAPL": 0.5, "GOOG": 0.5})

        actions = self.p.rebalance()
        
        self.assertEqual(len(actions), 2)
        
        # Analizamos la primera acción (Puede variar el orden por ser dict, así que buscamos por nombre)
        action_aapl = next(a for a in actions if a.name == "AAPL")
        action_goog = next(a for a in actions if a.name == "GOOG")

        # Verificar AAPL (Compra)
        self.assertEqual(action_aapl.action, Action.BUY)
        self.assertEqual(action_aapl.shares, 10.0)
        self.assertEqual(action_aapl.value, 1000.0)

        # Verificar GOOG (Venta)
        self.assertEqual(action_goog.action, Action.SELL)
        self.assertEqual(action_goog.shares, 5.0)
        self.assertEqual(action_goog.value, 1000.0) # Tu código guarda el valor positivo en el objeto Rebalance aunque sea venta (abs)

    def test_rebalance_within_tolerance(self):
        """Caso de Borde: Desviación pequeña dentro de la tolerancia (no hacer nada)"""
        # Total 2000. Target 50/50.
        # AAPL: 1000 (50%)
        # GOOG: 1000 (50%)
        # Movemos el precio ligeramente para crear un desbalance menor al 1%
        self.p.set_holdings("AAPL", 10) # 1000
        self.p.set_holdings("GOOG", 5)  # 1000
        self.p.set_target_allocation({"AAPL": 0.5, "GOOG": 0.5})
        
        # Subimos AAPL un poquito: Precio 100 -> 100.5
        # Nuevo valor AAPL = 1005. Total = 2005.
        # Target AAPL = 1002.5. Diff = 2.5.
        # % Diff = 2.5 / 2005 = 0.0012 (0.12%) < 1% Tolerance
        self.s1.update_price(100.5) 
        
        actions = self.p.rebalance(tolerance=0.01)
        self.assertEqual(len(actions), 0, "No debería generar acciones si está dentro de la tolerancia")

def run_tests():
    """Ejecuta todos los tests y muestra resultados"""
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestStock))
    suite.addTests(loader.loadTestsFromTestCase(TestPortfolio))
    
    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "=" * 70)
    print("RESUMEN DE TESTS")
    print("=" * 70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallidos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    run_tests()