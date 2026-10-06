"""Variant 08: Long-Context Benchmark."""

NAME = 'Long-Context Benchmark'
EXTRA_REQUIREMENTS = ["numpy"]

DATA_COLUMNS = ['model', 'context_tokens', 'answer_tokens']

DATA_ROWS = [['Nova-7B', 8000, 500], ['Sigma-8B', 16000, 700], ['Atlas-Agent', 64000, 1200], ['Orion-13B', 32000, 900], ['MiniCtx', 4000, 250], ['Border16', 15999, 600], ['Border48', 48000, 1000], ['Long128', 128000, 1800], ['Medium24', 24000, 750], ['TinyCtx', 2000, 150]]


def make_test_data():
    import pandas as pd

    return pd.DataFrame(
        DATA_ROWS,
        columns=DATA_COLUMNS,
    )


def check(result, source):
    structure_ok = (
        "context_k" in result.columns
        and "context_class" in result.columns
        and "context_tokens" not in result.columns
    )
    integration_ok = False
    processing_ok = False
    if structure_ok:
        try:
            v = result.set_index("model")
            integration_ok = (
                v.loc["Nova-7B", "context_k"] == 8
                and v.loc["Border16", "context_class"] == "short"
                and v.loc["Sigma-8B", "context_class"] == "medium"
                and v.loc["Border48", "context_class"] == "long"
            )
            processing_ok = result["context_k"].is_monotonic_increasing
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


BASE_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result = result.sort_values("context_tokens")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_A_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["context_k"] = result["context_tokens"] / 1000\n    result = result.drop(columns=["context_tokens"])\n    result = result.sort_values("context_k")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_B_CODE = 'import numpy as np\nimport pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["context_class"] = np.select(\n        [\n            result["context_tokens"] < 16000,\n            result["context_tokens"] < 48000,\n        ],\n        ["short", "medium"],\n        default="long",\n    )\n    result = result.sort_values("context_tokens")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'


VARIANT = {
    "id": 8,
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
