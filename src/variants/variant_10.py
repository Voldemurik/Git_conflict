"""Variant 10: Web Research Benchmark."""

NAME = 'Web Research Benchmark'
EXTRA_REQUIREMENTS = ["numpy"]

DATA_COLUMNS = ['model', 'sources', 'valid_citations', 'judge_score']

DATA_ROWS = [['Nova-Agent', 6, 5, 0.82], ['Sigma-Agent', 4, 2, 0.71], ['Atlas-Agent', 10, 9, 0.94], ['Orion-Agent', 8, 5, 0.77], ['Tiny-Research', 2, 1, 0.6], ['CitationPro', 12, 12, 0.96], ['SourceFlood', 20, 8, 0.69], ['Balanced-Web', 9, 7, 0.84], ['Sparse-Web', 3, 1, 0.58], ['Deep-Web', 15, 13, 0.91]]


def make_test_data():
    import pandas as pd

    return pd.DataFrame(
        DATA_ROWS,
        columns=DATA_COLUMNS,
    )


def check(result, source):
    structure_ok = (
        "evidence_count" in result.columns
        and "evidence_quality" in result.columns
        and "sources" not in result.columns
        and "valid_citations" not in result.columns
    )
    integration_ok = False
    processing_ok = False
    if structure_ok:
        try:
            v = result.set_index("model")
            integration_ok = (
                v.loc["Nova-Agent", "evidence_count"] == 11
                and v.loc["CitationPro", "evidence_count"] == 24
                and v.loc["CitationPro", "evidence_quality"] > 0.9
            )
            processing_ok = result["evidence_count"].is_monotonic_increasing
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


BASE_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result = result.sort_values("sources")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_A_CODE = 'import pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["evidence_count"] = (\n        result["sources"] + result["valid_citations"]\n    )\n    result = result.drop(columns=["sources", "valid_citations"])\n    result = result.sort_values("evidence_count")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'
BRANCH_B_CODE = 'import numpy as np\nimport pandas as pd\n\n\ndef prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:\n    result = df.copy()\n\n    result["evidence_quality"] = np.round(\n        result["valid_citations"] / result["sources"]\n        * result["judge_score"],\n        3,\n    )\n    result = result.sort_values("sources")\n\n    return result\n\n\nif __name__ == "__main__":\n    data = pd.read_csv("data/benchmark.csv")\n    print(prepare_benchmark(data))\n'


VARIANT = {
    "id": 10,
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
