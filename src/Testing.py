__author__ = 'n3k'

from HanoiTowers import *

TA1 = Tower(max_rings=7)
TA2 = Tower()
TA3 = Tower()
IS = GameState(TA1, TA2, TA3, parent=None)

TB1 = Tower()
TB2 = Tower(max_rings=7)
TB3 = Tower()
FS = GameState(TB1, TB2, TB3, parent=None, end_goal=True)

print "Initial State: %s" % str(IS.state)
print "Final State: %s" % str(FS.state)

solver = Hanoi(IS, FS)
solver.A_STAR()

print "\n\nRecursive Hanoi\n\n"
Hanoi.recursive_hanoi(7, "src", "aux", "dst")