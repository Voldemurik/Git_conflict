import numpy as np
import pandas as pd


DATA_COLUMNS = ['model', 'context_tokens', 'answer_tokens']

DATA_ROWS = [['Nova-7B', 8000, 500],
            ['Sigma-8B', 16000, 700],
            ['Atlas-Agent', 64000, 1200],
            ['Orion-13B', 32000, 900],
            ['MiniCtx', 4000, 250],
            ['Border16', 15999, 600],
            ['Border48', 48000, 1000],
            ['Long128', 128000, 1800],
            ['Medium24', 24000, 750],
            ['TinyCtx', 2000, 150]]
def prepare_benchmark(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["context_k"] = result["context_tokens"] / 1000
    result["context_class"] = np.select(
        [
            result["context_k"] < 16,
            result["context_k"] < 48,
        ],
        ["short", "medium"],
        default="long",
    )
    result = result.drop(columns=["context_tokens"])
    result = result.sort_values("context_k").reset_index(drop=True)
    return result


if __name__ == "__main__":
    data = pd.read_csv("data/benchmark.csv")
    print(prepare_benchmark(data))
