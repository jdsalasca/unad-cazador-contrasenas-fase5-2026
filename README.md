# Cazador de Contraseñas

Implementación individual para la Fase 5 del curso Programación (213023), UNAD.

El juego permite generar contraseñas aleatorias y abrir cofres de acuerdo con la validez de cada ronda. Fue construido con Python y programación orientada a objetos.

## Requisitos que cubre

- Longitud definida por el usuario, con mínimo de 8 caracteres.
- Al menos una letra mayúscula, una minúscula, un número y un carácter especial permitido.
- Ausencia de caracteres repetidos.
- Cofres común, raro, legendario y maldito, con puntajes distintos.
- Varias rondas de juego y puntaje acumulado.
- Excepciones personalizadas para datos no numéricos y longitudes inválidas.

## Ejecución

```powershell
python cazador_contrasenas.py
```

Al iniciar, puede elegirse una demostración automatizada con casos válidos e inválidos, o jugar manualmente indicando la longitud de cada contraseña.

## Estructura orientada a objetos

- `Contrasena`: genera y valida contraseñas.
- `Cofre`: representa los resultados posibles de una ronda.
- `JuegoCazador`: administra rondas, puntaje y manejo controlado de errores.

## Nota académica

Este repositorio muestra el código fuente del proyecto. La evidencia formal de ejecución y la explicación del código se presentan en el video asociado a la entrega Moodle.
