"""Juego grafico Cazador de Contrasenas para la Fase 5 de Programacion.

La aplicacion usa una organizacion MVC dentro de un unico archivo fuente:
el modelo aplica reglas y puntajes, la vista presenta Tkinter y el
controlador conecta ambas capas sin mezclar sus responsabilidades.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
import random
import string
import tkinter as tk
from tkinter import ttk
from typing import Callable


class ErrorJuego(Exception):
    """Clase base para los errores de dominio del juego."""


class LongitudInvalidaError(ErrorJuego):
    """Se produce cuando la longitud no cumple el minimo permitido."""


class DatoNoNumericoError(ErrorJuego):
    """Se produce cuando la longitud no puede convertirse a un entero."""


class ContrasenaIncorrectaError(ErrorJuego):
    """Se produce cuando una contrasena no cumple las reglas de seguridad."""


class Contrasena:
    """Genera y valida contrasenas aleatorias sin caracteres repetidos."""

    MAYUSCULAS = string.ascii_uppercase
    MINUSCULAS = string.ascii_lowercase
    NUMEROS = string.digits
    ESPECIALES = "¿¡?=)(/¨*+-%&$#!."
    LONGITUD_MINIMA = 8

    def __init__(self, longitud: int) -> None:
        """Crea una solicitud de generacion y valida su longitud."""
        self.longitud = longitud
        self._validar_longitud()

    @classmethod
    def desde_longitud_texto(cls, texto_longitud: str) -> "Contrasena":
        """Convierte el dato de la interfaz en una solicitud valida."""
        try:
            longitud = int(texto_longitud)
        except ValueError as exc:
            raise DatoNoNumericoError(
                "La longitud debe ser un numero entero."
            ) from exc
        return cls(longitud)

    @property
    def caracteres_unicos(self) -> tuple[str, ...]:
        """Devuelve el alfabeto permitido sin duplicados."""
        caracteres = self.MAYUSCULAS + self.MINUSCULAS + self.NUMEROS + self.ESPECIALES
        return tuple(dict.fromkeys(caracteres))

    def generar(self, aleatorio: random.Random) -> str:
        """Genera una contrasena valida con orden aleatorio impredecible."""
        obligatorios = [
            aleatorio.choice(self.MAYUSCULAS),
            aleatorio.choice(self.MINUSCULAS),
            aleatorio.choice(self.NUMEROS),
            aleatorio.choice(self.ESPECIALES),
        ]
        disponibles = [
            caracter
            for caracter in self.caracteres_unicos
            if caracter not in obligatorios
        ]
        seleccion = obligatorios + aleatorio.sample(
            disponibles, self.longitud - len(obligatorios)
        )
        aleatorio.shuffle(seleccion)
        contrasena = "".join(seleccion)
        self.validar(contrasena)
        return contrasena

    def validar(self, valor: str) -> None:
        """Comprueba todas las condiciones solicitadas por la guia."""
        errores: list[str] = []

        if len(valor) != self.longitud:
            errores.append("no coincide con la longitud solicitada")
        if len(valor) < self.LONGITUD_MINIMA:
            errores.append("no cumple la longitud minima")
        if not any(caracter in self.MAYUSCULAS for caracter in valor):
            errores.append("no contiene una mayuscula")
        if not any(caracter in self.MINUSCULAS for caracter in valor):
            errores.append("no contiene una minuscula")
        if not any(caracter in self.NUMEROS for caracter in valor):
            errores.append("no contiene un numero")
        if not any(caracter in self.ESPECIALES for caracter in valor):
            errores.append("no contiene un caracter especial permitido")
        if len(set(valor)) != len(valor):
            errores.append("contiene caracteres repetidos")

        if errores:
            raise ContrasenaIncorrectaError(
                f"Contrasena invalida: {'; '.join(errores)}."
            )

    def _validar_longitud(self) -> None:
        """Verifica limites que dependen del alfabeto disponible."""
        if self.longitud < self.LONGITUD_MINIMA:
            raise LongitudInvalidaError(
                f"La longitud minima permitida es {self.LONGITUD_MINIMA}."
            )
        if self.longitud > len(self.caracteres_unicos):
            raise LongitudInvalidaError(
                "La longitud supera los caracteres unicos disponibles."
            )


@dataclass(frozen=True)
class Cofre(ABC):
    """Contrato comun para los cofres y sus efectos de puntaje."""

    nombre: str
    puntos: int

    @abstractmethod
    def mensaje_apertura(self) -> str:
        """Describe el efecto del cofre para presentarlo al jugador."""


class CofreComun(Cofre):
    """Cofre basico con recompensa de diez puntos."""

    def __init__(self) -> None:
        super().__init__("Comun", 10)

    def mensaje_apertura(self) -> str:
        """Devuelve el mensaje de una recompensa comun."""
        return "Abriste un cofre comun y recibiste una recompensa basica."


class CofreRaro(Cofre):
    """Cofre de recompensa intermedia."""

    def __init__(self) -> None:
        super().__init__("Raro", 25)

    def mensaje_apertura(self) -> str:
        """Devuelve el mensaje de una recompensa rara."""
        return "Abriste un cofre raro y mejoraste tu puntaje."


class CofreLegendario(Cofre):
    """Cofre de mayor recompensa valida."""

    def __init__(self) -> None:
        super().__init__("Legendario", 50)

    def mensaje_apertura(self) -> str:
        """Devuelve el mensaje de una recompensa legendaria."""
        return "Abriste un cofre legendario y obtuviste la maxima recompensa."


class CofreMaldito(Cofre):
    """Cofre de penalizacion para entradas o contrasenas invalidas."""

    def __init__(self) -> None:
        super().__init__("Maldito", -20)

    def mensaje_apertura(self) -> str:
        """Devuelve el mensaje de una penalizacion."""
        return "Se activo un cofre maldito por una entrada invalida."


class FabricaCofres:
    """Selecciona el cofre apropiado sin exponer la aleatoriedad al controlador."""

    def __init__(self, aleatorio: random.Random) -> None:
        """Recibe la fuente de aleatoriedad compartida por el modelo."""
        self._aleatorio = aleatorio

    def crear_cofre_valido(self) -> Cofre:
        """Crea un cofre positivo seleccionado al azar."""
        return self._aleatorio.choice(
            [CofreComun(), CofreRaro(), CofreLegendario()]
        )

    def crear_cofre_maldito(self) -> Cofre:
        """Crea el cofre de penalizacion definido por la guia."""
        return CofreMaldito()


@dataclass(frozen=True)
class ResultadoRonda:
    """Representa la informacion completa que la vista debe mostrar."""

    numero_ronda: int
    contrasena_generada: str
    estado: str
    cofre: Cofre
    puntaje_total: int
    detalle: str


class JuegoCazador:
    """Modelo que controla rondas, contrasenas, cofres y puntaje acumulado."""

    def __init__(self, aleatorio: random.Random | None = None) -> None:
        """Inicializa una partida independiente con puntaje igual a cero."""
        self._aleatorio = aleatorio or random.Random()
        self._fabrica_cofres = FabricaCofres(self._aleatorio)
        self._puntaje = 0
        self._rondas = 0

    @property
    def puntaje(self) -> int:
        """Expone el puntaje actual sin permitir modificarlo desde fuera."""
        return self._puntaje

    def jugar_ronda(self, texto_longitud: str) -> ResultadoRonda:
        """Genera, valida y califica una ronda a partir de una longitud textual."""
        self._rondas += 1
        contrasena_generada = "No generada"
        try:
            solicitud = Contrasena.desde_longitud_texto(texto_longitud.strip())
            contrasena_generada = solicitud.generar(self._aleatorio)
            cofre = self._fabrica_cofres.crear_cofre_valido()
            estado = "valida"
            detalle = cofre.mensaje_apertura()
        except ErrorJuego as error:
            cofre = self._fabrica_cofres.crear_cofre_maldito()
            estado = "invalida"
            detalle = f"{cofre.mensaje_apertura()} {error}"

        self._puntaje += cofre.puntos
        return ResultadoRonda(
            numero_ronda=self._rondas,
            contrasena_generada=contrasena_generada,
            estado=estado,
            cofre=cofre,
            puntaje_total=self._puntaje,
            detalle=detalle,
        )


class VistaCazador:
    """Vista Tkinter: solo muestra datos y delega acciones al controlador."""

    def __init__(self, raiz: tk.Tk) -> None:
        """Construye los controles visuales y sus variables de presentacion."""
        self._raiz = raiz
        self._longitud = tk.StringVar(value="8")
        self._resultado = tk.StringVar(
            value="Define una longitud y abre tu primer cofre."
        )
        self._puntaje = tk.StringVar(value="Puntaje acumulado: 0")
        self._crear_componentes()

    def configurar_acciones(
        self,
        al_abrir_cofre: Callable[[], None],
        al_salir: Callable[[], None],
    ) -> None:
        """Conecta los eventos de la vista con los casos de uso del controlador."""
        self._boton_abrir.configure(command=al_abrir_cofre)
        self._boton_salir.configure(command=al_salir)
        self._entrada.bind("<Return>", lambda _evento: al_abrir_cofre())

    def obtener_longitud(self) -> str:
        """Obtiene el unico dato que el usuario entrega al juego."""
        return self._longitud.get()

    def mostrar_resultado(self, resultado: ResultadoRonda) -> None:
        """Actualiza la interfaz con la informacion de la ronda procesada."""
        if resultado.estado == "valida":
            texto = (
                f"Ronda {resultado.numero_ronda}: contrasena generada: "
                f"{resultado.contrasena_generada}. Cofre {resultado.cofre.nombre} "
                f"({resultado.cofre.puntos:+d} puntos). {resultado.detalle}"
            )
        else:
            texto = (
                f"Ronda {resultado.numero_ronda}: Cofre {resultado.cofre.nombre} "
                f"({resultado.cofre.puntos:+d} puntos). {resultado.detalle}"
            )
        self._resultado.set(texto)
        self._puntaje.set(f"Puntaje acumulado: {resultado.puntaje_total}")

    def iniciar_bucle(self) -> None:
        """Entrega el control del programa al ciclo de eventos de Tkinter."""
        self._raiz.mainloop()

    def cerrar(self) -> None:
        """Cierra la ventana cuando el jugador decide terminar."""
        self._raiz.destroy()

    def _crear_componentes(self) -> None:
        """Configura la composicion estable de la interfaz grafica."""
        self._raiz.title("Cazador de Contrasenas")
        self._raiz.geometry("680x460")
        self._raiz.minsize(620, 420)
        self._raiz.configure(padx=28, pady=28)
        self._raiz.columnconfigure(0, weight=1)

        ttk.Label(
            self._raiz,
            text="Cazador de Contrasenas",
            font=("Arial", 20, "bold"),
        ).grid(row=0, column=0, columnspan=3, sticky="w")
        ttk.Label(
            self._raiz,
            text="Tu defines la longitud; el juego genera y valida la contrasena aleatoria.",
            wraplength=600,
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=(8, 24))

        ttk.Label(self._raiz, text="Longitud que deseas generar (minimo 8):").grid(
            row=2, column=0, sticky="w"
        )
        self._entrada = ttk.Entry(self._raiz, textvariable=self._longitud, width=12)
        self._entrada.grid(row=2, column=1, sticky="w", padx=12)
        self._boton_abrir = ttk.Button(self._raiz, text="Abrir cofre")
        self._boton_abrir.grid(row=2, column=2, sticky="w")

        ttk.Separator(self._raiz, orient="horizontal").grid(
            row=3, column=0, columnspan=3, sticky="ew", pady=24
        )
        ttk.Label(
            self._raiz,
            textvariable=self._resultado,
            wraplength=600,
            justify="left",
        ).grid(row=4, column=0, columnspan=3, sticky="w")
        ttk.Label(
            self._raiz,
            textvariable=self._puntaje,
            font=("Arial", 11, "bold"),
        ).grid(row=5, column=0, columnspan=3, sticky="w", pady=(20, 8))
        ttk.Label(
            self._raiz,
            text="Reglas: mayuscula, minuscula, numero, caracter especial y sin repetir caracteres.",
            wraplength=600,
        ).grid(row=6, column=0, columnspan=3, sticky="w")
        self._boton_salir = ttk.Button(self._raiz, text="Salir del juego")
        self._boton_salir.grid(row=7, column=0, columnspan=3, sticky="e", pady=(24, 0))


class ControladorCazador:
    """Coordina la vista y el modelo sin incluir reglas de dominio propias."""

    def __init__(self, juego: JuegoCazador, vista: VistaCazador) -> None:
        """Recibe las dependencias y registra los eventos de la interfaz."""
        self._juego = juego
        self._vista = vista
        self._vista.configurar_acciones(self.abrir_cofre, self.salir)

    def abrir_cofre(self) -> None:
        """Procesa una ronda a partir de la longitud solicitada en la vista."""
        resultado = self._juego.jugar_ronda(self._vista.obtener_longitud())
        self._vista.mostrar_resultado(resultado)

    def salir(self) -> None:
        """Finaliza la sesion grafica solicitada por el jugador."""
        self._vista.cerrar()

    def iniciar(self) -> None:
        """Inicia el ciclo grafico sin exponer detalles internos de la vista."""
        self._vista.iniciar_bucle()


def crear_aplicacion() -> ControladorCazador:
    """Compone las capas MVC y devuelve el controlador de la aplicacion."""
    raiz = tk.Tk()
    vista = VistaCazador(raiz)
    juego = JuegoCazador()
    return ControladorCazador(juego, vista)


def iniciar_aplicacion() -> None:
    """Inicia la unica experiencia disponible: el juego grafico."""
    aplicacion = crear_aplicacion()
    aplicacion.iniciar()


if __name__ == "__main__":
    iniciar_aplicacion()
