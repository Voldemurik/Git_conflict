import os
import subprocess
import sys
from pathlib import Path

from benchmark import prepare_benchmark
from variants import get_variant


def has_student_merge():
    try:
        result = subprocess.run(
            [
                "git",
                "rev-list",
                "--min-parents=2",
                "origin/master..HEAD",
            ],
            capture_output=True,
            text=True,
            check=True,
        )

        return bool(
            result.stdout.strip()
        )

    except Exception:
        return False


def has_nonempty_readme():
    path = Path(
        "README.md"
    )

    if not path.exists():
        return False

    try:
        return bool(
            path.read_text(
                encoding="utf-8"
            ).strip()
        )

    except Exception:
        return False


def has_required_dependencies(
    variant,
):
    path = Path(
        "requirements.txt"
    )

    if not path.exists():
        return False

    try:
        installed = set()

        for line in path.read_text(
            encoding="utf-8"
        ).splitlines():

            line = line.strip()

            if (
                not line
                or line.startswith("#")
            ):
                continue

            package = (
                line
                .split("==")[0]
                .split(">=")[0]
                .split("<=")[0]
                .split("~=")[0]
                .strip()
                .lower()
            )

            if package:
                installed.add(
                    package
                )

    except Exception:
        return False

    required = {
        package.lower()
        for package
        in variant.get(
            "requirements",
            [],
        )
    }

    return required.issubset(
        installed
    )


def main():
    try:
        variant_id = int(
            os.environ[
                "QUEST_VARIANT"
            ]
        )

        variant = get_variant(
            variant_id
        )

    except Exception:
        print(
            "❌ Не удалось определить "
            "вариант задания"
        )
        sys.exit(1)

    print(
        "=== Проверка решения ==="
    )
    print()

    try:
        source = (
            variant[
                "test_data"
            ]()
        )

        result = (
            prepare_benchmark(
                source
            )
        )

        checks = (
            variant["check"](
                result,
                source,
            )
        )

    except Exception:
        checks = {
            "Выполнение решения":
                False,
        }

    for name, passed in (
        checks.items()
    ):
        mark = (
            "✅"
            if passed
            else "❌"
        )

        print(
            f"{mark} {name}"
        )

    merge_ok = (
        has_student_merge()
    )

    readme_ok = (
        has_nonempty_readme()
    )

    dependencies_ok = (
        has_required_dependencies(
            variant
        )
    )

    print(
        "✅ История изменений"
        if merge_ok
        else "❌ История изменений"
    )

    print(
        "✅ README"
        if readme_ok
        else "❌ README"
    )

    print(
        "✅ Зависимости проекта"
        if dependencies_ok
        else "❌ Зависимости проекта"
    )

    print()

    all_ok = (
        all(checks.values())
        and merge_ok
        and readme_ok
        and dependencies_ok
    )

    if all_ok:
        print(
            "✅ Задание выполнено"
        )
        sys.exit(0)

    print(
        "❌ Решение пока не "
        "соответствует требованиям"
    )

    sys.exit(1)


if __name__ == "__main__":
    main()