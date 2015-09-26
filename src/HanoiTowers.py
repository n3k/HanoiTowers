__author__ = 'n3k'

class Tower(object):

    def __init__(self, rings=[], max_rings=0):
        if len(rings) > 0:
            self.rings = rings
        else:
            self.rings = [i for i in xrange(max_rings, 0, -1)]

    def __iter__(self):
        return iter(self.rings)

    def is_empty(self):
        return len(self.rings) == 0

    def get_top_ring(self):
        if self.is_empty():
            return 1000
        return self.rings[-1:].pop()

    def put_ring(self, ring):
        if not self.is_empty():
            if ring < self.rings[-1:].pop():
                self.rings.append(ring)
        else:
            self.rings.append(ring)

    def pop_ring(self):
        return self.rings.pop()

    def move_to(self, tower_dest):
        if not self.is_empty():
            if self.get_top_ring() < tower_dest.get_top_ring():
                tower_dest.put_ring(self.pop_ring())

    def get_state(self):
        return tuple(self.rings)


class GameState(object):
    def __init__(self, A, B , C, parent, end_goal=False):
        self.state = ([i for i in A],
                      [i for i in B],
                      [i for i in C])
        self.end_goal = end_goal
        self.value = None
        self.parent = parent

    def __eq__(self, other):
        if isinstance(other, GameState):
            try:
                for t_index in xrange(0, len(self.state)):
                    for r_index in xrange(0, len(self.state[t_index])):
                        if self.state[t_index][r_index] != other.state[t_index][r_index]:
                            return False
                for t_index in xrange(0, len(other.state)):
                    for r_index in xrange(0, len(other.state[t_index])):
                        if other.state[t_index][r_index] != self.state[t_index][r_index]:
                            return False
            except IndexError:
                return False
            return True

    def F(self, cost, final_state):
        self.value = self.G(cost) + self.H(final_state)
        return self.value

    def G(self, cost):
        """
        This is the real cost function
        """
        return cost + 1

    def H(self, final_state):
        """
        This is the heuristic function
        """
        if not isinstance(final_state, GameState):
            raise Exception("This is not a GameState object")

        current_tower_1 = self.state[0]
        current_tower_2 = self.state[1]
        current_tower_3 = self.state[2]
        final_tower_1 = final_state.state[0]
        final_tower_2 = final_state.state[1]
        final_tower_3 = final_state.state[2]

        v = 0

        """
        len_t1 = len(current_tower_1)
        len_t2 = len(current_tower_2)
        len_t3 = len(current_tower_3)

        total_rings = len_t1 + len_t2 + len_t3
        if len_t1 > 0:
            for i in xrange(len_t1-1, -1, -1):
                if i > 0:
                    v += (abs(current_tower_1[i]-current_tower_1[i-1]) - total_rings)
                else:
                    v += total_rings - current_tower_1[i]

        if len_t2 > 0:
            for i in xrange(len_t2-1, -1, -1):
                if i > 0:
                    v += (abs(current_tower_2[i]-current_tower_2[i-1]) - total_rings)
                else:
                    v += total_rings - current_tower_2[i]

        if len_t3 > 0:
            for i in xrange(len_t3-1, -1, -1):
                if i > 0:
                    v += (abs(current_tower_3[i]-current_tower_3[i-1]) - total_rings)
                else:
                    v += total_rings - current_tower_3[i]
        """

        try:
            for r_index in xrange(0, len(current_tower_1)):
                if current_tower_1[r_index] == final_tower_1[r_index]:
                    v -= 1
        except IndexError:
            pass

        try:
            for r_index in xrange(0, len(current_tower_2)):
                if current_tower_2[r_index] == final_tower_2[r_index]:
                    v -= 1
        except IndexError:
            pass

        try:
            for r_index in xrange(0, len(current_tower_3)):
                if current_tower_3[r_index] == final_tower_3[r_index]:
                    v -= 1
        except IndexError:
            pass

        return v

