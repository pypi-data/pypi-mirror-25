#!/usr/bin/env python
# -*- coding: utf-8
import pytest
import six
from k8s import config
from k8s.base import Model
from k8s.client import Client
from k8s.fields import Field, ReadOnlyField, OnceField, ListField, RequiredField
from k8s.models.common import ObjectMeta
from mock import create_autospec
from requests import Response


class ModelTest(Model):
    class Meta:
        pass

    metadata = Field(ObjectMeta)
    field = Field(int)
    list_field = ListField(int)
    once_field = OnceField(int)
    read_only_field = ReadOnlyField(int)
    alt_type_field = Field(int, alt_type=six.text_type)
    dict_field = Field(dict)
    _exec = Field(int)


class TestFields(object):
    @pytest.fixture(autouse=True)
    def set_config_debug(self, monkeypatch):
        monkeypatch.setattr(config, "debug", True)

    @pytest.mark.parametrize("field_name,initial_value,other_value", (
            ("field", 1, 2),
            ("list_field", [1], [1, 2]),
            ("once_field", 1, 2),
            ("_exec", 1, 2)
    ))
    def test_field_new(self, field_name, initial_value, other_value):
        kwargs = {"new": True, field_name: initial_value}
        model = ModelTest(**kwargs)
        assert getattr(model, field_name) == initial_value
        setattr(model, field_name, other_value)
        assert getattr(model, field_name) == other_value

    @pytest.mark.parametrize("field_name,initial_value,other_value", (
            ("field", 1, 2),
            ("list_field", [1], [1, 2]),
    ))
    def test_field_old(self, field_name, initial_value, other_value):
        model = ModelTest.from_dict({field_name: initial_value})
        assert getattr(model, field_name) == initial_value
        setattr(model, field_name, other_value)
        assert getattr(model, field_name) == other_value

    def test_once_field_old(self):
        model = ModelTest.from_dict({"once_field": 1})
        assert model.once_field == 1
        model.once_field = 2
        assert model.once_field == 1

    def test_exec_field_old(self):
        model = ModelTest.from_dict({"exec": 1})
        assert model._exec == 1
        model._exec = 2
        assert model._exec == 2
        assert model.as_dict()[u"exec"] == 2

    def test_read_only_field_new(self):
        model = ModelTest(new=True, read_only_field=1)
        assert model.read_only_field is None
        model.read_only_field = 2
        assert model.read_only_field is None

    def test_read_only_field_old(self):
        model = ModelTest.from_dict({"read_only_field": 1})
        assert model.read_only_field == 1
        model.read_only_field = 2
        assert model.read_only_field == 1

    @pytest.mark.parametrize("value,modifier", [
        (1, lambda x: x + 1),
        (u"string", lambda x: x.upper())
    ])
    def test_alt_type_field(self, value, modifier):
        model = ModelTest.from_dict({"alt_type_field": value})
        assert model.alt_type_field == value
        assert model.as_dict()[u"alt_type_field"] == value
        model.alt_type_field = modifier(value)
        assert model.alt_type_field == modifier(value)


class RequiredFieldTest(Model):
    required_field = RequiredField(int)
    field = Field(int, 100)


@pytest.mark.usefixtures("logger")
class TestRequiredField(object):
    @pytest.mark.parametrize("kwargs", [
        {"required_field": 1, "field": 2},
        {"required_field": 1},
    ])
    def test_create_with_fields(self, kwargs):
        instance = RequiredFieldTest(new=True, **kwargs)
        for key, value in kwargs.items():
            assert getattr(instance, key) == value

    def test_create_fails_when_field_missing(self):
        with pytest.raises(TypeError):
            RequiredFieldTest(new=True, field=1)


@pytest.mark.usefixtures("logger")
class TestModel(object):
    @pytest.fixture()
    def mock_response(self, monkeypatch):
        mock_client = create_autospec(Client)
        mock_response = create_autospec(Response)
        monkeypatch.setattr(ModelTest, "_client", mock_client)
        mock_client.get.return_value = mock_response
        return mock_response

    def test_unexpected_kwargs(self):
        with pytest.raises(TypeError):
            ModelTest(unknown=3)

    def test_change(self, mock_response):
        metadata = ObjectMeta(name="my-name", namespace="my-namespace")
        mock_response.json.return_value = {"field": 1, "list_field": [1], "once_field": 1, "read_only_field": 1}
        instance = ModelTest.get_or_create(metadata=metadata, field=2, list_field=[2], once_field=2, read_only_field=2)
        assert instance.field == 2
        assert instance.list_field == [2]
        assert instance.once_field == 1
        assert instance.read_only_field == 1

    def test_set_dict_field_to_none(self, mock_response):
        metadata = ObjectMeta(name="my-name", namespace="my-namespace")
        mock_response.json.return_value = {'dict_field': {'thing': 'otherthing'}}
        instance = ModelTest.get_or_create(metadata=metadata, dict_field=None)
        assert instance.dict_field is None

    def test_annotations_merge(self, mock_response):
        mock_response.json.return_value = {
            u"metadata": {
                u"name": u"my-name",
                u"namespace": u"my-namespace",
                u"annotations": {
                    u"must_keep": u"this",
                    u"will_overwrite": u"this"
                }
            }
        }
        metadata = ObjectMeta(name="my-name", namespace="my-namespace", annotations={u"will_overwrite": u"that"})
        instance = ModelTest.get_or_create(metadata=metadata)
        assert instance.metadata.annotations[u"will_overwrite"] == u"that"
        assert instance.metadata.annotations[u"must_keep"] == u"this"
