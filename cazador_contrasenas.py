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
import tkinter as tk
from tkinter import ttk


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
    """Clase base para los cofres del juego."""

    nombre: str
    puntos: int
    descripcion: str

    def mensaje_apertura(self) -> str:
        """Entrega una descripcion polimorfica del resultado del cofre."""
        return self.descripcion

    @classmethod
    def aleatorio_valido(cls) -> "Cofre":
        cofres: list[Cofre] = [CofreComun(), CofreRaro(), CofreLegendario()]
        return random.choice(cofres)

    @classmethod
    def maldito(cls) -> "Cofre":
        return CofreMaldito()


class CofreComun(Cofre):
    """Cofre basico que aplica una recompensa de diez puntos."""

    def __init__(self) -> None:
        super().__init__("Comun", 10, "Cofre basico abierto correctamente.")

    def mensaje_apertura(self) -> str:
        return "Abriste un cofre comun y obtuviste una recompensa basica."


class CofreRaro(Cofre):
    """Cofre con una recompensa superior."""

    def __init__(self) -> None:
        super().__init__("Raro", 25, "Cofre con recompensa superior.")

    def mensaje_apertura(self) -> str:
        return "Abriste un cofre raro y mejoraste tu puntaje."


class CofreLegendario(Cofre):
    """Cofre con la recompensa valida mas alta."""

    def __init__(self) -> None:
        super().__init__("Legendario", 50, "Cofre especial con maxima recompensa.")

    def mensaje_apertura(self) -> str:
        return "Abriste un cofre legendario y recibiste la maxima recompensa."


class CofreMaldito(Cofre):
    """Cofre que aplica la penalizacion solicitada por la guia."""

    def __init__(self) -> None:
        super().__init__("Maldito", -20, "La contrasena fallo y activo una penalizacion.")

    def mensaje_apertura(self) -> str:
        return "Se activo un cofre maldito por una entrada invalida."


class JuegoCazador:
    """Controla el flujo, el puntaje y las rondas del juego."""

    def __init__(self) -> None:
        self.puntaje = 0
        self.rondas = 0

    def jugar_ronda(self, texto_longitud: str) -> dict[str, object]:
        self.rondas += 1
        candidata = "No generada"
        try:
            generador = Contrasena.desde_texto(texto_longitud)
            candidata = generador.generar()
            generador.validar(candidata)
            cofre = Cofre.aleatorio_valido()
            estado = "valida"
            mensaje = cofre.mensaje_apertura()
        except ErrorJuego as exc:
            cofre = Cofre.maldito()
            estado = "invalida"
            mensaje = f"{cofre.mensaje_apertura()} {exc}"

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

class InterfazCazador:
    """Interfaz grafica para jugar sin reemplazar la logica del dominio."""

    def __init__(self, raiz: tk.Tk) -> None:
        self.raiz = raiz
        self.juego = JuegoCazador()
        self.longitud = tk.StringVar(value="8")
        self.resultado = tk.StringVar(
            value="Elija una longitud y abra su primer cofre."
        )
        self.puntaje = tk.StringVar(value="Puntaje acumulado: 0")
        self._crear_componentes()

    def _crear_componentes(self) -> None:
        self.raiz.title("Cazador de Contrasenas")
        self.raiz.geometry("620x440")
        self.raiz.minsize(560, 400)
        self.raiz.configure(padx=24, pady=24)
        self.raiz.columnconfigure(0, weight=1)

        ttk.Label(
            self.raiz,
            text="Cazador de Contrasenas",
            font=("Arial", 18, "bold"),
        ).grid(row=0, column=0, columnspan=3, sticky="w")
        ttk.Label(
            self.raiz,
            text=(
                "Genere una contrasena valida para abrir cofres y acumular puntos."
            ),
            wraplength=540,
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(8, 22))

        ttk.Label(self.raiz, text="Longitud (minimo 8):").grid(
            row=2, column=0, sticky="w"
        )
        entrada = ttk.Entry(self.raiz, textvariable=self.longitud, width=12)
        entrada.grid(row=2, column=1, sticky="w", padx=(12, 12))
        entrada.focus()
        entrada.bind("<Return>", self.abrir_cofre)
        ttk.Button(self.raiz, text="Abrir cofre", command=self.abrir_cofre).grid(
            row=2, column=2, sticky="w"
        )

        ttk.Separator(self.raiz, orient="horizontal").grid(
            row=3, column=0, columnspan=3, sticky="ew", pady=22
        )
        ttk.Label(self.raiz, textvariable=self.resultado, wraplength=540).grid(
            row=4, column=0, columnspan=3, sticky="w"
        )
        ttk.Label(
            self.raiz,
            textvariable=self.puntaje,
            font=("Arial", 11, "bold"),
        ).grid(row=5, column=0, columnspan=3, sticky="w", pady=(20, 8))
        ttk.Label(
            self.raiz,
            text=(
                "Reglas: mayuscula, minuscula, numero, caracter especial y sin repetir caracteres."
            ),
            wraplength=540,
        ).grid(row=6, column=0, columnspan=3, sticky="w")
        ttk.Button(self.raiz, text="Salir del juego", command=self.salir).grid(
            row=7, column=0, columnspan=3, sticky="e", pady=(24, 0)
        )

    def abrir_cofre(self, _evento: object | None = None) -> None:
        resultado = self.juego.jugar_ronda(self.longitud.get().strip())
        if resultado["estado"] == "valida":
            texto = (
                f"Ronda {resultado['ronda']}: contrasena {resultado['contrasena']}. "
                f"Cofre {resultado['cofre']} ({resultado['puntos_ronda']:+d} puntos). "
                "Puedes abrir otro cofre o salir del juego."
            )
        else:
            texto = (
                f"Ronda {resultado['ronda']}: cofre {resultado['cofre']} "
                f"({resultado['puntos_ronda']:+d} puntos). {resultado['mensaje']}"
            )
        self.resultado.set(texto)
        self.puntaje.set(f"Puntaje acumulado: {resultado['puntaje_total']}")

    def salir(self) -> None:
        """Cierra la sesion despues de que el jugador decide finalizar."""
        self.raiz.destroy()


def iniciar_interfaz_grafica() -> None:
    """Inicia la version visual solicitada para la socializacion del juego."""
    raiz = tk.Tk()
    InterfazCazador(raiz)
    raiz.mainloop()


if __name__ == "__main__":
    iniciar_interfaz_grafica()
