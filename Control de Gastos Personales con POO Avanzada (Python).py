import json
import csv
from typing import List, Dict


class Movimiento:
    """
    Representa un movimiento financiero (ingreso o gasto).
    """

    def __init__(self, tipo: str, categoria: str, monto: float):
        if tipo not in ("ingreso", "gasto"):
            raise ValueError("El tipo debe ser 'ingreso' o 'gasto'")
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")

        self.tipo = tipo
        self.categoria = categoria
        self.monto = monto

    def to_dict(self) -> Dict:
        """Convierte el movimiento en diccionario (para JSON o CSV)."""
        return {"tipo": self.tipo, "categoria": self.categoria, "monto": self.monto}


class ControlGastos:
    """
    Sistema para registrar ingresos y gastos personales.
    """

    def __init__(self):
        self.movimientos: List[Movimiento] = []

    # ---------- Operaciones principales ----------
    def agregar_movimiento(self, tipo: str, categoria: str, monto: float) -> None:
        """Agrega un nuevo movimiento (ingreso o gasto)."""
        movimiento = Movimiento(tipo, categoria, monto)
        self.movimientos.append(movimiento)

    def calcular_saldo(self) -> float:
        """Devuelve el saldo total (ingresos - gastos)."""
        ingresos = sum(m.monto for m in self.movimientos if m.tipo == "ingreso")
        gastos = sum(m.monto for m in self.movimientos if m.tipo == "gasto")
        return ingresos - gastos

    def resumen_por_categoria(self) -> Dict[str, float]:
        """Genera un resumen de gastos por categoría."""
        resumen: Dict[str, float] = {}
        for m in self.movimientos:
            if m.tipo == "gasto":
                resumen[m.categoria] = resumen.get(m.categoria, 0) + m.monto
        return resumen

    # ---------- Persistencia en JSON ----------
    def guardar_json(self, archivo: str) -> None:
        """Guarda movimientos en archivo JSON."""
        with open(archivo, "w", encoding="utf-8") as f:
            json.dump([m.to_dict() for m in self.movimientos], f, indent=4)

    def cargar_json(self, archivo: str) -> None:
        """Carga movimientos desde archivo JSON."""
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.movimientos = [Movimiento(**item) for item in data]
        except FileNotFoundError:
            self.movimientos = []

    # ---------- Persistencia en CSV ----------
    def guardar_csv(self, archivo: str) -> None:
        """Guarda movimientos en archivo CSV."""
        with open(archivo, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["tipo", "categoria", "monto"])
            writer.writeheader()
            for m in self.movimientos:
                writer.writerow(m.to_dict())

    def cargar_csv(self, archivo: str) -> None:
        """Carga movimientos desde archivo CSV."""
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                self.movimientos = [Movimiento(row["tipo"], row["categoria"], float(row["monto"])) for row in reader]
        except FileNotFoundError:
            self.movimientos = []


# =======================
# Ejemplo de uso real
# =======================
if __name__ == "__main__":
    sistema = ControlGastos()

    # Registrar movimientos
    sistema.agregar_movimiento("ingreso", "salario", 2500)
    sistema.agregar_movimiento("gasto", "alimentación", 300)
    sistema.agregar_movimiento("gasto", "transporte", 150)
    sistema.agregar_movimiento("gasto", "ocio", 200)

    # Calcular saldo
    print(f" Saldo actual: ${sistema.calcular_saldo()}")

    # Resumen por categoría
    print("\n Resumen de gastos por categoría:")
    for categoria, total in sistema.resumen_por_categoria().items():
        print(f" - {categoria}: ${total}")

    # Guardar en archivos
    sistema.guardar_json("movimientos.json")
    sistema.guardar_csv("movimientos.csv")

    # Cargar desde archivos
    nuevo_sistema = ControlGastos()
    nuevo_sistema.cargar_json("movimientos.json")
    print(f"\n Cargados desde JSON, saldo: ${nuevo_sistema.calcular_saldo()}")
