"""Variant 04: LLM Cost Benchmark."""

NAME = 'LLM Cost Benchmark'
EXTRA_REQUIREMENTS = ["numpy"]

DATA_COLUMNS = ['model', 'cost_usd', 'total_tokens']

DATA_ROWS = [['Nova-7B', 0.014, 1610], ['Sigma-8B', 0.008, 1180], ['Atlas-Agent', 0.083, 4420], ['Orion-13B', 0.041, 2450], ['Mini-2B', 0.003, 700], ['Research-L', 0.12, 6900], ['Coder-M', 0.019, 2600], ['BorderCheap', 0.02, 2000], ['BorderNormal', 0.06, 3200], ['Reasoner-X', 0.059, 4800]]


def make_test_data():
    import pandas as pd

    return pd.DataFrame(
        DATA_ROWS,
        columns=DATA_COLUMNS,
    )


def check(result, source):
    structure_ok = (
        "cost_per_1k_tokens" in result.columns
        and "cost_class" in result.columns
        and "cost_usd" not in result.columns
    )
    integration_ok = False
    processing_ok = False
    if structure_ok:
        try:
            v = result.set_index("model")
            integration_ok = (
                v.loc["Nova-7B", "cost_class"] == "cheap"
                and v.loc["BorderCheap", "cost_class"] == "normal"
                and v.loc["BorderNormal", "cost_class"] == "expensive"
                and v.loc["Atlas-Agent", "cost_per_1k_tokens"] > 0
            )
            processing_ok = result["cost_per_1k_tokens"].is_monotonic_increasing
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


BASE_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result = result.sort_values("cost_usd")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_A_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["cost_per_1k_tokens"] = (\n        result["cost_usd"] / result["total_tokens"] * 1000\n    )\n    result = result.drop(columns=["cost_usd"])\n    result = result.sort_values("cost_per_1k_tokens")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_B_CODE = 'import numpy as np\nimport pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["cost_class"] = np.select(\n        [\n            result["cost_usd"] < 0.02,\n            result["cost_usd"] < 0.06,\n        ],\n        ["cheap", "normal"],\n        default="expensive",\n    )\n    result = result.sort_values("cost_usd")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'


VARIANT = {
    "id": 4,
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
