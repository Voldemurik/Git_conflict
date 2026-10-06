"""Variant 15: Coding Benchmark."""

NAME = 'Coding Benchmark'
EXTRA_REQUIREMENTS = ["numpy"]

DATA_COLUMNS = ['model', 'passed_tests', 'total_tests', 'runtime_ms']

DATA_ROWS = [['Nova-7B', 8, 10, 1800], ['Sigma-8B', 6, 10, 2300], ['Atlas-Agent', 19, 20, 5100], ['Orion-13B', 7, 12, 3900], ['Boundary80', 4, 5, 1200], ['Near80', 79, 100, 8900], ['PerfectCoder', 20, 20, 4200], ['WeakCoder', 2, 10, 1600], ['FastCoder', 9, 10, 600], ['ResearchCoder', 17, 20, 7200]]


def make_test_data():
    import pandas as pd

    return pd.DataFrame(
        DATA_ROWS,
        columns=DATA_COLUMNS,
    )


def check(result, source):
    structure_ok = (
        "pass_rate" in result.columns
        and "solution_class" in result.columns
        and "passed_tests" not in result.columns
        and "total_tests" not in result.columns
    )
    integration_ok = False
    processing_ok = False
    if structure_ok:
        try:
            v = result.set_index("model")
            integration_ok = (
                v.loc["Nova-7B", "pass_rate"] == 80
                and v.loc["Boundary80", "solution_class"] == "strong"
                and v.loc["Near80", "solution_class"] == "weak"
            )
            processing_ok = result["pass_rate"].is_monotonic_decreasing
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


BASE_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result = result.sort_values("passed_tests", ascending=False)\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_A_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["pass_rate"] = (\n        result["passed_tests"] / result["total_tests"] * 100\n    )\n    result = result.drop(columns=["passed_tests", "total_tests"])\n    result = result.sort_values("pass_rate", ascending=False)\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_B_CODE = 'import numpy as np\nimport pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["solution_class"] = np.where(\n        result["passed_tests"] / result["total_tests"] >= 0.8,\n        "strong",\n        "weak",\n    )\n    result = result.sort_values("passed_tests", ascending=False)\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'


VARIANT = {
    "id": 15,
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
