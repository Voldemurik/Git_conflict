import importlib


VARIANT_IDS = tuple(range(1, 16))


def get_variant(variant_id: int):
    if variant_id not in VARIANT_IDS:
        raise ValueError(
            f"Unknown variant: {variant_id}"
        )

    module = importlib.import_module(
        f"variants.variant_{variant_id:02d}"
    )

    return module.VARIANT