from pybone.bone import detect_platform
from bone.board import Board

pf = detect_platform()
b = Board(pf)

print("Board name: %s" % b.name)
print("Revision : %s" % b.revision)
print("Serial number: %s" % b.serial_number)
