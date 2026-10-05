
from pathlib import Path
import subprocess
import time
import matplotlib.pyplot as plt

CARPETA = Path(__file__).resolve().parent
TAMANOS = [1, 10, 100, 1000, 10000, 100000, 1000000]
LIMITE_SEGUNDOS = 100
REPETICIONES = 5


def compilar(problema):
    ejecutable = CARPETA / "bin" / f"problema{problema}.exe"
    subprocess.run([
        "gcc", "-std=c11", "-O2", "-Wall", "-Wextra", "-Wpedantic",
        str(CARPETA / "ejercicios" / f"problema{problema}.c"),
        "-o", str(ejecutable)
    ], check=True)
    return ejecutable


def medir(ejecutable):
    try:
        subprocess.run([str(ejecutable), "10"], stdout=subprocess.DEVNULL,
                       timeout=LIMITE_SEGUNDOS, check=True)
    except subprocess.TimeoutExpired:
        print(f"{ejecutable.stem}: el calentamiento agoto el tiempo.", flush=True)

    resultados = []
    for n in TAMANOS:
        tiempos = []
        for _ in range(REPETICIONES):
            inicio = time.perf_counter()
            try:
                subprocess.run([str(ejecutable), str(n)],
                               stdout=subprocess.DEVNULL,
                               timeout=LIMITE_SEGUNDOS, check=True)
                tiempos.append(time.perf_counter() - inicio)
            except subprocess.TimeoutExpired:
                break

        segundos = None
        if len(tiempos) == REPETICIONES:
            # Ordenar y tomar el centro; tambien funciona con cantidades pares.
            tiempos.sort()
            centro = len(tiempos) // 2
            segundos = (tiempos[(len(tiempos) - 1) // 2] + tiempos[centro]) / 2
        resultados.append((n, segundos))
        texto = f"{segundos:.6f} s" if segundos is not None else "Tiempo agotado"
        print(f"{ejecutable.stem}, n={n}: {texto}", flush=True)
    return resultados


def guardar(problema, resultados):
    salida = CARPETA / "resultados"
    tabla = [f"Problema {problema}: entrada vs. tiempo",
             f"{'Entrada n':>12} | {'Mediana (segundos)':>20}",
             "-" * 35]
    for n, segundos in resultados:
        texto = f"{segundos:.6f}" if segundos is not None else "Tiempo agotado"
        tabla.append(f"{n:>12} | {texto:>20}")
    tabla.append(f"\nLimite por ejecucion: {LIMITE_SEGUNDOS} segundos.")
    tabla.append(f"Mediana de {REPETICIONES} ejecuciones por entrada; calentamiento excluido.")
    (salida / f"problema{problema}_tabla.txt").write_text(
        "\n".join(tabla) + "\n", encoding="utf-8")

    entradas = [n for n, t in resultados if t is not None]
    tiempos = [t for _, t in resultados if t is not None]
    figura, eje = plt.subplots(figsize=(8, 5))
    if entradas:
        eje.plot(entradas, tiempos, "o-")
        eje.set_xscale("log")
        eje.set_yscale("log")
    else:
        eje.text(0.5, 0.5, "No hay ejecuciones completas",
                 ha="center", transform=eje.transAxes)
    eje.set_title(f"Problema {problema}: entrada vs. tiempo")
    eje.set_xlabel("Entrada n")
    eje.set_ylabel("Mediana del tiempo (segundos)")
    eje.grid(True, alpha=0.3)
    figura.text(0.5, 0.02, "Los casos con tiempo agotado no se grafican.", ha="center")
    figura.tight_layout(rect=(0, 0.05, 1, 1))
    figura.savefig(salida / f"problema{problema}_grafica.png", dpi=160)
    plt.close(figura)


def main():
    (CARPETA / "bin").mkdir(exist_ok=True)
    (CARPETA / "resultados").mkdir(exist_ok=True)
    for problema in (1, 2, 3):
        ejecutable = compilar(problema)
        resultados = medir(ejecutable)
        guardar(problema, resultados)
    print("Listo: tres tablas TXT y tres graficas PNG en resultados/.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, subprocess.CalledProcessError) as error:
        raise SystemExit(f"Error: {error}")
