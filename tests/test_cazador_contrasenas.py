"""Pruebas unitarias del motor del juego Cazador de Contrasenas."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import random
import sys
import unittest


RUTA_MODULO = Path(__file__).resolve().parents[1] / "cazador_contrasenas.py"
ESPECIFICACION = importlib.util.spec_from_file_location("cazador", RUTA_MODULO)
assert ESPECIFICACION is not None
assert ESPECIFICACION.loader is not None
MODULO = importlib.util.module_from_spec(ESPECIFICACION)
sys.modules["cazador"] = MODULO
ESPECIFICACION.loader.exec_module(MODULO)


class PruebasContrasena(unittest.TestCase):
    def test_generar_contrasena_cumple_reglas(self) -> None:
        contrasena = MODULO.Contrasena(12)
        valor = contrasena.generar(random.Random(20))

        self.assertEqual(len(valor), 12)
        self.assertEqual(len(set(valor)), len(valor))
        contrasena.validar(valor)

    def test_longitud_menor_a_ocho_lanza_excepcion(self) -> None:
        with self.assertRaises(MODULO.LongitudInvalidaError):
            MODULO.Contrasena(7)

    def test_dato_no_numerico_lanza_excepcion(self) -> None:
        with self.assertRaises(MODULO.DatoNoNumericoError):
            MODULO.Contrasena.desde_longitud_texto("ocho")

    def test_caracteres_repetidos_no_superan_validacion(self) -> None:
        contrasena = MODULO.Contrasena(8)
        with self.assertRaises(MODULO.ContrasenaIncorrectaError):
            contrasena.validar("AAa1!bcd")


class PruebasJuego(unittest.TestCase):
    def test_entrada_invalida_abre_cofre_maldito(self) -> None:
        juego = MODULO.JuegoCazador()
        resultado = juego.jugar_ronda("abc")

        self.assertEqual(resultado.estado, "invalida")
        self.assertEqual(resultado.cofre.nombre, "Maldito")
        self.assertEqual(resultado.cofre.puntos, -20)
        self.assertEqual(resultado.puntaje_total, -20)

    def test_ronda_valida_muestra_contrasena_y_suma_puntos(self) -> None:
        juego = MODULO.JuegoCazador(random.Random(5))
        resultado = juego.jugar_ronda("8")

        self.assertEqual(resultado.estado, "valida")
        self.assertEqual(len(resultado.contrasena_generada), 8)
        self.assertIn(resultado.cofre.nombre, {"Comun", "Raro", "Legendario"})
        self.assertIn(resultado.cofre.puntos, {10, 25, 50})
        self.assertEqual(resultado.puntaje_total, resultado.cofre.puntos)

    def test_varias_rondas_conservan_puntaje_y_contador(self) -> None:
        juego = MODULO.JuegoCazador(random.Random(8))
        primera = juego.jugar_ronda("8")
        segunda = juego.jugar_ronda("12")

        self.assertEqual(segunda.numero_ronda, 2)
        self.assertEqual(
            segunda.puntaje_total, primera.cofre.puntos + segunda.cofre.puntos
        )

    def test_cofres_especializados_heredan_de_cofre(self) -> None:
        self.assertIsInstance(MODULO.CofreComun(), MODULO.Cofre)
        self.assertIsInstance(MODULO.CofreRaro(), MODULO.Cofre)
        self.assertIsInstance(MODULO.CofreLegendario(), MODULO.Cofre)
        self.assertIsInstance(MODULO.CofreMaldito(), MODULO.Cofre)
        self.assertNotEqual(
            MODULO.CofreComun().mensaje_apertura(),
            MODULO.CofreLegendario().mensaje_apertura(),
        )


class VistaDePrueba:
    """Doble de prueba que evita abrir una ventana durante las pruebas unitarias."""

    def __init__(self, longitud: str) -> None:
        self._longitud = longitud
        self.resultado = None
        self.cerrada = False
        self.accion_abrir = None
        self.accion_salir = None

    def configurar_acciones(self, al_abrir_cofre, al_salir) -> None:
        self.accion_abrir = al_abrir_cofre
        self.accion_salir = al_salir

    def obtener_longitud(self) -> str:
        return self._longitud

    def mostrar_resultado(self, resultado) -> None:
        self.resultado = resultado

    def cerrar(self) -> None:
        self.cerrada = True

    def iniciar_bucle(self) -> None:
        return None


class PruebasControlador(unittest.TestCase):
    def test_controlador_coordina_modelo_y_vista(self) -> None:
        vista = VistaDePrueba("8")
        juego = MODULO.JuegoCazador(random.Random(11))
        controlador = MODULO.ControladorCazador(juego, vista)

        controlador.abrir_cofre()

        self.assertIsNotNone(vista.resultado)
        self.assertEqual(vista.resultado.estado, "valida")
        self.assertEqual(juego.puntaje, vista.resultado.puntaje_total)

    def test_controlador_delega_el_cierre_a_la_vista(self) -> None:
        vista = VistaDePrueba("8")
        controlador = MODULO.ControladorCazador(MODULO.JuegoCazador(), vista)

        controlador.salir()

        self.assertTrue(vista.cerrada)


if __name__ == "__main__":
    unittest.main(verbosity=2)
