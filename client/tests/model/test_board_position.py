"""unit tests for the model.board_position module"""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from hardware.interface import ENDIANNESS
from model.board_position import BoardPosition


@given(st.integers(min_value=-5, max_value=15), st.integers(min_value=-5, max_value=15))
def test_valid_board_boundaries(row: int, col: int):
    """test board coordinate boundaries"""

    if 0 <= row <= BoardPosition.MAX_ROW and 0 <= col <= BoardPosition.MAX_COL:
        pos = BoardPosition(row=row, col=col)
        assert pos.row == row
        assert pos.col == col
        return

    with pytest.raises(ValueError):
        BoardPosition(row=row, col=col)


@pytest.mark.parametrize(
    ("row", "col", "expected"),
    [
        (0, 0, 0x00),
        (9, 9, 0x99),
        (9, 0, 0x90),
        (0, 9, 0x09),
        (4, 7, 0x47),
        (6, 3, 0x63),
        (0, 1, 0x01),
        (8, 5, 0x85),
    ],
)
def test_encode(row: int, col: int, expected: int):
    """test position encoding"""

    encoded_pos = BoardPosition(row=row, col=col).hardware_encode()

    assert len(encoded_pos) == 1
    assert encoded_pos == expected.to_bytes(1, ENDIANNESS)


@given(st.integers(min_value=0, max_value=9), st.integers(min_value=0, max_value=9))
def test_bytes_conversion(row: int, col: int):
    """test the __bytes__ method."""

    pos = BoardPosition(row=row, col=col)
    assert bytes(pos) == pos.hardware_encode()
