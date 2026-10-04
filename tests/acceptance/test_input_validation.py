import pytest

from fixtureforge.models import FixtureSpec


@pytest.mark.parametrize('field,value', [
    ('units', 'inch'), ('schema_version', '2.0'),
    ('sensor_diameter_mm', -1), ('sensor_diameter_mm', float('nan')),
    ('wall_mm', 2.39), ('base_mm', 4.99), ('sensor_length_mm', 24.99),
    ('clearance_mm', 1.01), ('mount_pitch_y_mm', 30),
    ('mount_pitch_x_mm', 31.99), ('sensor_diameter_mm', float('inf')),
])
def test_reject_invalid_before_cad(field, value):
    with pytest.raises(ValueError):
        FixtureSpec(**{field: value})


def test_defaults_and_equal_boundaries():
    assert FixtureSpec().sensor_diameter_mm == 24
    assert FixtureSpec(wall_mm=2.4, base_mm=5).wall_mm == 2.4
    with pytest.raises(ValueError):
        FixtureSpec(unrecognized=42)
