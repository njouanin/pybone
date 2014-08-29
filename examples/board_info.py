from pybone.bone import detect_platform
from pybone.board import Board

pf = detect_platform()
b = Board(pf)
print(b.name)
print(b.serial_number)
print(b.revision)