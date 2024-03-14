from point import Point
from enums import CheckerType, SideType

# Сторона за которую играет игрок
PLAYER_SIDE = SideType.RED

# Размер поля
X_SIZE = 8
Y_SIZE = 8
# Размер ячейки в пикселях
CELL_SIZE = 100

# Скорость анимации (больше = быстрее)
ANIMATION_SPEED = 6

# Ширина рамки 
BORDER_WIDTH = 2 * 2

# Цвета игровой доски
FIELD_COLORS = ['#ffffff', '#050608']
# Цвет рамки при наведении на ячейку мышкой
HOVER_BORDER_COLOR = '#54b346'
# Цвет рамки при выделении ячейки
SELECT_BORDER_COLOR = '#944444'
# Цвет кружков возможных ходов
POSIBLE_MOVE_CIRCLE_COLOR = '#444444'

# Возможные смещения ходов шашек
MOVE_OFFSETS = [
    Point(-1, -1),
    Point( 1, -1),
    Point(-1,  1),
    Point( 1,  1)
]

# Массивы типов красных и синих шашек [Обычная пешка, дамка]
RED_CHECKERS = [CheckerType.RED_REGULAR, CheckerType.RED_QUEEN]
BLUE_CHECKERS = [CheckerType.BLUE_REGULAR, CheckerType.BLUE_QUEEN]