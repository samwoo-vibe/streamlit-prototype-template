import importlib.util
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def load_handoff_exporter():
    path = ROOT / "scripts/export_handoff.py"
    spec = importlib.util.spec_from_file_location("streamlit_handoff_exporter", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_compose_requires_routing_and_database_inputs() -> None:
    compose = read("compose.yaml")

    assert "${COOLIFY_RESOURCE_UUID:?COOLIFY_RESOURCE_UUID must be provided by Coolify}" in compose
    assert "${DATABASE_URL:?DATABASE_URL must be configured in Coolify}" in compose
    assert "${APP_BASE_URL:?APP_BASE_URL must be configured in Coolify}" in compose


def test_container_runs_streamlit_as_pid_one_after_migrations() -> None:
    dockerfile = read("Dockerfile")
    dockerignore = read(".dockerignore")

    assert "ENTRYPOINT []" in dockerfile
    assert "alembic upgrade head && exec streamlit run" in dockerfile
    assert "COPY . ." in dockerfile
    assert "chown -R" not in dockerfile
    assert "_handoff" in dockerignore
    assert dockerfile.count("@sha256:") == 2
    assert "COPY --from=ghcr.io/astral-sh/uv:0.11.32@sha256:" in dockerfile


def test_streamlit_request_sizes_fit_the_container_budget() -> None:
    config = read(".streamlit/config.toml")
    gitignore = read(".gitignore")
    dockerignore = read(".dockerignore")

    assert "maxUploadSize = 50" in config
    assert "maxMessageSize = 50" in config
    assert "enableCORS = true" in config
    assert "enableXsrfProtection = true" in config
    assert ".streamlit/secrets.toml" in gitignore
    assert ".streamlit/secrets.toml" in dockerignore


def test_public_streamlit_hides_exception_details() -> None:
    config = read(".streamlit/config.toml")
    local_start = read("start.cmd")
    dockerfile = read("Dockerfile")

    assert 'showErrorDetails = "none"' in config
    assert "showErrorDetails=full" in local_start
    assert "showErrorDetails=full" not in dockerfile


def test_application_does_not_create_schema_outside_alembic() -> None:
    application_paths = [ROOT / "app.py"]
    application_paths.extend((ROOT / "src").rglob("*.py"))
    application_paths.extend((ROOT / "pages").rglob("*.py"))
    application_sources = [path.read_text(encoding="utf-8") for path in application_paths]

    assert all("create_tables" not in source for source in application_sources)
    assert all(".create_all(" not in source for source in application_sources)


def test_public_note_listing_is_bounded() -> None:
    repository = read("src/samwoo_prototype/repositories/notes.py")

    assert ".limit(100)" in repository


def test_anonymous_demo_data_is_local_sqlite_only() -> None:
    from samwoo_prototype.config import allows_local_demo_data

    assert allows_local_demo_data("sqlite:///./data/prototype.db")
    assert not allows_local_demo_data("postgresql+psycopg://app_role:password@database:5432/app_db")

    application = read("app.py")
    assert "local_demo = allows_local_demo_data(get_settings().database_url)" in application
    assert application.count("if local_demo:") == 2
    assert "공개 배포에서는 익명 저장이 비활성화" in application
    assert "PostgreSQL 레코드를 공개 화면에서 조회하지 않습니다" in application


def test_documents_describe_public_by_default_access() -> None:
    readme = read("README.md")
    agents = read("AGENTS.md")

    assert "회사 공용 HTTP Basic Auth를 먼저 적용" not in readme
    assert "기본 공개" in readme
    assert "기본 공개" in agents
    assert "앱 안에 자체 인증·인가" in agents


def test_bmad_scope_is_downstream_app_development_only() -> None:
    readme = read("README.md")
    agents = read("AGENTS.md")

    assert "이 템플릿으로 파생 앱을 바이브코딩하는 작업에만 적용" in readme
    assert "Coolify·프로비저너 운영 또는 원본 템플릿 자체의 유지보수" in agents
    assert "BMAD 없는 인계 저장소" in agents


def test_gitpython_security_floor_is_locked() -> None:
    lock = read("uv.lock")
    match = re.search(
        r'\[\[package\]\]\nname = "gitpython"\nversion = "(\d+)\.(\d+)\.(\d+)"',
        lock,
    )

    assert match is not None
    assert tuple(map(int, match.groups())) >= (3, 1, 58)


def test_handoff_keeps_tests_and_development_contract() -> None:
    exporter = read("scripts/export_handoff.py")

    assert '"pyproject.toml",' in exporter
    assert '"tests",' in exporter
    assert '"scripts",' in exporter
    assert '"tests/test_deployment_contract.py",' in exporter
    assert '".streamlit/config.toml",' in exporter
    assert "runtime_pyproject" not in exporter
    assert '(export_root / ".gitignore").write_text' not in exporter


def test_local_environment_defines_the_canonical_base_url() -> None:
    env_example = read(".env.example")

    assert "APP_BASE_URL=http://127.0.0.1:8501" in env_example


def test_compose_limits_service_cpu() -> None:
    compose = read("compose.yaml")

    assert compose.count('cpus: "1.0"') == 1
    assert compose.count("pids_limit: 256") == 1
    assert 'user: "10001:10001"' in compose
    assert "- ALL" in compose
    assert "- no-new-privileges:true" in compose


def test_postgresql_pool_fits_the_provisioned_role_limit() -> None:
    database = read("src/samwoo_prototype/database.py")

    assert "pool_size=5" in database
    assert "max_overflow=3" in database
    assert "pool_timeout=5" in database
    assert 'connect_args={"connect_timeout": 5}' in database
    assert '"connect_timeout": 5' in read("migrations/env.py")


def test_handoff_rejects_environment_and_private_key_files(tmp_path: Path) -> None:
    exporter = load_handoff_exporter()

    assert exporter.should_exclude(Path(".env.production"))
    assert exporter.should_exclude(Path(".envrc"))
    assert exporter.should_exclude(Path("client-secret.txt"))
    assert exporter.should_exclude(Path("signing.key"))
    assert exporter.should_exclude(Path("id_ed25519"))
    assert exporter.should_exclude(Path(".ssh/id_ecdsa"))
    assert exporter.should_exclude(Path(".streamlit/secrets.toml"))
    assert exporter.should_exclude(Path("config/credentials.json"))
    assert exporter.should_exclude(Path(".aws/credentials"))
    assert exporter.should_exclude(Path("application_default_credentials.json"))
    assert exporter.should_exclude(Path("data/cache.sqlite-wal"))
    assert exporter.should_exclude(Path("data/cache.db-journal"))
    assert exporter.should_exclude(Path("backups/prod.db.bak"))
    assert exporter.should_exclude(Path("copies/cache.sqlite.copy"))
    assert not exporter.should_exclude(Path(".env.example"))
    sensitive_file = tmp_path / "client-secret.txt"
    sensitive_file.touch()
    with pytest.raises(ValueError, match="비밀 가능성"):
        exporter.copy_source(sensitive_file, tmp_path / "exported.txt")


def test_dockerignore_excludes_nested_credentials() -> None:
    dockerignore = read(".dockerignore")

    for pattern in (
        "**/.git",
        "**/.env",
        "**/.env.*",
        ".env*",
        "**/.env*",
        "**/*.pem",
        "**/.npmrc",
        "**/.ssh",
        "**/id_ed25519",
        "**/secrets.*",
        "**/credentials.*",
        "**/.streamlit/secrets.*",
        "*.db*",
        "**/*.db*",
        "*.sqlite*",
        "**/*.sqlite*",
    ):
        assert pattern in dockerignore

    gitignore = read(".gitignore")
    assert "secrets.*" in gitignore
    assert "credentials.*" in gitignore
    assert "id_ed25519" in gitignore
    assert ".ssh/" in gitignore
    assert "*.db" in gitignore
    assert "*.sqlite" in gitignore
    assert "*.sqlite-*" in gitignore
    assert "**/*.db" in dockerignore
    assert "**/*.sqlite3" in dockerignore
    assert "*.db*" in gitignore
    assert "*.sqlite*" in gitignore


def test_handoff_rejects_recursive_project_output() -> None:
    exporter = load_handoff_exporter()

    with pytest.raises(ValueError, match="_handoff"):
        exporter.validate_output_dir(ROOT, ROOT / "src" / "export")