class Hanoi(object):

    def __init__(self, initial_state, final_state):
        self.final_state = final_state
        self.initial_state = initial_state
        self.open_list = []
        self.closed_list = []

    @classmethod
    def recursive_hanoi(cls, disc, src, aux, dst):
        if disc > 0:
            cls.recursive_hanoi(disc-1, src, dst, aux)
            print "Move disc %s from %s to %s" % (disc, src, dst)
            cls.recursive_hanoi(disc-1, aux, src, dst)

    def select_next_node(self, cost):
        minor_F = 1000000
        index = 0
        index_minor = 1000000
        for node in self.open_list:
            node_F = node.F(cost=cost, final_state=self.final_state)
            if node_F < minor_F:
                minor_F = node_F
                index_minor = index
            index += 1

        selected = self.open_list[index_minor]
        del self.open_list[index_minor]
        return selected

    def generate_successors(self, node):
        T1 = Tower(node.state[0])
        T2 = Tower(node.state[1])
        T3 = Tower(node.state[2])
        successors = []

        TA1_1 = Tower(rings=T1.rings[:])
        TA2_1 = Tower(rings=T2.rings[:])
        TA3_1 = Tower(rings=T3.rings[:])
        TA1_1.move_to(TA2_1)
        successors.append(GameState(TA1_1, TA2_1, TA3_1, parent=node))

        TA1_2 = Tower(rings=T1.rings[:])
        TA2_2 = Tower(rings=T2.rings[:])
        TA3_2 = Tower(rings=T3.rings[:])
        TA1_2.move_to(TA3_2)
        successors.append(GameState(TA1_2, TA2_2, TA3_2, parent=node))

        TB1_1 = Tower(rings=T1.rings[:])
        TB2_1 = Tower(rings=T2.rings[:])
        TB3_1 = Tower(rings=T3.rings[:])
        TB2_1.move_to(TB1_1)
        successors.append(GameState(TB1_1, TB2_1, TB3_1, parent=node))

        TB1_2 = Tower(rings=T1.rings[:])
        TB2_2 = Tower(rings=T2.rings[:])
        TB3_2 = Tower(rings=T3.rings[:])
        TB2_2.move_to(TB3_2)
        successors.append(GameState(TB1_2, TB2_2, TB3_2, parent=node))

        TC1_1 = Tower(rings=T1.rings[:])
        TC2_1 = Tower(rings=T2.rings[:])
        TC3_1 = Tower(rings=T3.rings[:])
        TC3_1.move_to(TC1_1)
        successors.append(GameState(TC1_1, TC2_1, TC3_1, parent=node))

        TC1_2 = Tower(rings=T1.rings[:])
        TC2_2 = Tower(rings=T2.rings[:])
        TC3_2 = Tower(rings=T3.rings[:])
        TC3_2.move_to(TC2_2)
        successors.append(GameState(TC1_2, TC2_2, TC3_2, parent=node))

        return successors

    def reconstruct_path(self, node):
        path = []
        while node.parent != None:
            path.append(node)
            node = node.parent
        path.append(self.initial_state)
        return path

    def A_STAR(self):
        cost = -1
        self.open_list.append(self.initial_state)
        while len(self.open_list) > 0:
            node = self.select_next_node(cost)
            cost += 1
            self.closed_list.append(node)
            if node == self.final_state:
                # Stop here and trace back
                print "We GOT IT"
                print "Total States: %d" % len(self.closed_list)
                print "Path To Solution:"
                for n in reversed(self.reconstruct_path(node)):
                    print n.state
                break
            else:
                successors = self.generate_successors(node)
                for s in successors:
                    new_state = True
                    for c in self.closed_list:
                        if c == s:
                            new_state = False
                    if new_state:
                        for o in self.open_list:
                            if o == s:
                                new_state = False
                                if o.value > s.value:
                                    self.open_list.remove(o)
                                    self.open_list.append(s)
                                    break
                        if new_state:
                            self.open_list.append(s)


