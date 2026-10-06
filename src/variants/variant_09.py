"""Variant 09: Agent Planning Benchmark."""

NAME = 'Agent Planning Benchmark'
EXTRA_REQUIREMENTS = ["numpy"]

DATA_COLUMNS = ['model', 'plan_steps', 'replans', 'success_score']

DATA_ROWS = [['Nova-Agent', 5, 1, 0.8], ['Sigma-Agent', 8, 2, 0.72], ['Atlas-Agent', 12, 1, 0.94], ['Orion-Agent', 10, 3, 0.76], ['Tiny-Planner', 2, 0, 0.61], ['Retry-Planner', 6, 5, 0.68], ['Deep-Planner', 18, 2, 0.9], ['Stable-Planner', 7, 0, 0.85], ['Chaotic-Planner', 9, 7, 0.55], ['Research-Planner', 14, 3, 0.88]]


def make_test_data():
    import pandas as pd

    return pd.DataFrame(
        DATA_ROWS,
        columns=DATA_COLUMNS,
    )


def check(result, source):
    structure_ok = (
        "planning_actions" in result.columns
        and "planning_efficiency" in result.columns
        and "plan_steps" not in result.columns
        and "replans" not in result.columns
    )
    integration_ok = False
    processing_ok = False
    if structure_ok:
        try:
            v = result.set_index("model")
            integration_ok = (
                v.loc["Nova-Agent", "planning_actions"] == 6
                and abs(v.loc["Nova-Agent", "planning_efficiency"] - 0.1143) < 0.0001
                and v.loc["Chaotic-Planner", "planning_actions"] == 16
            )
            processing_ok = result["planning_actions"].is_monotonic_increasing
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


BASE_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result = result.sort_values("plan_steps")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_A_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["planning_actions"] = (\n        result["plan_steps"] + result["replans"]\n    )\n    result = result.drop(columns=["plan_steps", "replans"])\n    result = result.sort_values("planning_actions")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_B_CODE = 'import numpy as np\nimport pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["planning_efficiency"] = np.round(\n        result["success_score"]\n        / (1 + result["plan_steps"] + result["replans"]),\n        4,\n    )\n    result = result.sort_values("plan_steps")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'


VARIANT = {
    "id": 9,
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
