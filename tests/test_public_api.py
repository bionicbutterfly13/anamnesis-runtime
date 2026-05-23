import anamnesis_runtime


def test_public_exports_resolve() -> None:
    for name in anamnesis_runtime.__all__:
        assert getattr(anamnesis_runtime, name)


def test_public_description_mentions_runtime() -> None:
    assert "memory runtime" in (anamnesis_runtime.__doc__ or "")

