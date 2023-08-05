#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cryptohands` package."""

import pytest
from cryptohands import cryptohands


def test_update_all_balances():
    cryptohands.update_all_balances()
