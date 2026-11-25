"""Подстановка локальных .puml-файлов в блоки puml до mkdocs_puml."""

from pathlib import Path
import re

from mkdocs.exceptions import PluginError
from mkdocs.plugins import event_priority


PUML_FENCE = re.compile(
    r"```puml[ \t]*\r?\n(?P<body>.*?)\r?\n```",
    flags=re.DOTALL,
)
FILE_DIRECTIVE = re.compile(r'--8<--[ \t]+"(?P<path>[^"\r\n]+\.puml)"')


@event_priority(100)
def on_page_markdown(markdown: str, config, page, **kwargs) -> str:
    """Разворачивает блок, содержащий только ссылку на локальный .puml."""

    docs_dir = Path(config.docs_dir).resolve()

    def expand(match: re.Match[str]) -> str:
        directive = FILE_DIRECTIVE.fullmatch(match.group("body").strip())
        if directive is None:
            return match.group(0)

        relative_path = Path(directive.group("path"))
        source_path = (docs_dir / relative_path).resolve()

        if source_path != docs_dir and docs_dir not in source_path.parents:
            raise PluginError(
                f"PlantUML-файл должен находиться внутри docs/: {relative_path}"
            )
        if not source_path.is_file():
            raise PluginError(
                f"PlantUML-файл не найден для страницы {page.file.src_uri}: "
                f"{relative_path}"
            )

        source = source_path.read_text(encoding="utf-8").rstrip()
        return f"```puml\n{source}\n```"

    return PUML_FENCE.sub(expand, markdown)
