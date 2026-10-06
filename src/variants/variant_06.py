"""Variant 06: Function Calling Benchmark."""

NAME = 'Function Calling Benchmark'
EXTRA_REQUIREMENTS = ["numpy"]

DATA_COLUMNS = ['model', 'calls', 'valid_calls']

DATA_ROWS = [['Nova-7B', 10, 9], ['Sigma-8B', 10, 7], ['Atlas-Agent', 20, 19], ['Orion-13B', 12, 6], ['Boundary80', 10, 8], ['PerfectCall', 8, 8], ['WeakCall', 9, 3], ['ToolCoder', 15, 12], ['ResearchCall', 25, 21], ['MiniCall', 4, 3]]


def make_test_data():
    import pandas as pd

    return pd.DataFrame(
        DATA_ROWS,
        columns=DATA_COLUMNS,
    )


def check(result, source):
    structure_ok = (
        "validity_rate" in result.columns
        and "reliability" in result.columns
        and "calls" not in result.columns
        and "valid_calls" not in result.columns
    )
    integration_ok = False
    processing_ok = False
    if structure_ok:
        try:
            v = result.set_index("model")
            integration_ok = (
                v.loc["Nova-7B", "validity_rate"] == 90
                and v.loc["Boundary80", "reliability"] == "reliable"
                and v.loc["Sigma-8B", "reliability"] == "unstable"
            )
            processing_ok = result["validity_rate"].is_monotonic_decreasing
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


BASE_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result = result.sort_values("valid_calls", ascending=False)\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_A_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["validity_rate"] = (\n        result["valid_calls"] / result["calls"] * 100\n    )\n    result = result.drop(columns=["valid_calls", "calls"])\n    result = result.sort_values("validity_rate", ascending=False)\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_B_CODE = 'import numpy as np\nimport pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["reliability"] = np.where(\n        result["valid_calls"] / result["calls"] >= 0.8,\n        "reliable",\n        "unstable",\n    )\n    result = result.sort_values("valid_calls", ascending=False)\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'


VARIANT = {
    "id": 6,
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
