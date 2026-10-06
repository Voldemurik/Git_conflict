import argparse
import csv
from pathlib import Path

from variants import get_variant


def write_data(
    variant,
    output_path,
):
    output = Path(output_path)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with output.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.writer(file)

        writer.writerow(
            variant["data_columns"]
        )

        writer.writerows(
            variant["data_rows"]
        )


def write_code(
    variant,
    target,
    output_path,
):
    key = {
        "base":
            "base_code",

        "branch_a":
            "branch_a_code",

        "branch_b":
            "branch_b_code",
    }[target]

    output = Path(output_path)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.write_text(
        variant[key].strip() + "\n",
        encoding="utf-8",
    )


def update_requirements(
    variant,
    output_path,
):
    path = Path(output_path)

    existing = set()

    if path.exists():
        existing = {
            line.strip()
            for line
            in path.read_text(
                encoding="utf-8"
            ).splitlines()
            if line.strip()
        }

    existing.update(
        variant.get(
            "requirements",
            [],
        )
    )

    path.write_text(
        "\n".join(
            sorted(existing)
        ) + "\n",
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--variant",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--target",
        choices=[
            "base",
            "branch_a",
            "branch_b",
            "data",
        ],
        required=True,
    )

    parser.add_argument(
        "--output",
        default="src/benchmark.py",
    )

    parser.add_argument(
        "--data-output",
        default="data/benchmark.csv",
    )

    parser.add_argument(
        "--requirements-output",
        default=None,
    )

    args = parser.parse_args()

    variant = get_variant(
        args.variant
    )

    if args.target == "data":
        write_data(
            variant,
            args.data_output,
        )

        print(
            f"Generated data for "
            f"variant {args.variant}"
        )

        return

    write_code(
        variant,
        args.target,
        args.output,
    )

    if args.requirements_output:
        update_requirements(
            variant,
            args.requirements_output,
        )

    print(
        f"Generated variant "
        f"{args.variant}: "
        f"{variant['name']} / "
        f"{args.target}"
    )


if __name__ == "__main__":
    main()