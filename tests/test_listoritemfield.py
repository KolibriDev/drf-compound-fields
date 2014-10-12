#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
test_listoritemfield
--------------------

Tests for `drf_compound_fields.fields.ListOrItemField`.

"""


from . import test_settings

from datetime import date

from django.core.exceptions import ValidationError
from rest_framework import ISO_8601
from rest_framework.fields import CharField
from rest_framework.fields import DateField
import pytest

from drf_compound_fields.fields import ListOrItemField


def test_to_native_list():
    """
    When given a valid list, the ListOrItemField to_native method should utilize the list to-native
    logic.
    """
    field = ListOrItemField(DateField(format=ISO_8601))
    data = field.to_native([date.today()])
    assert [date.today().isoformat()] == data


def test_from_native_list():
    """
    When given a valid list, the ListOrItemField from_native method should utilize the list
    from-native logic.
    """
    field = ListOrItemField(DateField(format=ISO_8601))
    data = field.from_native([date.today().isoformat()])
    assert [date.today()] == data


def test_to_native_item():
    """
    When given a valid item, the ListOrItemField to_native method should utilize the item to-native
    logic.
    """
    field = ListOrItemField(DateField(format=ISO_8601))
    data = field.to_native(date.today())
    assert date.today().isoformat() == data


def test_from_native_item():
    """
    When given a valid item, the ListOrItemField from_native method should utilize the item
    from-native logic.
    """
    field = ListOrItemField(DateField(format=ISO_8601))
    data = field.from_native(date.today().isoformat())
    assert date.today() == data


def test_validate_required_missing():
    """
    When given a None value the ListOrItemField validate method should raise a ValidationError.
    """
    field = ListOrItemField()
    with pytest.raises(ValidationError):
        field.validate(None)


def test_invalid_item():
    """
    When given an invalid value the ListOrItemField validate method should raise a ValidationError.
    """
    field = ListOrItemField(CharField(max_length=5))
    with pytest.raises(ValidationError):
        field.run_validators('123456')


def test_list_value_invalid_items():
    """
    When given a list with an invalid value the ListOrItemField validate method should raise a
    ValidationError.
    """
    field = ListOrItemField(CharField(max_length=5))
    try:
        field.run_validators(['12345', '123456'])
        assert False, 'Expected ValidationError'
    except ValidationError as e:
        assert [1] == list(e.messages[0].keys())

def test_validate_not_required_missing():
    """
    When given a null value and is not required, do not raise a ValidationError
    """
    field = ListOrItemField(required=False)

    try:
        field.validate(None)
    except ValidationError:
        assert False, "ValidationError was raised"
