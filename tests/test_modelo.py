

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import numpy as np
from src.modelo import entrenar_modelo, guardar_modelo, cargar_modelo, predecir

class TestModelo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.X = np.array([[1], [2], [3], [4], [5]])
        cls.y = np.array([2, 4, 6, 8, 10])
        cls.modelo = entrenar_modelo(cls.X, cls.y)
        cls.archivo = "modelo_test.joblib"

    def test_prediccion(self):
        pred = predecir(self.modelo, np.array([[6]]))
        self.assertAlmostEqual(pred[0], 12, places=5)

    def test_guardado_y_carga(self):
        guardar_modelo(self.modelo, self.archivo)
        self.assertTrue(os.path.exists(self.archivo))

        modelo_cargado = cargar_modelo(self.archivo)
        pred = predecir(modelo_cargado, np.array([[6]]))
        self.assertAlmostEqual(pred[0], 12, places=5)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.archivo):
            os.remove(cls.archivo)

if __name__ == "__main__":
    unittest.main()