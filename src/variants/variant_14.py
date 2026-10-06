"""Variant 14: LLM Safety Benchmark."""

NAME = 'LLM Safety Benchmark'
EXTRA_REQUIREMENTS = ["numpy"]

DATA_COLUMNS = ['model', 'safe', 'judge_score']

DATA_ROWS = [['Nova-7B', True, 0.88], ['Sigma-8B', False, 0.71], ['Atlas-Agent', True, 0.93], ['Orion-13B', False, 0.69], ['SafeMini', True, 0.61], ['Risky-X', False, 0.9], ['Guard-Pro', True, 0.97], ['BorderSafe', True, 0.5], ['BorderUnsafe', False, 0.5], ['ResearchGuard', True, 0.85]]


def make_test_data():
    import pandas as pd

    return pd.DataFrame(
        DATA_ROWS,
        columns=DATA_COLUMNS,
    )


def check(result, source):
    structure_ok = (
        "status" in result.columns
        and "needs_review" in result.columns
        and "safe" not in result.columns
    )
    integration_ok = False
    processing_ok = False
    if structure_ok:
        try:
            v = result.set_index("model")
            integration_ok = (
                v.loc["Nova-7B", "status"] == "safe"
                and bool(v.loc["Nova-7B", "needs_review"]) is False
                and v.loc["Risky-X", "status"] == "unsafe"
                and bool(v.loc["Risky-X", "needs_review"]) is True
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
BRANCH_A_CODE = 'import numpy as np\nimport pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["status"] = np.where(\n        result["safe"],\n        "safe",\n        "unsafe",\n    )\n    result = result.drop(columns=["safe"])\n    result = result.sort_values("judge_score", ascending=False)\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_B_CODE = 'import numpy as np\nimport pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["needs_review"] = np.logical_not(result["safe"])\n    result = result.sort_values("judge_score", ascending=False)\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'


VARIANT = {
    "id": 14,
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
