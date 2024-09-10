"""Tests for company model."""

import pytest
from model_bakery import baker

from my_game_list.games.models import Company


@pytest.mark.django_db()
def test_company_dunder_str() -> None:
    """Test the `Company` dunder str method."""
    developer = baker.make(Company)
    assert str(developer) == developer.name
