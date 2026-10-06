"""Variant 11: Summarization Benchmark."""

NAME = 'Summarization Benchmark'
EXTRA_REQUIREMENTS = ["numpy"]

DATA_COLUMNS = ['model', 'compression_ratio', 'faithfulness']

DATA_ROWS = [['Nova-7B', 0.35, 0.88], ['Sigma-8B', 0.55, 0.75], ['Atlas-Agent', 0.25, 0.94], ['Orion-13B', 0.7, 0.81], ['Boundary30', 0.3, 0.8], ['Boundary60', 0.6, 0.83], ['Compact-1B', 0.15, 0.68], ['Verbose-X', 0.82, 0.89], ['Balanced-M', 0.45, 0.86], ['Research-S', 0.28, 0.91]]


def make_test_data():
    import pandas as pd

    return pd.DataFrame(
        DATA_ROWS,
        columns=DATA_COLUMNS,
    )


def check(result, source):
    structure_ok = "compression_class" in result.columns
    integration_ok = False
    processing_ok = False
    if structure_ok:
        try:
            v = result.set_index("model")
            integration_ok = (
                v.loc["Atlas-Agent", "compression_ratio"] == 25
                and v.loc["Atlas-Agent", "compression_class"] == "strong"
                and v.loc["Boundary30", "compression_class"] == "balanced"
                and v.loc["Boundary60", "compression_class"] == "light"
            )
            processing_ok = result["compression_ratio"].is_monotonic_increasing
        except Exception:
            pass

    base_ok = (
        len(result) == len(source)
        and "model" in result.columns
    )

    return {
        "Структура результата": structure_ok,
        "Интеграция изменений": integration_ok,
        "Базовое поведение": base_ok,
        "Обработка benchmark-данных": processing_ok,
    }


BASE_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result = result.sort_values("compression_ratio")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_A_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["compression_ratio"] = (\n        result["compression_ratio"] * 100\n    )\n    result = result.sort_values("compression_ratio")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_B_CODE = 'import numpy as np\nimport pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["compression_class"] = np.select(\n        [\n            result["compression_ratio"] < 0.3,\n            result["compression_ratio"] < 0.6,\n        ],\n        ["strong", "balanced"],\n        default="light",\n    )\n    result = result.sort_values("compression_ratio")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'


VARIANT = {
    "id": 11,
    "name": NAME,
    "requirements": EXTRA_REQUIREMENTS,
    "data_columns": DATA_COLUMNS,
    "data_rows": DATA_ROWS,
    "base_code": BASE_CODE,
    "branch_a_code": BRANCH_A_CODE,
    "branch_b_code": BRANCH_B_CODE,
    "test_data": make_test_data,
    "check": check,
}
