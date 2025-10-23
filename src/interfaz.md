#Documentación del prototipo  de Interfaz Gráfica en Python

-Objetivo:
Como desarrolladores, el objetivo fue investigar y seleccionar librerías adecuadas para crar interfaces gráficas(GUI) además de hacer una prueba mínima funcional para evaluar su viabilidad en proyectos futuros.

-Investigación de Librerías Gráficas:
Para analizarlas hemos tenido en cuenta los criterios expresos en el enunciado de la historia.
Algunas  de las librerías más utilizadas para crear GUIs son:
    -Tkinter: teniendo en cuenta la facilidad de uso, nos hemos basado en la instalación y configuración inicial, en este caso es fácil ya que la librería viene incluída con Python por lo que no requiere instalación ni configuración adicional; la cantidad de código necesario, Tkinter permite crear una ventana funcional con muy pocas líneas.
    
    Por otro lado, atendiendo a la curva de aprendizaje;ña cual se refiere al tiempo que tarda un desarrollador promedio en comprender cómo se crea una interfaz básica,Tkinter tiene una curva suave si conoces lo básico sobre Pyhton(funciones, variables, módulos).
    
    En cuanto a la compatibilidad, la librería es altamente compatible con Windows;funciona de manera nativa usando la librería instalada junto con Pyhton,macOS, Linux; disponible meidante el paquete python3-tk.

    La comunidad de soporte es amplia y activa participando en foros como Reddit o Discord, demás la documentación disponible oficial(presente en la guía oficial de Pyhton) o no oficial es excelente ya que ofrece información precisa y actualizada lo que facilita la resolución de dudas.
    Las funcionalidades y capacidades gráficas que ofrece Tkinter corresponden  con un conjunto completo de widgets y herramientas, es funcional, estable y extensible. Presenta canvas gráficos, gestores de diseño, cuadros de diálogo estándar como messagebox.
    Por último en cuanto al rendimiento y estabilidad  es adecuado presentando un enfoque más simple y fiable. Tiene un bajo consumo de recursos ya que no requiere frameworks pesados, no obstante presenta limitaciones y que no es adecuado para aplicaciones con gráficos intensivos o grandes volúmenes de datos.

    En comparación, otra librería como PyQt es más compleja de usar ya que requiere aprender conceptos como layouts, singals y slots, más adecuada para usuarios intermedios o avanzados, también requiere la instalación con pip install PyQt6 e inclute muchas dependencias. Además es multiplataforma como Tkinter pero tiene una mejor integración nativa y soporte profesional. Cuenta con una comunidad amplia y profesional, en relación a las capacidades gráficas y visuales son muy avnazadas , adminten temas , estilos modernos,tablas,gráficos menús dinámicos etc.
    Tiene  un rendimineto más pesado aunque optimizado para interfaces grandes.

    En conclusión para fines educativos y de prototipo rápido Tkinter es la mejor opción pese a presentar dificultades de diseño , menjo de eventos y limitaciones visuales.