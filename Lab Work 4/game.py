from tkinter import Canvas, Event, messagebox
from PIL import Image, ImageTk
from random import choice, randint
from pathlib import Path
from time import sleep
from math import inf

from field import Field
from move import Move
from constants import *
from enums import CheckerType, SideType
from tkinter import Tk, Canvas, PhotoImage
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets


class Game:
    def __init__(self, canvas: Canvas, x_field_size: int, y_field_size: int, window: Tk):
        self.__canvas = canvas
        self.__window = window
        self.__field = Field(x_field_size, y_field_size)
        self.__player_id_turn = 1

        self.__hovered_cell = Point()
        self.__selected_cell = Point()
        self.__animated_cell = Point()

        self.__init_images()

        self.__draw()

    def __init_images(self):
        '''Инициализация изображений'''
        self.__images = {
            CheckerType.RED_REGULAR: ImageTk.PhotoImage(
                Image.open(Path('assets', 'RR.png')).resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)),
            CheckerType.BLUE_REGULAR: ImageTk.PhotoImage(
                Image.open(Path('assets', 'BR.png')).resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)),
            CheckerType.RED_QUEEN: ImageTk.PhotoImage(
                Image.open(Path('assets', 'RQ.png')).resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)),
            CheckerType.BLUE_QUEEN: ImageTk.PhotoImage(
                Image.open(Path('assets', 'BQ.png')).resize((CELL_SIZE, CELL_SIZE), Image.LANCZOS)),
        }

    def __animate_move(self, move: Move):
        '''Анимация перемещения шашки'''
        self.__animated_cell = Point(move.from_x, move.from_y)
        self.__draw()

        # Создание анимации для шашек
        animated_checker = self.__canvas.create_image(move.from_x * CELL_SIZE, move.from_y * CELL_SIZE,
                                                      image=self.__images.get(
                                                          self.__field.type_at(move.from_x, move.from_y)), anchor='nw',
                                                      tag='animated_checker')

        # Вектора движения
        dx = 1 if move.from_x < move.to_x else -1
        dy = 1 if move.from_y < move.to_y else -1

        # Анимация
        for distance in range(abs(move.from_x - move.to_x)):
            for _ in range(100 // ANIMATION_SPEED):
                self.__canvas.move(animated_checker, ANIMATION_SPEED / 100 * CELL_SIZE * dx,
                                   ANIMATION_SPEED / 100 * CELL_SIZE * dy)
                self.__canvas.update()
                sleep(0.01)

        self.__animated_cell = Point()

    def __draw(self):
        '''Отрисовка сетки поля и шашек'''
        self.__canvas.delete('all')
        self.__draw_field_grid()
        self.__draw_checkers()
        self.__window.title(f"Шашки | Ход {'красных' if self.__player_id_turn == 1 else 'синих'}")

    def __draw_field_grid(self):
        '''Отрисовка сетки поля'''
        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                self.__canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE, x * CELL_SIZE + CELL_SIZE,
                                               y * CELL_SIZE + CELL_SIZE, fill=FIELD_COLORS[(y + x) % 2], width=0,
                                               tag='boards')

                # Отрисовка рамок у необходимых клеток
                if (x == self.__selected_cell.x and y == self.__selected_cell.y):
                    self.__canvas.create_rectangle(x * CELL_SIZE + BORDER_WIDTH // 2, y * CELL_SIZE + BORDER_WIDTH // 2,
                                                   x * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2,
                                                   y * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2,
                                                   outline=SELECT_BORDER_COLOR, width=BORDER_WIDTH, tag='border')
                elif (x == self.__hovered_cell.x and y == self.__hovered_cell.y):
                    self.__canvas.create_rectangle(x * CELL_SIZE + BORDER_WIDTH // 2, y * CELL_SIZE + BORDER_WIDTH // 2,
                                                   x * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2,
                                                   y * CELL_SIZE + CELL_SIZE - BORDER_WIDTH // 2,
                                                   outline=HOVER_BORDER_COLOR, width=BORDER_WIDTH, tag='border')

                # Отрисовка возможных точек перемещения, если есть выбранная ячейка
                if (self.__selected_cell):
                    player_moves_list = self.__get_moves_list(PLAYER_SIDE) + self.__get_moves_list(SideType.BLUE)
                    for move in player_moves_list:
                        if (self.__selected_cell.x == move.from_x and self.__selected_cell.y == move.from_y):
                            self.__canvas.create_oval(move.to_x * CELL_SIZE + CELL_SIZE / 3,
                                                      move.to_y * CELL_SIZE + CELL_SIZE / 3,
                                                      move.to_x * CELL_SIZE + (CELL_SIZE - CELL_SIZE / 3),
                                                      move.to_y * CELL_SIZE + (CELL_SIZE - CELL_SIZE / 3),
                                                      fill=POSIBLE_MOVE_CIRCLE_COLOR, width=0,
                                                      tag='posible_move_circle')

    def __draw_checkers(self):
        '''Отрисовка шашек'''
        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                # Не отрисовывать пустые ячейки и анимируемую шашку
                if (self.__field.type_at(x, y) != CheckerType.NONE and not (
                        x == self.__animated_cell.x and y == self.__animated_cell.y)):
                    self.__canvas.create_image(x * CELL_SIZE, y * CELL_SIZE,
                                               image=self.__images.get(self.__field.type_at(x, y)), anchor='nw',
                                               tag='checkers')

    def mouse_move(self, event: Event):
        '''Событие перемещения мышки'''
        x, y = (event.x) // CELL_SIZE, (event.y) // CELL_SIZE
        if (x != self.__hovered_cell.x or y != self.__hovered_cell.y):
            self.__hovered_cell = Point(x, y)
            self.__draw()

    def mouse_down(self, event: Event):
        '''Событие нажатия мышки'''

        x, y = event.x // CELL_SIZE, event.y // CELL_SIZE

        # Если точка не внутри поля
        if not (self.__field.is_within(x, y)): return

        if self.__player_id_turn == 1:
            player_checkers = RED_CHECKERS
            enemy_checkers = BLUE_CHECKERS
        else:
            player_checkers = BLUE_CHECKERS
            enemy_checkers = RED_CHECKERS

        # Если нажатие по шашке игрока, то выбрать её
        if self.__field.type_at(x, y) in player_checkers or self.__field.type_at(x, y) in enemy_checkers:
            self.__selected_cell = Point(x, y)
            self.__draw()
        else:
            move = Move(self.__selected_cell.x, self.__selected_cell.y, x, y)

            # Если нажатие по ячейке, на которую можно походить
            if (move in self.__get_moves_list(SideType.RED)) or (move in self.__get_moves_list(SideType.BLUE)):
                self.__handle_player_turn(move)

    def __handle_move(self, move: Move, draw: bool = True, debug: bool = False) -> bool:
        '''Совершение хода'''
        if (draw): self.__animate_move(move)

        # Изменение позиции шашки
        self.__field.at(move.to_x, move.to_y).change_type(self.__field.type_at(move.from_x, move.from_y))
        self.__field.at(move.from_x, move.from_y).change_type(CheckerType.NONE)

        if move.to_y == 0 and self.__field.type_at(move.to_x, move.to_y) == CheckerType.RED_REGULAR:
            self.__field.at(move.to_x, move.to_y).change_type(CheckerType.RED_QUEEN)

        if move.to_y == 7 and self.__field.type_at(move.to_x, move.to_y) == CheckerType.BLUE_REGULAR:
            self.__field.at(move.to_x, move.to_y).change_type(CheckerType.BLUE_QUEEN)

        if debug:
            print(move)

        # Вектора движения
        dx = -1 if move.from_x < move.to_x else 1
        dy = -1 if move.from_y < move.to_y else 1

        # Удаление съеденных шашек
        has_killed_checker = False
        x, y = move.to_x, move.to_y
        while x != move.from_x or y != move.from_y:
            x += dx
            y += dy
            if self.__field.type_at(x, y) != CheckerType.NONE:
                self.__field.at(x, y).change_type(CheckerType.NONE)
                has_killed_checker = True

        if draw:
            self.__draw()

        return has_killed_checker

    def __handle_player_turn(self, move: Move):
        '''Обработка хода игрока'''
        self.__player_id_turn = 1 if self.__player_id_turn == 0 else 0
        # Была ли убита шашка
        has_killed_checker = self.__handle_move(move, debug=True)

        required_moves_list = list(
            filter(lambda required_move: move.to_x == required_move.from_x and move.to_y == required_move.from_y,
                   self.__get_required_moves_list(PLAYER_SIDE)))

        # Если есть ещё ход этой же шашкой
        if has_killed_checker and required_moves_list:
            self.__player_id_turn = 1 if self.__player_id_turn == 0 else 0

        self.__selected_cell = Point()

    def __check_for_game_over(self):
        '''Проверка на конец игры'''
        game_over = False

        if self.__field.red_checkers_count == 0:
            # Синие ВЫИГРАЛИ
            answer = messagebox.showinfo('Конец игры', 'Синие выиграли')
            game_over = True

        if self.__field.blue_checkers_count == 0:
            # Красные ВЫИГРАЛИ
            answer = messagebox.showinfo('Конец игры', 'Красные выиграли')
            game_over = True

        red_moves_list = self.__get_moves_list(SideType.RED)
        blue_moves_list = self.__get_moves_list(SideType.BLUE)

        if not red_moves_list and not blue_moves_list:
            if self.__player_id_turn == 1:
                answer = messagebox.showinfo('Конец игры', 'Синие выиграли')
            else:
                answer = messagebox.showinfo('Конец игры', 'Красные выиграли')
            game_over = True

        if game_over:
            self.__init__(self.__canvas, self.__field.x_size, self.__field.y_size)

    def __get_moves_list(self, side: SideType) -> list[Move]:
        '''Получение списка ходов'''
        moves_list = self.__get_required_moves_list(side)
        if not (moves_list):
            moves_list = self.__get_optional_moves_list(side)
        return moves_list

    def __get_required_moves_list(self, side: SideType) -> list[Move]:
        '''Получение списка обязательных ходов'''
        moves_list = []

        # Определение типов шашек
        if side == SideType.RED:
            friendly_checkers = RED_CHECKERS
            enemy_checkers = BLUE_CHECKERS
        elif side == SideType.BLUE:
            friendly_checkers = BLUE_CHECKERS
            enemy_checkers = RED_CHECKERS
        else:
            return moves_list

        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):

                # Для обычной шашки
                if self.__field.type_at(x, y) == friendly_checkers[0]:
                    for offset in MOVE_OFFSETS:
                        if not (self.__field.is_within(x + offset.x * 2, y + offset.y * 2)): continue

                        if self.__field.type_at(x + offset.x, y + offset.y) in enemy_checkers and self.__field.type_at(
                                x + offset.x * 2, y + offset.y * 2) == CheckerType.NONE:
                            moves_list.append(Move(x, y, x + offset.x * 2, y + offset.y * 2))

                # Для дамки
                elif self.__field.type_at(x, y) == friendly_checkers[1]:
                    for offset in MOVE_OFFSETS:
                        if not (self.__field.is_within(x + offset.x * 2, y + offset.y * 2)): continue

                        has_enemy_checker_on_way = False

                        for shift in range(1, self.__field.size):
                            if not (self.__field.is_within(x + offset.x * shift, y + offset.y * shift)): continue

                            # Если на пути не было вражеской шашки
                            if not has_enemy_checker_on_way:
                                if self.__field.type_at(x + offset.x * shift, y + offset.y * shift) in enemy_checkers:
                                    has_enemy_checker_on_way = True
                                    continue
                                # Если на пути союзная шашка - то закончить цикл
                                elif (self.__field.type_at(x + offset.x * shift,
                                                           y + offset.y * shift) in friendly_checkers):
                                    break

                            # Если на пути была вражеская шашка
                            if has_enemy_checker_on_way:
                                if (self.__field.type_at(x + offset.x * shift,
                                                         y + offset.y * shift) == CheckerType.NONE):
                                    moves_list.append(Move(x, y, x + offset.x * shift, y + offset.y * shift))
                                else:
                                    break
                elif self.__field.type_at(x, y) == enemy_checkers[0]:
                    for offset in MOVE_OFFSETS:
                        if not (self.__field.is_within(x + offset.x * 2, y + offset.y * 2)): continue

                        if self.__field.type_at(x + offset.x, y + offset.y) in friendly_checkers and self.__field.type_at(
                                x + offset.x * 2, y + offset.y * 2) == CheckerType.NONE:
                            moves_list.append(Move(x, y, x + offset.x * 2, y + offset.y * 2))
                elif self.__field.type_at(x, y) == enemy_checkers[1]:
                    for offset in MOVE_OFFSETS:
                        if not (self.__field.is_within(x + offset.x * 2, y + offset.y * 2)): continue

                        has_enemy_checker_on_way = False

                        for shift in range(1, self.__field.size):
                            if not (self.__field.is_within(x + offset.x * shift, y + offset.y * shift)): continue

                            # Если на пути не было вражеской шашки
                            if not has_enemy_checker_on_way:
                                if self.__field.type_at(x + offset.x * shift, y + offset.y * shift) in friendly_checkers:
                                    has_enemy_checker_on_way = True
                                    continue
                                # Если на пути союзная шашка - то закончить цикл
                                elif (self.__field.type_at(x + offset.x * shift,
                                                           y + offset.y * shift) in enemy_checkers):
                                    break

                            # Если на пути была вражеская шашка
                            if has_enemy_checker_on_way:
                                if (self.__field.type_at(x + offset.x * shift,
                                                         y + offset.y * shift) == CheckerType.NONE):
                                    moves_list.append(Move(x, y, x + offset.x * shift, y + offset.y * shift))
                                else:
                                    break

        return moves_list

    def __get_optional_moves_list(self, side: SideType) -> list[Move]:
        '''Получение списка необязательных ходов'''
        moves_list = []

        # Определение типов шашек
        if side == SideType.RED:
            friendly_checkers = RED_CHECKERS
        elif side == SideType.BLUE:
            friendly_checkers = BLUE_CHECKERS
        else:
            return moves_list

        for y in range(self.__field.y_size):
            for x in range(self.__field.x_size):
                # Для обычной шашки
                if self.__field.type_at(x, y) == friendly_checkers[0]:
                    for offset in MOVE_OFFSETS[:2] if side == SideType.RED else MOVE_OFFSETS[2:]:
                        if not (self.__field.is_within(x + offset.x, y + offset.y)): continue

                        if self.__field.type_at(x + offset.x, y + offset.y) == CheckerType.NONE:
                            moves_list.append(Move(x, y, x + offset.x, y + offset.y))

                # Для дамки
                elif self.__field.type_at(x, y) == friendly_checkers[1]:
                    for offset in MOVE_OFFSETS:
                        if not (self.__field.is_within(x + offset.x, y + offset.y)): continue

                        for shift in range(1, self.__field.size):
                            if not (self.__field.is_within(x + offset.x * shift, y + offset.y * shift)): continue

                            if self.__field.type_at(x + offset.x * shift, y + offset.y * shift) == CheckerType.NONE:
                                moves_list.append(Move(x, y, x + offset.x * shift, y + offset.y * shift))
                            else:
                                break
        return moves_list


def run_game():
    main_window = Tk()
    main_window.title('Шашки')
    main_window.resizable()
    main_window.iconphoto(False, PhotoImage(file='assets/icon.png'))

    # Создание холста
    main_canvas = Canvas(main_window, width=CELL_SIZE * X_SIZE, height=CELL_SIZE * Y_SIZE)
    main_canvas.pack()

    game = Game(main_canvas, X_SIZE, Y_SIZE, main_window)

    main_canvas.bind("<Motion>", game.mouse_move)
    main_canvas.bind("<Button-1>", game.mouse_down)

    main_window.mainloop()


if __name__ == "__main__":
    run_game()