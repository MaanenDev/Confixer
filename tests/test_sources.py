import pytest
import yaml
import json
from confixer.sources.base import ConfigSource
from confixer.sources.yaml_source import YamlSource
from confixer.sources.json_source import JsonSource


class DummySource(ConfigSource):
    def load(self):
        return {"a": 1, "b": {"c": 2}}


def test_dummy_source_load():
    source = DummySource()
    data = source.load()
    assert data["a"] == 1
    assert data["b"]["c"] == 2


def test_load_valid_yaml(tmp_path):
    data = {"key": "value", "nested": {"a": 1}}
    file_path = tmp_path / "config.yaml"
    file_path.write_text(yaml.dump(data), encoding="utf-8")

    source = YamlSource(str(file_path))
    loaded = source.load()
    assert loaded == data


def test_load_invalid_yaml(tmp_path):
    invalid_yaml = "key: value\n: invalid"
    file_path = tmp_path / "invalid.yaml"
    file_path.write_text(invalid_yaml, encoding="utf-8")

    source = YamlSource(str(file_path))
    with pytest.raises(yaml.YAMLError):
        source.load()


def test_load_non_dict_root(tmp_path):
    yaml_data = ["item1", "item2"]
    file_path = tmp_path / "list_root.yaml"
    file_path.write_text(yaml.dump(yaml_data), encoding="utf-8")

    source = YamlSource(str(file_path))
    with pytest.raises(ValueError, match="YAML root must be a dict"):
        source.load()


def test_load_empty_yaml(tmp_path):
    file_path = tmp_path / "empty.yaml"
    file_path.write_text("", encoding="utf-8")

    source = YamlSource(str(file_path))
    with pytest.raises(ValueError, match="YAML root must be a dict"):
        source.load()


def test_load_valid_json(tmp_path):
    data = {"key": "value", "nested": {"a": 1}}
    file_path = tmp_path / "config.json"
    file_path.write_text(json.dumps(data), encoding="utf-8")

    source = JsonSource(str(file_path))
    loaded = source.load()
    assert loaded == data


def test_load_invalid_json(tmp_path):
    invalid_json = '{"key": "value", invalid}'
    file_path = tmp_path / "invalid.json"
    file_path.write_text(invalid_json, encoding="utf-8")

    source = JsonSource(str(file_path))
    with pytest.raises(json.JSONDecodeError):
        source.load()


def test_load_non_dict_root_json(tmp_path):
    json_data = ["item1", "item2"]  # list instead of dict
    file_path = tmp_path / "list_root.json"
    file_path.write_text(json.dumps(json_data), encoding="utf-8")

    source = JsonSource(str(file_path))
    with pytest.raises(ValueError, match="JSON root must be a dict"):
        source.load()


def test_load_empty_json(tmp_path):
    file_path = tmp_path / "empty.json"
    file_path.write_text("", encoding="utf-8")  # empty file

    source = JsonSource(str(file_path))
    with pytest.raises(json.JSONDecodeError):
        source.load()
