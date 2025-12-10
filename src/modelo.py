
import joblib
from sklearn.linear_model import LinearRegression

# ... resto de las funciones ...
def entrenar_modelo(X, y):
    modelo = LinearRegression()
    modelo.fit(X, y)
    return modelo

def predecir(modelo, X):
    return modelo.predict(X)

def guardar_modelo(modelo, ruta):
    joblib.dump(modelo, ruta)

def cargar_modelo(ruta):
    return joblib.load(ruta)
