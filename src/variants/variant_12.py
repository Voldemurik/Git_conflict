"""Variant 12: Translation Benchmark."""

NAME = 'Translation Benchmark'
EXTRA_REQUIREMENTS = ["numpy"]

DATA_COLUMNS = ['model', 'quality_score', 'latency_ms']

DATA_ROWS = [['Nova-7B', 0.86, 1800], ['Sigma-8B', 0.72, 2300], ['Atlas-Agent', 0.94, 5600], ['Orion-13B', 0.63, 3900], ['Boundary80', 0.8, 2100], ['Near80', 0.799, 2000], ['MiniTrans', 0.55, 900], ['ProTrans', 0.91, 4300], ['FastTrans', 0.81, 700], ['WeakTrans', 0.42, 1600]]


def make_test_data():
    import pandas as pd

    return pd.DataFrame(
        DATA_ROWS,
        columns=DATA_COLUMNS,
    )


def check(result, source):
    structure_ok = "review_status" in result.columns
    integration_ok = False
    processing_ok = False
    if structure_ok:
        try:
            v = result.set_index("model")
            integration_ok = (
                v.loc["Nova-7B", "quality_score"] == 86
                and v.loc["Boundary80", "review_status"] == "accepted"
                and v.loc["Near80", "review_status"] == "review"
            )
            processing_ok = result["quality_score"].is_monotonic_decreasing
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


BASE_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result = result.sort_values("quality_score", ascending=False)\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_A_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["quality_score"] = result["quality_score"] * 100\n    result = result.sort_values("quality_score", ascending=False)\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_B_CODE = 'import numpy as np\nimport pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["review_status"] = np.where(\n        result["quality_score"] >= 0.8,\n        "accepted",\n        "review",\n    )\n    result = result.sort_values("quality_score", ascending=False)\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'


VARIANT = {
    "id": 12,
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
