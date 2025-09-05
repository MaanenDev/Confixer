from confixer.sources.base import ConfigSource


class DummySource(ConfigSource):
    def load(self):
        return {"a": 1, "b": {"c": 2}}


def test_dummy_source_load():
    source = DummySource()
    data = source.load()
    assert data["a"] == 1
    assert data["b"]["c"] == 2
