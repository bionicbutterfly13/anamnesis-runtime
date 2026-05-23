import ast
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1] / "src" / "anamnesis_runtime"

FORBIDDEN_IMPORT_ROOTS = {
    "api",
    "autonoesis",
    "dionysus",
    "elume",
    "eventbus",
    "fastapi",
    "graphiti",
    "linoss",
    "pika",
    "qdrant_client",
    "redis",
    "sakshi",
}


def _import_roots(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    roots: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            roots.update(alias.name.split(".", maxsplit=1)[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            roots.add(node.module.split(".", maxsplit=1)[0])
    return roots


def test_core_package_has_no_host_or_transport_imports() -> None:
    violations: dict[str, set[str]] = {}

    for path in PACKAGE_ROOT.rglob("*.py"):
        imported = _import_roots(path)
        forbidden = imported & FORBIDDEN_IMPORT_ROOTS
        if forbidden:
            violations[str(path.relative_to(PACKAGE_ROOT.parents[1]))] = forbidden

    assert violations == {}

