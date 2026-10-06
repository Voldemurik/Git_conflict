"""Variant 05: Agent Tool-Use Benchmark."""

NAME = 'Agent Tool-Use Benchmark'
EXTRA_REQUIREMENTS = ["numpy"]

DATA_COLUMNS = ['model', 'tool_calls', 'failed_calls', 'success_score']

DATA_ROWS = [['Atlas-Agent', 5, 1, 0.92], ['Nova-Agent', 3, 0, 0.8], ['Orion-Agent', 8, 2, 0.74], ['Sigma-Agent', 2, 1, 0.67], ['ToolMaster', 12, 1, 0.95], ['Minimal-Agent', 1, 0, 0.55], ['Retry-Agent', 4, 4, 0.62], ['Research-Agent', 10, 3, 0.89], ['Planner-Agent', 6, 0, 0.83], ['Broken-Agent', 5, 5, 0.31]]


def make_test_data():
    import pandas as pd

    return pd.DataFrame(
        DATA_ROWS,
        columns=DATA_COLUMNS,
    )


def check(result, source):
    structure_ok = (
        "interactions" in result.columns
        and "agent_efficiency" in result.columns
        and "tool_calls" not in result.columns
        and "failed_calls" not in result.columns
    )
    integration_ok = False
    processing_ok = False
    if structure_ok:
        try:
            v = result.set_index("model")
            integration_ok = (
                v.loc["Atlas-Agent", "interactions"] == 6
                and abs(v.loc["Atlas-Agent", "agent_efficiency"] - 0.1314) < 0.0001
                and v.loc["Broken-Agent", "interactions"] == 10
            )
            processing_ok = result["interactions"].is_monotonic_increasing
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


BASE_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result = result.sort_values("tool_calls")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_A_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["interactions"] = (\n        result["tool_calls"] + result["failed_calls"]\n    )\n    result = result.drop(columns=["tool_calls", "failed_calls"])\n    result = result.sort_values("interactions")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_B_CODE = 'import numpy as np\nimport pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["agent_efficiency"] = np.round(\n        result["success_score"]\n        / (1 + result["tool_calls"] + result["failed_calls"]),\n        4,\n    )\n    result = result.sort_values("tool_calls")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'


VARIANT = {
    "id": 5,
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
