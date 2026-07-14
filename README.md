# Cazador de Contraseñas

Implementacion individual para la Fase 5 del curso Programacion (213023), UNAD.

El juego genera contrasenas aleatorias y abre cofres segun la validez de cada
ronda. Fue construido con Python, programacion orientada a objetos y una
arquitectura MVC sencilla, adecuada para mantener separadas las reglas del
juego, la interfaz y el flujo de interaccion.

## Requisitos que cubre

- Longitud definida por el usuario, con minimo de 8 caracteres.
- Al menos una letra mayuscula, una minuscula, un numero y un caracter especial permitido.
- Ausencia de caracteres repetidos.
- Cofres comun, raro, legendario y maldito, con puntajes distintos.
- Varias rondas de juego y puntaje acumulado.
- Excepciones personalizadas para datos no numericos, longitudes invalidas y contrasenas incorrectas.
- Interfaz grafica unica para abrir cofres, consultar el resultado y finalizar la sesion.
- Herencia y polimorfismo mediante los cofres especializado: comun, raro, legendario y maldito.

## Ejecución

```powershell
py cazador_contrasenas.py
```

Al ejecutar el archivo se abre directamente la interfaz grafica. El usuario solo
indica la longitud que desea generar; el programa crea y valida la contrasena
aleatoria. Luego puede abrir tantas rondas como necesite y finalizar mediante el
boton `Salir del juego`.

## Pruebas

```powershell
py -m unittest discover -s tests -v
```

Las pruebas verifican las reglas de contrasena, las excepciones, los puntajes,
las rondas acumuladas, la jerarquia de cofres y la coordinacion entre
controlador, modelo y vista mediante un doble de prueba.

## Arquitectura MVC y POO

- **Modelo:** `Contrasena`, `Cofre`, `CofreComun`, `CofreRaro`,
  `CofreLegendario`, `CofreMaldito`, `FabricaCofres`, `ResultadoRonda` y
  `JuegoCazador`. Esta capa contiene las reglas, las excepciones, la
  aleatoriedad inyectable y el puntaje acumulado.
- **Vista:** `VistaCazador`. Construye la interfaz Tkinter y solo presenta datos
  o recibe la longitud solicitada por el jugador.
- **Controlador:** `ControladorCazador`. Coordina las acciones de la vista con
  el modelo; no conoce reglas de contrasenas ni calcula puntajes.

El codigo incluye docstrings en clases y metodos publicos para facilitar la
lectura durante la sustentacion. `FabricaCofres` concentra la creacion de los
cofres y evita que el controlador dependa de sus implementaciones concretas.

## Nota académica

Este repositorio muestra el código fuente del proyecto. La evidencia formal de ejecución y la explicación del código se presentan en el video asociado a la entrega Moodle.
