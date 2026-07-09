"""
Curso: Programacion 213023 - Fase 5
Estudiante: Juan David Salas Camargo
Grupo: 213023_23

Juego: Cazador de Contrasenas

El programa genera contrasenas aleatorias, valida requisitos de seguridad
y asigna cofres con puntaje segun el resultado de cada ronda.
"""

from __future__ import annotations

import random
import string
from dataclasses import dataclass


class ErrorJuego(Exception):
    """Clase base para errores controlados del juego."""


class LongitudInvalidaError(ErrorJuego):
    """Se lanza cuando la longitud no cumple las reglas del juego."""


class DatoNoNumericoError(ErrorJuego):
    """Se lanza cuando el usuario no digita un numero valido."""


class ContrasenaIncorrectaError(ErrorJuego):
    """Se lanza cuando una contrasena generada no supera la validacion."""


class Contrasena:
    """Genera y valida contrasenas aleatorias sin caracteres repetidos."""

    MAYUSCULAS = string.ascii_uppercase
    MINUSCULAS = string.ascii_lowercase
    NUMEROS = string.digits
    ESPECIALES = "¿¡?=)(/¨*+-%&$#!."
    MINIMA_LONGITUD = 8

    def __init__(self, longitud: int) -> None:
        self.longitud = longitud
        self._validar_longitud()

    @classmethod
    def desde_texto(cls, texto: str) -> "Contrasena":
        """Construye una contrasena a partir de la entrada del usuario."""
        try:
            longitud = int(texto)
        except ValueError as exc:
            raise DatoNoNumericoError("La longitud debe ser un numero entero.") from exc
        return cls(longitud)

    @property
    def caracteres_disponibles(self) -> str:
        return self.MAYUSCULAS + self.MINUSCULAS + self.NUMEROS + self.ESPECIALES

    @property
    def caracteres_unicos(self) -> list[str]:
        return list(dict.fromkeys(self.caracteres_disponibles))

    def _validar_longitud(self) -> None:
        if self.longitud < self.MINIMA_LONGITUD:
            raise LongitudInvalidaError(
                f"La longitud minima permitida es {self.MINIMA_LONGITUD} caracteres."
            )
        if self.longitud > len(self.caracteres_unicos):
            raise LongitudInvalidaError(
                "La longitud supera la cantidad de caracteres unicos disponibles."
            )

    def generar(self) -> str:
        """Genera una contrasena aleatoria valida sin repetir caracteres."""
        obligatorios = [
            random.choice(self.MAYUSCULAS),
            random.choice(self.MINUSCULAS),
            random.choice(self.NUMEROS),
            random.choice(self.ESPECIALES),
        ]
        disponibles = [char for char in self.caracteres_unicos if char not in obligatorios]
        faltantes = self.longitud - len(obligatorios)
        seleccion = obligatorios + random.sample(disponibles, faltantes)
        random.shuffle(seleccion)
        return "".join(seleccion)

    def validar(self, valor: str) -> None:
        """Valida todas las condiciones obligatorias de la guia."""
        errores: list[str] = []

        if len(valor) < self.MINIMA_LONGITUD:
            errores.append("no cumple la longitud minima")
        if not any(char in self.MAYUSCULAS for char in valor):
            errores.append("no contiene letra mayuscula")
        if not any(char in self.MINUSCULAS for char in valor):
            errores.append("no contiene letra minuscula")
        if not any(char in self.NUMEROS for char in valor):
            errores.append("no contiene numero")
        if not any(char in self.ESPECIALES for char in valor):
            errores.append("no contiene caracter especial permitido")
        if len(set(valor)) != len(valor):
            errores.append("tiene caracteres repetidos")

        if errores:
            detalle = "; ".join(errores)
            raise ContrasenaIncorrectaError(f"Contrasena invalida: {detalle}.")


@dataclass(frozen=True)
class Cofre:
    """Representa el resultado de una ronda del juego."""

    nombre: str
    puntos: int
    descripcion: str

    @classmethod
    def aleatorio_valido(cls) -> "Cofre":
        cofres = [
            cls("Comun", 10, "Cofre basico abierto correctamente."),
            cls("Raro", 25, "Cofre con recompensa superior."),
            cls("Legendario", 50, "Cofre especial con maxima recompensa."),
        ]
        return random.choice(cofres)

    @classmethod
    def maldito(cls) -> "Cofre":
        return cls("Maldito", -20, "La contrasena fallo y activo una penalizacion.")


class JuegoCazador:
    """Controla el flujo, el puntaje y las rondas del juego."""

    def __init__(self) -> None:
        self.puntaje = 0
        self.rondas = 0

    def jugar_ronda(self, texto_longitud: str) -> dict[str, object]:
        self.rondas += 1
        try:
            generador = Contrasena.desde_texto(texto_longitud)
            candidata = generador.generar()
            generador.validar(candidata)
            cofre = Cofre.aleatorio_valido()
            estado = "valida"
            mensaje = "La contrasena cumple todos los requisitos."
        except ErrorJuego as exc:
            candidata = "No generada" if not isinstance(exc, ContrasenaIncorrectaError) else candidata
            cofre = Cofre.maldito()
            estado = "invalida"
            mensaje = str(exc)

        self.puntaje += cofre.puntos
        return {
            "ronda": self.rondas,
            "contrasena": candidata,
            "estado": estado,
            "cofre": cofre.nombre,
            "puntos_ronda": cofre.puntos,
            "puntaje_total": self.puntaje,
            "mensaje": mensaje,
        }

    @staticmethod
    def mostrar_resultado(resultado: dict[str, object]) -> None:
        print(f"Ronda: {resultado['ronda']}")
        print(f"Contrasena generada: {resultado['contrasena']}")
        print(f"Estado: {resultado['estado']}")
        print(f"Cofre obtenido: {resultado['cofre']}")
        print(f"Puntos de la ronda: {resultado['puntos_ronda']}")
        print(f"Puntaje acumulado: {resultado['puntaje_total']}")
        print(f"Detalle: {resultado['mensaje']}")
        print("-" * 50)

    def iniciar(self) -> None:
        print("=== Cazador de Contrasenas ===")
        print("Genere contrasenas aleatorias para abrir cofres y acumular puntos.")
        print("Digite 'salir' para terminar el juego.\n")

        while True:
            entrada = input("Longitud de la contrasena (minimo 8): ").strip()
            if entrada.lower() == "salir":
                print(f"Juego finalizado. Puntaje final: {self.puntaje}")
                break
            resultado = self.jugar_ronda(entrada)
            self.mostrar_resultado(resultado)


def demo_controlada() -> None:
    """Ejecuta rondas fijas para evidencia sin interaccion manual."""
    random.seed(2026)
    juego = JuegoCazador()
    for entrada in ["abc", "5", "8", "12", "10"]:
        resultado = juego.jugar_ronda(entrada)
        juego.mostrar_resultado(resultado)


if __name__ == "__main__":
    iniciar_demo = input("¿Desea ejecutar demo automatica? (s/n): ").strip().lower()
    if iniciar_demo == "s":
        demo_controlada()
    else:
        JuegoCazador().iniciar()
