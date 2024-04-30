from .entity import BaseEntity


def label(entity: BaseEntity) -> str:
    if hasattr(entity, "__label__"):
        label_fn = getattr(entity, "__label__")
        if callable(label_fn):
            label = label_fn()
            if isinstance(label, str):
                return label

            raise ValueError(
                f"Invalid label value: {label}. return type of __label__ should be an str. "
                f"'{type(label)}' returned instead."
            )

    attrs_list = [
        ("name",),
        ("full_name",),
        ("fullname",),
        ("label",),
        ("value",),
        ("first_name", "last_name"),
        ("short_description",),
    ]

    for attrs in attrs_list:
        if not all(hasattr(entity, attr) for attr in attrs):
            continue

        values = [getattr(entity, attr) for attr in attrs]
        if all(isinstance(value, str) for value in values):
            return " ".join(values)

    raise NotImplementedError(
        f"Label value cannot be resolved automatically, "
        f"please implement __label__ method on {entity.__class__.__name__} entity."
    )
