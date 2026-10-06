"""Variant 01: LLM Latency Benchmark."""

NAME = 'LLM Latency Benchmark'
EXTRA_REQUIREMENTS = ["numpy"]

DATA_COLUMNS = ['model', 'latency_ms', 'judge_score']

DATA_ROWS = [['Nova-7B', 1850, 0.82], ['Sigma-8B', 2400, 0.76], ['BorderModel', 3000, 0.8], ['Orion-13B', 4200, 0.91], ['Atlas-Agent', 7600, 0.88], ['MiniLM-Agent', 950, 0.69], ['Titan-20B', 12500, 0.94], ['Edge-3B', 2999, 0.71], ['SlowCoder', 3001, 0.84], ['Rapid-1B', 420, 0.58]]


def make_test_data():
    import pandas as pd

    return pd.DataFrame(
        DATA_ROWS,
        columns=DATA_COLUMNS,
    )


def check(result, source):
    structure_ok = (
        "latency_sec" in result.columns
        and "speed_class" in result.columns
        and "latency_ms" not in result.columns
    )
    integration_ok = False
    processing_ok = False
    if structure_ok:
        try:
            v = result.set_index("model")
            integration_ok = (
                v.loc["Nova-7B", "latency_sec"] == 1.85
                and v.loc["Edge-3B", "speed_class"] == "fast"
                and v.loc["BorderModel", "speed_class"] == "slow"
                and v.loc["SlowCoder", "speed_class"] == "slow"
            )
            processing_ok = result["latency_sec"].is_monotonic_increasing
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


BASE_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result = result.sort_values("latency_ms")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_A_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["latency_sec"] = result["latency_ms"] / 1000\n    result = result.drop(columns=["latency_ms"])\n    result = result.sort_values("latency_sec")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_B_CODE = 'import numpy as np\nimport pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["speed_class"] = np.where(\n        result["latency_ms"] < 3000,\n        "fast",\n        "slow",\n    )\n    result = result.sort_values("latency_ms")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'


VARIANT = {
    "id": 1,
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
