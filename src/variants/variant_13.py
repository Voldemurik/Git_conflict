"""Variant 13: Multi-Agent Coordination Benchmark."""

NAME = 'Multi-Agent Coordination Benchmark'
EXTRA_REQUIREMENTS = ["numpy"]

DATA_COLUMNS = ['model', 'messages', 'handoffs', 'success_score']

DATA_ROWS = [['Swarm-A', 20, 3, 0.84], ['Swarm-B', 30, 8, 0.75], ['Swarm-C', 18, 2, 0.91], ['Swarm-D', 25, 6, 0.79], ['Tiny-Swarm', 8, 1, 0.62], ['Handoff-Pro', 22, 10, 0.88], ['Silent-Team', 12, 0, 0.73], ['Research-Swarm', 40, 7, 0.93], ['Chaotic-Team', 35, 15, 0.58], ['Compact-Team', 10, 2, 0.81]]


def make_test_data():
    import pandas as pd

    return pd.DataFrame(
        DATA_ROWS,
        columns=DATA_COLUMNS,
    )


def check(result, source):
    structure_ok = (
        "interactions" in result.columns
        and "coordination_score" in result.columns
        and "messages" not in result.columns
        and "handoffs" not in result.columns
    )
    integration_ok = False
    processing_ok = False
    if structure_ok:
        try:
            v = result.set_index("model")
            integration_ok = (
                v.loc["Swarm-C", "interactions"] == 20
                and v.loc["Research-Swarm", "interactions"] == 47
                and v.loc["Swarm-C", "coordination_score"] > 0
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


BASE_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result = result.sort_values("messages")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_A_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["interactions"] = (\n        result["messages"] + result["handoffs"]\n    )\n    result = result.drop(columns=["messages", "handoffs"])\n    result = result.sort_values("interactions")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_B_CODE = 'import numpy as np\nimport pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["coordination_score"] = np.round(\n        result["success_score"]\n        / (1 + result["messages"] + result["handoffs"]),\n        4,\n    )\n    result = result.sort_values("messages")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'


VARIANT = {
    "id": 13,
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
