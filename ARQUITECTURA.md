# Arquitectura del juego

## Patron aplicado

El proyecto usa el patron Modelo-Vista-Controlador (MVC) en un solo archivo
Python, porque la guia solicita entregar un archivo fuente funcional. Esta
organizacion mantiene las responsabilidades separadas sin fragmentar un
proyecto pequeno en modulos innecesarios.

## Responsabilidades

| Capa | Componentes | Responsabilidad |
|---|---|---|
| Modelo | `Contrasena`, `Cofre`, `FabricaCofres`, `ResultadoRonda`, `JuegoCazador` | Aplicar reglas de contrasena, resolver rondas, crear cofres y conservar el puntaje. |
| Vista | `VistaCazador` | Capturar la longitud, mostrar el resultado y administrar los controles de Tkinter. |
| Controlador | `ControladorCazador` | Atender eventos de la vista y delegar el procesamiento al modelo. |

## Flujo de una ronda

1. El jugador escribe solo la longitud deseada en la interfaz grafica.
2. `ControladorCazador` solicita ese dato a `VistaCazador`.
3. `JuegoCazador` crea una `Contrasena`, la genera aleatoriamente y la valida.
4. `FabricaCofres` entrega un cofre positivo o el cofre maldito cuando ocurre
   una excepcion de dominio.
5. El modelo devuelve un `ResultadoRonda` inmutable.
6. El controlador envía el resultado a la vista para actualizar la pantalla.

## Calidad y pruebas

Las excepciones de dominio permiten informar entradas no numericas, longitudes
invalidas y contrasenas que incumplen reglas. La aleatoriedad se inyecta en el
modelo, de modo que las pruebas son reproducibles. Las pruebas unitarias no
abren ventanas: usan una vista de prueba para comprobar que el controlador
coordina correctamente las capas.
