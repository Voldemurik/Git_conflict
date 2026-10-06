"""Variant 03: Token Usage Benchmark."""

NAME = 'Token Usage Benchmark'
EXTRA_REQUIREMENTS = ["numpy"]

DATA_COLUMNS = ['model', 'input_tokens', 'output_tokens', 'latency_ms']

DATA_ROWS = [['Nova-7B', 1200, 410, 1850], ['Sigma-8B', 900, 280, 2400], ['Atlas-Agent', 3500, 920, 7600], ['Orion-13B', 1800, 650, 4200], ['Mini-2B', 400, 120, 700], ['LongCtx-X', 7200, 1800, 9500], ['Coder-M', 2200, 1100, 3100], ['Reasoner-S', 1500, 1500, 5400], ['Rapid-1B', 300, 90, 300], ['Research-L', 5000, 2500, 12200]]


def make_test_data():
    import pandas as pd

    return pd.DataFrame(
        DATA_ROWS,
        columns=DATA_COLUMNS,
    )


def check(result, source):
    structure_ok = (
        "total_tokens" in result.columns
        and "tokens_per_second" in result.columns
        and "input_tokens" not in result.columns
        and "output_tokens" not in result.columns
    )
    integration_ok = False
    processing_ok = False
    if structure_ok:
        try:
            v = result.set_index("model")
            integration_ok = (
                v.loc["Nova-7B", "total_tokens"] == 1610
                and abs(v.loc["Nova-7B", "tokens_per_second"] - 870.27) < 0.01
                and v.loc["Research-L", "total_tokens"] == 7500
            )
            processing_ok = result["total_tokens"].is_monotonic_increasing
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


BASE_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result = result.sort_values("input_tokens")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_A_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result = result.rename(\n        columns={\n            "input_tokens": "prompt_tokens",\n            "output_tokens": "completion_tokens",\n        }\n    )\n    result["total_tokens"] = (\n        result["prompt_tokens"] + result["completion_tokens"]\n    )\n    result = result.drop(\n        columns=["prompt_tokens", "completion_tokens"]\n    )\n    result = result.sort_values("total_tokens")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_B_CODE = 'import numpy as np\nimport pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["tokens_per_second"] = np.round(\n        (result["input_tokens"] + result["output_tokens"])\n        / (result["latency_ms"] / 1000),\n        2,\n    )\n    result = result.sort_values("input_tokens")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'


VARIANT = {
    "id": 3,
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
