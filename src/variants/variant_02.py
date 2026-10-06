"""Variant 02: LLM Quality Benchmark."""

NAME = 'LLM Quality Benchmark'
EXTRA_REQUIREMENTS = ["numpy"]

DATA_COLUMNS = ['model', 'judge_score', 'latency_ms']

DATA_ROWS = [['Nova-7B', 0.82, 1850], ['Sigma-8B', 0.68, 2400], ['Atlas-Agent', 0.93, 7600], ['Orion-13B', 0.74, 4200], ['Edge-3B', 0.7, 1500], ['Border-High', 0.9, 3100], ['Mini-2B', 0.51, 900], ['Reasoner-X', 0.89, 6800], ['Coder-M', 0.71, 2200], ['Research-L', 0.97, 9800]]


def make_test_data():
    import pandas as pd

    return pd.DataFrame(
        DATA_ROWS,
        columns=DATA_COLUMNS,
    )


def check(result, source):
    structure_ok = "quality_class" in result.columns
    integration_ok = False
    processing_ok = False
    if structure_ok:
        try:
            v = result.set_index("model")
            integration_ok = (
                v.loc["Atlas-Agent", "judge_score"] == 93
                and v.loc["Border-High", "quality_class"] == "high"
                and v.loc["Edge-3B", "quality_class"] == "medium"
                and v.loc["Sigma-8B", "quality_class"] == "low"
            )
            processing_ok = result["judge_score"].is_monotonic_decreasing
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


BASE_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result = result.sort_values("judge_score", ascending=False)\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_A_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["judge_score"] = result["judge_score"] * 100\n    result = result.sort_values("judge_score", ascending=False)\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_B_CODE = 'import numpy as np\nimport pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["quality_class"] = np.select(\n        [\n            result["judge_score"] >= 0.9,\n            result["judge_score"] >= 0.7,\n        ],\n        ["high", "medium"],\n        default="low",\n    )\n    result = result.sort_values("judge_score", ascending=False)\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'


VARIANT = {
    "id": 2,
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
