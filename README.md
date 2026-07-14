# Cazador de Contraseñas

Implementación individual para la Fase 5 del curso Programación (213023), UNAD.

El juego permite generar contraseñas aleatorias y abrir cofres de acuerdo con la validez de cada ronda. Fue construido con Python y programación orientada a objetos.

## Requisitos que cubre

- Longitud definida por el usuario, con mínimo de 8 caracteres.
- Al menos una letra mayúscula, una minúscula, un número y un carácter especial permitido.
- Ausencia de caracteres repetidos.
- Cofres común, raro, legendario y maldito, con puntajes distintos.
- Varias rondas de juego y puntaje acumulado.
- Excepciones personalizadas para datos no numéricos, longitudes inválidas y contraseñas incorrectas.
- Interfaz gráfica única para abrir cofres, consultar el resultado y finalizar la sesión.
- Herencia y polimorfismo mediante los cofres especializado: común, raro, legendario y maldito.

## Ejecución

```powershell
py cazador_contrasenas.py
```

Al ejecutar el archivo se abre directamente la interfaz gráfica. El usuario indica la longitud, abre tantas rondas como necesite y puede finalizar mediante el botón `Salir del juego`.

## Pruebas

```powershell
py -m unittest discover -s tests -v
```

Las pruebas verifican las reglas de contraseña, las excepciones, los puntajes, las rondas acumuladas y la jerarquía de cofres.

## Estructura orientada a objetos

- `Contrasena`: genera y valida contraseñas.
- `Cofre`: clase base de los resultados posibles de una ronda.
- `CofreComun`, `CofreRaro`, `CofreLegendario` y `CofreMaldito`: especializan el comportamiento de cada cofre.
- `JuegoCazador`: administra rondas, puntaje y manejo controlado de errores.
- `InterfazCazador`: presenta la interacción gráfica del jugador.

## Nota académica

Este repositorio muestra el código fuente del proyecto. La evidencia formal de ejecución y la explicación del código se presentan en el video asociado a la entrega Moodle.
