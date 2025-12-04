import unittest
import numpy as np
import os
from modelolienal import LinearRegression, joblib  # Ajusta imports según tu archivo

class TestModeloLineal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Datos de prueba simples
        cls.X = np.array([[1], [2], [3], [4], [5]])
        cls.y = np.array([2, 4, 6, 8, 10])

        # Crear y entrenar el modelo
        cls.modelo = LinearRegression()
        cls.modelo.fit(cls.X, cls.y)

        # Archivo temporal para pruebas de persistencia
        cls.archivo_prueba = "test_modelo.joblib"

    def test_prediccion(self):
        """Verifica que la predicción sea correcta"""
        pred = self.modelo.predict(np.array([[6]]))
        self.assertAlmostEqual(pred[0], 12, places=5)

    def test_guardar_cargar(self):
        """Verifica que el modelo se pueda guardar y cargar correctamente"""
        # Guardar modelo
        joblib.dump(self.modelo, self.archivo_prueba)
        self.assertTrue(os.path.exists(self.archivo_prueba))

        # Cargar modelo
        modelo_cargado = joblib.load(self.archivo_prueba)
        pred_cargado = modelo_cargado.predict(np.array([[6]]))
        self.assertAlmostEqual(pred_cargado[0], 12, places=5)

    @classmethod
    def tearDownClass(cls):
        # Limpiar archivo de prueba
        if os.path.exists(cls.archivo_prueba):
            os.remove(cls.archivo_prueba)

if __name__ == "__main__":
    unittest.main()
