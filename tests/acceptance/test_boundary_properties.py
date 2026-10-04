from hypothesis import given, settings
from hypothesis import strategies as st

from fixtureforge.models import FixtureSpec


@given(diameter=st.floats(min_value=12, max_value=40, allow_nan=False),
       wall=st.floats(min_value=2.4, max_value=6, allow_nan=False),
       clearance=st.floats(min_value=0.2, max_value=1, allow_nan=False))
@settings(max_examples=30)
def test_coupled_pitch_boundaries(diameter, wall, clearance):
    # Independent algebraic minimum: diameter + clearance + two walls + 28.
    minimum = diameter + clearance + 2 * wall + 28
    payload = dict(sensor_diameter_mm=diameter, wall_mm=wall, clearance_mm=clearance,
                   mount_pitch_y_mm=minimum + 1e-6)
    assert FixtureSpec(**payload).mount_pitch_y_mm > minimum
    payload['mount_pitch_y_mm'] = minimum - 1e-4
    try:
        FixtureSpec(**payload)
    except ValueError as error:
        assert 'mount_pitch_y_mm' in str(error)
    else:
        raise AssertionError('Impossible pitch was accepted')
