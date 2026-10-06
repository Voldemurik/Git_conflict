"""Variant 07: RAG Retrieval Benchmark."""

NAME = 'RAG Retrieval Benchmark'
EXTRA_REQUIREMENTS = ["numpy"]

DATA_COLUMNS = ['model', 'retrieved_chunks', 'relevant_chunks', 'context_tokens']

DATA_ROWS = [['Nova-RAG', 10, 8, 2400], ['Sigma-RAG', 8, 4, 1800], ['Atlas-RAG', 20, 18, 5200], ['Orion-RAG', 12, 7, 3000], ['Perfect-RAG', 6, 6, 1500], ['Noisy-RAG', 18, 3, 4600], ['Mini-RAG', 4, 3, 900], ['Long-RAG', 30, 24, 12000], ['Sparse-RAG', 5, 1, 2200], ['Balanced-RAG', 16, 12, 4000]]


def make_test_data():
    import pandas as pd

    return pd.DataFrame(
        DATA_ROWS,
        columns=DATA_COLUMNS,
    )


def check(result, source):
    structure_ok = (
        "retrieval_precision" in result.columns
        and "retrieval_load" in result.columns
        and "retrieved_chunks" not in result.columns
        and "relevant_chunks" not in result.columns
    )
    integration_ok = False
    processing_ok = False
    if structure_ok:
        try:
            v = result.set_index("model")
            integration_ok = (
                abs(v.loc["Nova-RAG", "retrieval_precision"] - 0.8) < 1e-9
                and v.loc["Perfect-RAG", "retrieval_precision"] == 1.0
                and v.loc["Nova-RAG", "retrieval_load"] > 0
            )
            processing_ok = result["retrieval_precision"].is_monotonic_decreasing
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


BASE_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result = result.sort_values("retrieved_chunks")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_A_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["retrieval_precision"] = (\n        result["relevant_chunks"] / result["retrieved_chunks"]\n    )\n    result = result.drop(\n        columns=["retrieved_chunks", "relevant_chunks"]\n    )\n    result = result.sort_values(\n        "retrieval_precision",\n        ascending=False,\n    )\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_B_CODE = 'import numpy as np\nimport pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["retrieval_load"] = np.round(\n        result["retrieved_chunks"] / result["context_tokens"] * 1000,\n        2,\n    )\n    result = result.sort_values("retrieved_chunks")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'


VARIANT = {
    "id": 7,
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
