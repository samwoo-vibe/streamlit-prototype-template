"""Create a deployment-ready handoff package for Nextcloud and a new Git repository."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path

INCLUDED_FILES = (
    "README.md",
    "AGENTS.md",
    ".dockerignore",
    ".env.example",
    ".gitignore",
    ".python-version",
    "Dockerfile",
    "compose.yaml",
    "samwoo-service.yaml",
    "alembic.ini",
    "app.py",
    "start.cmd",
    "uv.lock",
)
INCLUDED_DIRECTORIES = (
    "src",
    "pages",
    "components",
    "assets",
    "static",
    "templates",
    "locales",
    ".streamlit",
    "migrations",
)
REQUIRED_FILES = (
    "Dockerfile",
    "compose.yaml",
    "samwoo-service.yaml",
    "alembic.ini",
    "migrations/env.py",
    "uv.lock",
)
EXCLUDED_NAMES = {
    ".git",
    ".agents",
    "_bmad",
    "_bmad-output",
    "_handoff",
    "tests",
    "data",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
}
EXCLUDED_SUFFIXES = (
    ".db",
    ".db-shm",
    ".db-wal",
    ".log",
    ".pyc",
    ".pyo",
    ".tmp",
)
SECRET_NAME_PATTERN = re.compile(
    r"(^|[._-])(secret|token|password|passwd|credential|private[-_]?key)([._-]|$)",
    re.IGNORECASE,
)


def safe_project_name(raw_name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9가-힣._-]+", "-", raw_name.strip()).strip(".-")
    if not name:
        raise ValueError("프로젝트 이름에 사용할 수 있는 문자가 없습니다.")
    return name


def should_exclude(path: Path) -> bool:
    if any(part in EXCLUDED_NAMES for part in path.parts):
        return True
    if path.name == ".env" or SECRET_NAME_PATTERN.search(path.name):
        return True
    return path.name.lower().endswith(EXCLUDED_SUFFIXES)


def copy_source(source: Path, destination: Path) -> None:
    if source.is_symlink():
        raise ValueError(f"심볼릭 링크는 인수인계본에 포함할 수 없습니다: {source}")
    if source.is_dir():
        for child in sorted(source.iterdir()):
            relative = child.relative_to(source)
            if should_exclude(relative):
                continue
            copy_source(child, destination / relative)
        return
    if should_exclude(source):
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def runtime_pyproject(content: str) -> str:
    """Remove development-only TOML sections while preserving runtime metadata."""
    excluded_sections = ("[dependency-groups]", "[tool.pytest.", "[tool.ruff")
    output: list[str] = []
    skipping = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            skipping = any(stripped.startswith(section) for section in excluded_sections)
        if not skipping:
            output.append(line)
    return "\n".join(output).rstrip() + "\n"


def write_handoff_files(project_root: Path, export_root: Path, project_name: str) -> None:
    for name in INCLUDED_FILES:
        source = project_root / name
        if source.exists():
            copy_source(source, export_root / name)

    for name in INCLUDED_DIRECTORIES:
        source = project_root / name
        if source.exists():
            copy_source(source, export_root / name)

    # Preserve root-level application modules without copying maintenance scripts.
    for source in sorted(project_root.glob("*.py")):
        copy_source(source, export_root / source.name)

    pyproject = project_root / "pyproject.toml"
    if not pyproject.is_file():
        raise FileNotFoundError("pyproject.toml을 찾을 수 없습니다.")
    (export_root / "pyproject.toml").write_text(
        runtime_pyproject(pyproject.read_text(encoding="utf-8")),
        encoding="utf-8",
    )

    (export_root / ".gitignore").write_text(
        ".venv/\n__pycache__/\n*.py[cod]\n.env\ndata/\n*.db\n*.db-*\n",
        encoding="utf-8",
    )
    (export_root / "SOURCE-HANDOFF.md").write_text(
        f"""# {project_name} 소스코드 인수인계

이 폴더는 Streamlit Template 기반 앱의 검토·배포를 위한 소스코드 전달본입니다.
압축을 새 private GitHub 저장소의 루트에 풀면 별도 파일 이동 없이 바로 커밋할 수
있습니다.

## 포함 범위

- Streamlit 화면: `app.py`, `pages/`
- 재사용 대상 업무 코드: `src/`
- 화면 자산과 Streamlit 설정
- 런타임 의존성: `pyproject.toml`, `uv.lock`
- Coolify 배포 파일: `Dockerfile`, `compose.yaml`, `samwoo-service.yaml`
- PostgreSQL migration: `alembic.ini`, `migrations/`
- 비밀값이 없는 환경변수 예시: `.env.example`

## 의도적으로 제외한 항목

- BMAD 산출물과 테스트·린트 전용 파일
- SQLite DB, 사용자 입력 데이터와 로컬 업로드 파일
- `.env`, 토큰, 비밀번호, 개인정보
- 캐시, 가상환경, 로그, 임시 파일
- 원본 Git 이력과 remote

관리자는 이 ZIP을 새 private GitHub 저장소의 루트에 압축 해제한 뒤, 파일을
추가하거나 이동하지 않고 `main`에 최초 Push할 수 있습니다. 이후 기존
GitHub → Provisioner → Coolify 자동 배포가 이어집니다.
""",
        encoding="utf-8",
    )


def validate_export(export_root: Path) -> list[Path]:
    for relative_name in REQUIRED_FILES:
        if not (export_root / relative_name).is_file():
            raise ValueError(f"배포 필수 파일이 없습니다: {relative_name}")
    files = sorted(path for path in export_root.rglob("*") if path.is_file())
    if not (export_root / "app.py").is_file():
        raise ValueError("내보내기 결과에 app.py가 없습니다.")
    if not any((export_root / "src").rglob("*.py")):
        raise ValueError("내보내기 결과에 src Python 코드가 없습니다.")
    for path in files:
        relative = path.relative_to(export_root)
        if should_exclude(relative):
            raise ValueError(f"제외 대상 파일이 결과에 포함되었습니다: {relative}")
    return files


def create_zip(export_root: Path, archive: Path) -> None:
    # The archive is extracted directly into the new repository root. Do not
    # add the local ``<project>-source`` directory as a wrapper folder.
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(export_root.rglob("*")):
            if path.is_file():
                bundle.write(path, path.relative_to(export_root))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-name", help="인수인계본에 사용할 프로젝트 이름")
    parser.add_argument(
        "--output-dir",
        type=Path,
        help="출력 디렉터리(기본값: 프로젝트의 _handoff)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project_root = Path(__file__).resolve().parents[1]
    project_name = safe_project_name(args.project_name or project_root.name)
    output_dir = (args.output_dir or project_root / "_handoff").resolve()
    export_root = output_dir / f"{project_name}-source"
    archive = output_dir / f"{project_name}-source.zip"

    if export_root.exists() or archive.exists():
        print(
            f"기존 인수인계본이 있습니다. 검토 후 직접 치우고 다시 실행하세요: {output_dir}",
            file=sys.stderr,
        )
        return 2

    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        export_root.mkdir()
        write_handoff_files(project_root, export_root, project_name)
        files = validate_export(export_root)
        create_zip(export_root, archive)
    except Exception:
        if export_root.exists():
            shutil.rmtree(export_root)
        if archive.exists():
            archive.unlink()
        raise

    print(f"폴더: {export_root}")
    print(f"Nextcloud ZIP (저장소 루트 직결): {archive}")
    print(f"포함 파일: {len(files)}개")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
