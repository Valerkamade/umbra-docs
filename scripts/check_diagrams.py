"""Проверяет, что PlantUML-блоки заменены корректными SVG."""

from pathlib import Path
import sys


FAILURE_MARKERS = (
    "diagram failed to render",
    "plantuml error",
    "syntax error",
    'class="diagram-key"',
)


def main() -> int:
    site_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "site")
    if not site_dir.is_dir():
        print(f"Каталог сборки не найден: {site_dir}", file=sys.stderr)
        return 1

    html = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in site_dir.rglob("*.html")
    )
    lowered = html.lower()
    failures = [marker for marker in FAILURE_MARKERS if marker in lowered]
    containers = html.count("puml-container")
    diagrams = html.count('class="diagram"')

    if failures:
        print(
            "Обнаружены признаки ошибки PlantUML: " + ", ".join(failures),
            file=sys.stderr,
        )
        return 1
    if containers == 0:
        print("В сборке не найдено ни одной PlantUML-диаграммы.", file=sys.stderr)
        return 1
    if diagrams < containers:
        print(
            f"Не все PlantUML-блоки преобразованы в SVG: {diagrams}/{containers}.",
            file=sys.stderr,
        )
        return 1

    print(f"PlantUML: корректно отрисовано SVG: {diagrams}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
