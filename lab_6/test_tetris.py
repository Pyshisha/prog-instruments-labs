from unittest.mock import Mock, patch

import pytest

from tetris import Piece, SHAPES, SHAPE_COLORS, create_grid, valid_space, check_lost, get_shape



def test_piece_initialization():
    """Тест инициализации фигуры."""
    piece = Piece(5, 0, SHAPES[0])  # S-фигура
    assert piece.x == 5
    assert piece.y == 0
    assert piece.shape == SHAPES[0]
    assert piece.color == SHAPE_COLORS[0]
    assert piece.rotation == 0


def test_valid_space_invalid():
    """Тест проверки невалидного пространства для фигуры."""
    piece = Piece(5, 1, SHAPES[0])
    locked_pos = {(5, 0): (255, 0, 0)}
    grid = create_grid(locked_pos)
    assert valid_space(piece, grid) is False


def test_check_lost_true():
    """Тест проверки проигрыша (проиграл)."""
    locked_pos = {(5, -2): (255, 0, 0)}  # Позиция выше верхней границы
    assert check_lost(locked_pos) is True


def test_valid_space_valid():
    """Тест проверки валидного пространства для фигуры."""
    piece = Piece(5, 0, SHAPES[0])
    grid = create_grid()
    assert valid_space(piece, grid) is True


@pytest.mark.parametrize("shape_index, expected_color", [
    (0, (0, 255, 0)),
    (1, (255, 0, 0)),
    (2, (0, 255, 255)),
    (3, (255, 255, 0)),
    (4, (255, 165, 0)),
    (5, (0, 0, 255)),
    (6, (128, 0, 128)),
])
def test_piece_color_mapping(shape_index, expected_color):
    """Тест сопоставления цвета фигуры."""
    piece = Piece(0, 0, SHAPES[shape_index])
    assert piece.color == expected_color


@patch('tetris.random.choice')
def test_get_shape_always_o(mock_choice):
    """Мок: get_shape всегда возвращает O-фигуру."""
    mock_choice.return_value = SHAPES[3]

    piece = get_shape()

    assert piece.shape == SHAPES[3]
    assert piece.color == SHAPE_COLORS[3]
    mock_choice.assert_called_once_with(SHAPES)


def test_keyboard_input_with_mock():
    """Тест обработки клавиатурного ввода."""
    mock_callback = Mock()

    key_presses = ['left', 'right', 'up', 'down']

    for key in key_presses:
        mock_callback(key)

    assert mock_callback.call_count == 4

    calls = [call[0][0] for call in mock_callback.call_args_list]
    assert 'left' in calls
    assert 'right' in calls
    assert 'up' in calls


@pytest.fixture
def test_piece():
    """Фикстура для тестовой фигуры."""
    return Piece(5, 0, SHAPES[0])


def test_piece_properties_with_fixture(test_piece):
    """Тест свойств фигуры с фикстурой."""

    piece = test_piece

    assert piece.x == 5
    assert piece.y == 0
    assert piece.rotation == 0
