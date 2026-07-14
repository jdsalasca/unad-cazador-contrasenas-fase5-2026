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
        random.seed(20)
        contrasena = MODULO.Contrasena(12)
        valor = contrasena.generar()

        self.assertEqual(len(valor), 12)
        self.assertEqual(len(set(valor)), len(valor))
        contrasena.validar(valor)

    def test_longitud_menor_a_ocho_lanza_excepcion(self) -> None:
        with self.assertRaises(MODULO.LongitudInvalidaError):
            MODULO.Contrasena(7)

    def test_dato_no_numerico_lanza_excepcion(self) -> None:
        with self.assertRaises(MODULO.DatoNoNumericoError):
            MODULO.Contrasena.desde_texto("ocho")

    def test_caracteres_repetidos_no_superan_validacion(self) -> None:
        contrasena = MODULO.Contrasena(8)
        with self.assertRaises(MODULO.ContrasenaIncorrectaError):
            contrasena.validar("AAa1!bcd")


class PruebasJuego(unittest.TestCase):
    def test_entrada_invalida_abre_cofre_maldito(self) -> None:
        juego = MODULO.JuegoCazador()
        resultado = juego.jugar_ronda("abc")

        self.assertEqual(resultado["estado"], "invalida")
        self.assertEqual(resultado["cofre"], "Maldito")
        self.assertEqual(resultado["puntos_ronda"], -20)
        self.assertEqual(resultado["puntaje_total"], -20)

    def test_ronda_valida_muestra_contrasena_y_suma_puntos(self) -> None:
        random.seed(5)
        juego = MODULO.JuegoCazador()
        resultado = juego.jugar_ronda("8")

        self.assertEqual(resultado["estado"], "valida")
        self.assertEqual(len(resultado["contrasena"]), 8)
        self.assertIn(resultado["cofre"], {"Comun", "Raro", "Legendario"})
        self.assertIn(resultado["puntos_ronda"], {10, 25, 50})
        self.assertEqual(resultado["puntaje_total"], resultado["puntos_ronda"])

    def test_varias_rondas_conservan_puntaje_y_contador(self) -> None:
        random.seed(8)
        juego = MODULO.JuegoCazador()
        primera = juego.jugar_ronda("8")
        segunda = juego.jugar_ronda("12")

        self.assertEqual(segunda["ronda"], 2)
        self.assertEqual(
            segunda["puntaje_total"], primera["puntos_ronda"] + segunda["puntos_ronda"]
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


if __name__ == "__main__":
    unittest.main(verbosity=2)
