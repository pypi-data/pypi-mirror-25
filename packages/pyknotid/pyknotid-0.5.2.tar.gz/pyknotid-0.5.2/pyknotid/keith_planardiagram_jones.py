'''
Planar diagrams
===============

Classes for working with planar diagram notation of knot diagrams.

See individual class documentation for more details.
'''


import numpy as n


class PlanarDiagram(list):
    '''A class for containing and manipulating planar diagrams.

    Just provides convenient display and conversion methods for now.
    In the future, will support simplification.

    Shorthand input may be of the form ``X_1,4,2,5 X_3,6,4,1 X_5,2,6,3``.
    This is (should be?) the same as returned by repr.

    Parameters
    ----------
    crossings : array-like or string or GaussCode
        The list of crossings in the diagram, which will be converted
        to an internal planar diagram representation. Currently these are
        mostly converted via a GaussCode instance, so in addition to the
        shorthand any array-like supported by
        :class:`~pyknot2.representations.gausscode.GaussCode` may be used.
    '''

    def __init__(self, crossings=''):
        from pyknot2.representations import gausscode
        if isinstance(crossings, str):
            self.extend(shorthand_to_crossings(crossings))
        elif isinstance(crossings, gausscode.GaussCode):
            self.extend(gausscode_to_crossings(crossings))
        elif isinstance(crossings, list) and (isinstance(crossings[0], Crossing) or isinstance(crossings[0], Point)):
            self.extend(crossings)
        elif isinstance(crossings, Crossing) or isinstance(crossings, Point):
            self.extend([crossings])
        else:
            self.extend(gausscode_to_crossings(
                gausscode.GaussCode(crossings)))


    def __str__(self):
        number_of_crossings = sum(isinstance(i, Crossing) for i in self)
        number_of_points = sum(isinstance(i, Point) for i in self)
        lenstr = 'PD with {0} crossings and {1} points: \n'.format(
            number_of_crossings, number_of_points)
        return lenstr + ' '.join([str(crossing) for crossing in self])

    def __repr__(self):
        return self.__str__()

    def as_mathematica(self):
        '''
        Returns a mathematica code representation of self, usable in the
        mathematica knot tools.
        '''
        s = 'PD['
        s = s + ', '.join(crossing.as_mathematica() for crossing in self)
        return s + ']'

    def as_spherogram(self):
        '''
        Get a planar diagram class from the Spherogram module, which
        can be used to access SnapPy's manifold tools.

        This method requires that spherogram and SnapPy are installed.
        '''
        from spherogram import Crossing, Link
        scs = [Crossing() for crossing in self]

        indices = {}
        for i in range(len(self)):
            c = self[i]
            for j in range(len(c)):
                number = c[j]
                if number in indices:
                    otheri, otherj = indices.pop(number)
                    scs[i][j] = scs[otheri][otherj]
                else:
                    indices[number] = (i, j)
        return Link(scs)

    def contract_points(self):
        '''
        For appropriately contracting :class: `Points` in a
        :class: `PlanarDiagram` According to the following rules:

        P_a,b P_b,c -> P_a,c
        P_a,b P_a,b -> P_a,a
        '''
        import copy

        pd_crossings = [x for x in self if type(x) == Crossing]
        pd_points = [x for x in self if type(x) == Point]

        pd_trimmed = PlanarDiagram()
        for crossing in pd_crossings:
            pd_trimmed.append(crossing)

        substituted_points = []
        for i in range(len(pd_points)):
            if pd_points[i] not in substituted_points:
                pd_trimmed.append(pd_points[i])
                totally_simplified = False
                while not totally_simplified:
                    pd_trimmed_old = copy.copy(pd_trimmed)
                    for j in range(i+1, len(pd_points)):
                        if (len(pd_trimmed[-1].components()) > 1 and
                                len(pd_points[j].components()) > 1 and
                                pd_points[j] not in substituted_points):
                            # This skips P_a,a situations
                            if pd_trimmed[-1].components() != pd_points[j].components():
                                # This conditions skips (P_a,b P_a,b) situations
                                substituted = False
                                p = 0
                                while substituted is not True and p != 2:
                                    q = 0
                                    while substituted is not True and q != 2:
                                        if pd_trimmed[-1].components()[p] == pd_points[j].components()[q]:
                                            pd_trimmed.append(Point(pd_trimmed[-1].components()[(p+1) % 2],
                                                                    pd_points[j].components()[(q+1) % 2]))
                                            del pd_trimmed[-2]
                                            substituted = True
                                            substituted_points.append(pd_points[j])
                                        q += 1
                                    p += 1
                            else:
                                # This deals with (P_a,b P_a,b) situations
                                pd_trimmed.append(Point(pd_trimmed[-1].components()[0],
                                                        pd_trimmed[-1].components()[0]))
                                del pd_trimmed[-2]
                                substituted_points.append(pd_points[j])
                    if pd_trimmed_old == pd_trimmed:
                        totally_simplified = True
        return pd_trimmed

    def writhe(self):
        crossings = [x for x in self if type(x) == Crossing]
        total_writhe = 0
        for crossing in crossings:
            total_writhe += crossing.sign()
        return total_writhe

    def jones_polynomial(self, **kwargs):
        root_of_unity = kwargs.get('root_of_unity')
        if root_of_unity is not None:
            A = root_of_unity
            A **= 1/4
        else:
            import sympy as sym
            A = sym.var('A')
            q = sym.var('q')
        split_diagram = kauffman_all_crossings(self)
        replacement = -A**2 - A**-2
        jones_precursor = 0
        for diagram in split_diagram:
            jones_precursor += A**diagram[0] * replacement**len(diagram[1])
        jones_poly = (-A**3)**self.writhe() * jones_precursor / replacement
        if root_of_unity is None:
            return sym.expand(sym.simplify(jones_poly)).subs(A, q**0.25)
        else:
            return jones_poly

    def jones_optimised(self, **kwargs):
        '''
        Calculates the Jones polynomial of the :class:PlanarDiagram using the optimisations
        of the Mathematica package KnotTheory as detailed on the Knot Atlas website

        Will not work on PlanarDiagrams with Points
        '''
        root_of_unity = kwargs.get('root_of_unity')
        if root_of_unity is not None:
            if root_of_unity == -1:
                root_of_unity = 2
            root = n.exp(2 * n.pi * 1.j / root_of_unity)
            root = root.real.round(3) + root.imag.round(3)*1.j
            A = (root + 0j) ** 0.25
        else:
            import sympy as sym
            A = sym.var('A')
            q = sym.var('q')

        crossings = crossings_connectedness_order(self)
        if len(crossings) < 2:
            return 1

        if root_of_unity is None:

            web = []
            crossing = crossings[0]
            crossing = PlanarDiagram(crossing)
            diag_1, diag_2 = kauffman_skein(crossing)
            web.append([diag_1, [1, 0, 1]])
            web.append([diag_2, [1, 0, -1]])


            for crossing in crossings[1:]:
                crossing = PlanarDiagram(crossing)
                diag_1, diag_2 = kauffman_skein(crossing)
                new_web = []

                for term in web:
                    diag_1_product = PlanarDiagram([x for x in diag_1] + [x for x in term[0]]).contract_points()
                    diag_2_product = PlanarDiagram([x for x in diag_2] + [x for x in term[0]]).contract_points()
                    contracted_1 = 0
                    contracted_2 = 0
                    diag_1_new = []
                    diag_2_new = []

                    for point in diag_1_product:
                        if len(point.components()) == 1:
                            contracted_1 += 1
                        else:
                            diag_1_new.append(point)
                    for point in diag_2_product:
                        if len(point.components()) == 1:
                            contracted_2 += 1
                        else:
                            diag_2_new.append(point)

                    new_term_1 = []
                    new_term_2 = []
                    for entry in term[1:]:
                        new_term_1.append([entry[0], entry[1] + contracted_1, entry[2] + 1])
                        new_term_2.append([entry[0], entry[1] + contracted_2, entry[2] - 1])

                    new_term_1 = [sorted(diag_1_new)] + contract_exponents(new_term_1)
                    new_term_2 = [sorted(diag_2_new)] + contract_exponents(new_term_2)

                    new_web.append(new_term_1)
                    new_web.append(new_term_2)

                unique_diags = list(set([tuple(x[0]) for x in new_web]))
                contracted_web = [[list(x)] for x in unique_diags]

                for term in new_web:
                    for diag in contracted_web:
                        if diag[0] == term[0]:
                            diag += term[1:]

                contracted_web_2 = []
                for x in contracted_web:
                    diagram = x[0]
                    exponents = contract_exponents(x[1:])
                    to_append = [diagram] + exponents
                    contracted_web_2.append(to_append)

                web = contracted_web_2

            replacement = -A**2 - A**-2
            jones_precursor = 0
            for term in web[0][1:]:
                jones_precursor += term[0] * replacement**term[1] * A**term[2]
            jones_poly = (-A**3)**self.writhe() * jones_precursor / replacement

            return sym.expand(sym.simplify(jones_poly)).subs(A, q**0.25)
        else:
            web = []
            crossing = crossings[0]
            crossing = PlanarDiagram(crossing)
            diag_1, diag_2 = kauffman_skein(crossing)
            web.append([diag_1, A])
            web.append([diag_2, 1.0/A])
            replacement = -A**2 - A**-2

            for crossing in crossings[1:]:
                crossing = PlanarDiagram(crossing)
                diag_1, diag_2 = kauffman_skein(crossing)
                new_web = []

                for term in web:
                    diag_1_product = PlanarDiagram([x for x in diag_1] + [x for x in term[0]]).contract_points()
                    diag_2_product = PlanarDiagram([x for x in diag_2] + [x for x in term[0]]).contract_points()
                    contracted_1 = 0
                    contracted_2 = 0
                    diag_1_new = []
                    diag_2_new = []

                    for point in diag_1_product:
                        if len(point.components()) == 1:
                            contracted_1 += 1
                        else:
                            diag_1_new.append(point)
                    for point in diag_2_product:
                        if len(point.components()) == 1:
                            contracted_2 += 1
                        else:
                            diag_2_new.append(point)

                    new_term_1 = [sorted(diag_1_new)] + [term[1] * (replacement ** contracted_1) * A]
                    new_term_2 = [sorted(diag_2_new)] + [term[1] * (replacement ** contracted_2) * 1.0/A]

                    new_web.append(new_term_1)
                    new_web.append(new_term_2)

                unique_diags = list(set([tuple(x[0]) for x in new_web]))
                contracted_web = [[list(x)] for x in unique_diags]

                for term in new_web:
                    for diag in contracted_web:
                        if diag[0] == term[0]:
                            if len(diag) == 1:
                                diag.append(term[1])
                            else:
                                diag[1] += term[1]

                web = contracted_web

            jones_precursor = web[0][1]
            jones_poly = (-A**3)**self.writhe() * jones_precursor / replacement

            return round(abs(jones_poly))


class Crossing(list):
    '''
    A single crossing in a planar diagram. Each :class:`PlanarDiagram`
    is a list of these.

    Parameters
    ----------
    a : int or None
        The first entry in the list of lines meeting at this Crossing.
    b : int or None
        The second entry in the list of lines meeting at this Crossing.
    c : int or None
        The third entry in the list of lines meeting at this Crossing.
    d : int or None
        The fourth entry in the list of lines meeting at this Crossing.
    '''

    def __init__(self, a=None, b=None, c=None, d=None):
        super(Crossing, self).__init__()
        self.extend([a, b, c, d])

    def valid(self):
        '''
        True if all intersecting lines are not None.
        '''
        if all([entry is not None for entry in self]):
            return True
        return False

    def components(self):
        '''
        Returns a de-duplicated list of lines intersecting at this Crossing.

        :rtype: list
        '''
        return list(set(self))

    def __str__(self):
        return 'X_{{{0},{1},{2},{3}}}'.format(
            self[0], self[1], self[2], self[3])

    def __repr__(self):
        return self.__str__()

    def as_mathematica(self):
        '''
        Get a string of mathematica code that can represent the Crossing
        in mathematica's knot library.

        The mathematica code won't be valid if any lines of self are None.

        :rtype: str
        '''
        return 'X[{}, {}, {}, {}]'.format(
            self[0], self[1], self[2], self[3])

    def __hash__(self):
        return tuple(self).__hash__()

    def update_line_number(self, old, new):
        '''
        Replaces all instances of the given line number in self.

        Parameters
        ----------
        old : int
            The old line number
        new : int
            The number to replace it with
        '''
        for i in range(4):
            if self[i] == old:
                self[i] = new

    def sign(self):
        check = self[1] - self[3]
        if check == 1 or check < -1:
            return 1
        else:
            return -1


class Point(list):
    '''
    A bivalent vertex in a planar diagram. These are formed when a
    crossing is smoothed and indicate which previously distinct semi-
    arcs are now the same.

    Parameters
    ----------
    a : int or None
        The first entry in the list of lines meeting at this BiVertex.
    b : int or None
        The second entry in the list of lines meeting at this BiVertex.
    '''

    def __init__(self, a=None, b=None):
        super(Point, self).__init__()
        self.extend(sorted([a, b]))

    def valid(self):
        '''
        True if all intersecting lines are not None.
        '''
        if all([entry is not None for entry in self]):
            return True
        return False

    def components(self):
        '''
        Returns a de-duplicated list of lines intersecting at this Crossing.

        :rtype: list
        '''
        return list(set(self))

    def __str__(self):
        return 'P_{{{0},{1}}}'.format(
            self[0], self[1])

    def __repr__(self):
        return self.__str__()

    #def as_mathematica(self):
    #    '''
    #    Get a string of mathematica code that can represent the Crossing
    #    in mathematica's knot library.

    #    The mathematica code won't be valid if any lines of self are None.

    #    :rtype: str
    #    '''
    #    return 'P[{}, {}]'.format(
    #        self[0], self[1])

    def __hash__(self):
        return tuple(self).__hash__()

    def update_line_number(self, old, new):
        '''
        Replaces all instances of the given line number in self.

        Parameters
        ----------
        old : int
            The old line number
        new : int
            The number to replace it with
        '''
        for i in range(2):
            if self[i] == old:
                self[i] = new


def shorthand_to_crossings(s):
    '''
    Takes a planar diagram shorthand string, and returns a list of
    :class:`Crossing`s.
    '''
    crossings = []
    cs = s.split(' ')
    for entry in cs:
        entry = entry.split('_')
        if entry[0] == 'X':
            a, b, c, d = [int(j) for j in entry[1].split(',')]
            crossings.append(Crossing(a, b, c, d))
        elif entry[0] == 'P':
            a, b = [int(j) for j in entry[1].split(',')]
            crossings.append(Point(a, b))
    return crossings


def gausscode_to_crossings(gc):
    cl = gc._gauss_code
    crossings = []
    incomplete_crossings = {}
    line_lengths = [len(line) for line in cl]
    total_lines = sum(line_lengths)
    line_indices = [1] + list(n.cumsum(line_lengths)[:-1] + 1)

    curline = 1
    for i, line in enumerate(cl):
        curline = line_indices[i]
        for index, over, clockwise in line:
            if index in incomplete_crossings:
                crossing = incomplete_crossings.pop(index)
            else:
                crossing = Crossing()

            inline = curline
            curline += 1
            if curline >= (line_indices[i] + line_lengths[i]):
                curline = line_indices[i]
            outline = curline

            if over == -1:
                crossing[0] = inline
                crossing[2] = outline
                crossings.append(crossing)
            else:
                if clockwise == 1:
                    crossing[3] = inline
                    crossing[1] = outline
                else:
                    crossing[1] = inline
                    crossing[3] = outline

            if not crossing.valid():
                incomplete_crossings[index] = crossing

    return crossings

def kauffman_skein(planar_diagram, **kwargs):
    '''
    Performs Kauffman's skein relation on the given planar diagram. For
    a given crossing, this is X_a,b,c,d -> A P_a,d P_b,c + A^-1 P_a,b P_c,d.
    The A's here are ignored.

    The two planar diagrams returned are in the order P_a,d P_b,c then
    P_a,b P_c,d and have their :class:`Point`s contracted according to
    contract_points
    '''
    crossing_components = kwargs.get('crossing_components')
    crossing_number = kwargs.get('crossing_number')
    if crossing_components is not None:
        component = planar_diagram.index(Crossing(crossing_components[0],
                                         crossing_components[1],
                                         crossing_components[2],
                                         crossing_components[3]))
    elif crossing_number is not None:
        pd_crossings = [x for x in planar_diagram if type(x) == Crossing]
        crossing = pd_crossings[crossing_number]
        component = planar_diagram.index(crossing)
    else:
        seeking_crossing = True
        component = 0
        while seeking_crossing:
            if type(planar_diagram[component]) is Crossing:
                seeking_crossing = False
            else:
                component += 1
    import copy
    planar_diagram_1 = copy.copy(planar_diagram)
    planar_diagram_2 = copy.copy(planar_diagram)
    del planar_diagram_1[component]
    del planar_diagram_2[component]

    planar_diagram_1.append(Point(planar_diagram[component][0],
                                  planar_diagram[component][3]))
    planar_diagram_1.append(Point(planar_diagram[component][1],
                                  planar_diagram[component][2]))
    planar_diagram_2.append(Point(planar_diagram[component][0],
                                  planar_diagram[component][1]))
    planar_diagram_2.append(Point(planar_diagram[component][2],
                                  planar_diagram[component][3]))
    if type(planar_diagram) == PlanarDiagram:
        return planar_diagram_1.contract_points(), planar_diagram_2.contract_points()
    else:
        return planar_diagram_1, planar_diagram_2

def kauffman_all_crossings(planar_diagram):
    #pd_crossings = [x for x in planar_diagram if type(x) == Crossing]
    pd_crossings = crossings_connectedness_order(planar_diagram)
    crossing_components = [pd_crossings[0][0], pd_crossings[0][1],
                           pd_crossings[0][2], pd_crossings[0][3]]
    pd_1, pd_2 = (
        kauffman_skein(planar_diagram, crossing_components=crossing_components))
    split_diagram = [[1, pd_1], [-1, pd_2]]
    #print 1, pd_crossings[0]
    i = 2
    for crossing in pd_crossings[1:]:
        new_split_diagram = []
        #print i, crossing
        i += 1
        for diagram in split_diagram:
            coeff_1 = diagram[0] + 1
            coeff_2 = diagram[0] - 1
            crossing_components = [crossing[0], crossing[1],
                                   crossing[2], crossing[3]]
            new_pd_1, new_pd_2 = (
                kauffman_skein(diagram[1], crossing_components=crossing_components))
            new_split_diagram.append([coeff_1, new_pd_1])
            new_split_diagram.append([coeff_2, new_pd_2])
        split_diagram = new_split_diagram
    return split_diagram

def crossings_connectedness_order(planar_diagram):
    crossings = [x for x in planar_diagram if type(x) == Crossing]

    inner_components = crossings[0].components()
    crossings_remaining = crossings[1:]
    ordered_crossings = [crossings[0]]

    for i in range(len(crossings_remaining)):
        connectedness = []
        for crossing in crossings_remaining:
            new_components = (len(list(set(crossing.components() + inner_components))) -
                              len(inner_components))

            connectedness.append(len(crossing.components()) - new_components)
        most_connected_index = connectedness.index(max(connectedness))
        inner_components += crossings_remaining[most_connected_index].components()
        inner_components = list(set(inner_components))
        ordered_crossings.append(crossings_remaining[most_connected_index])
        del crossings_remaining[most_connected_index]

    return ordered_crossings

def contract_points(planar_diagram):
    '''
    For appropriately contracting :class: `Points` in a
    :class: `PlanarDiagram` According to the following rules:

    P_a,b P_b,c -> P_a,c
    P_a,b P_a,b -> P_a,a
    '''
    import copy

    pd_crossings = [x for x in planar_diagram if type(x) == Crossing]
    pd_points = [x for x in planar_diagram if type(x) == Point]

    pd_trimmed = PlanarDiagram()
    for crossing in pd_crossings:
        pd_trimmed.append(crossing)

    substituted_points = []
    for i in range(len(pd_points)):
        if pd_points[i] not in substituted_points:
            pd_trimmed.append(pd_points[i])
            totally_simplified = False
            while not totally_simplified:
                pd_trimmed_old = copy.copy(pd_trimmed)
                for j in range(i+1, len(pd_points)):
                    if (len(pd_trimmed[-1].components()) > 1 and
                            len(pd_points[j].components()) > 1 and
                            pd_points[j] not in substituted_points):
                        # This skips P_a,a situations
                        if pd_trimmed[-1].components() != pd_points[j].components():
                            # This conditions skips (P_a,b P_a,b) situations
                            substituted = False
                            p = 0
                            while substituted is not True and p != 2:
                                q = 0
                                while substituted is not True and q != 2:
                                    if pd_trimmed[-1].components()[p] == pd_points[j].components()[q]:
                                        pd_trimmed.append(Point(pd_trimmed[-1].components()[(p+1) % 2],
                                                                pd_points[j].components()[(q+1) % 2]))
                                        del pd_trimmed[-2]
                                        substituted = True
                                        substituted_points.append(pd_points[j])
                                    q += 1
                                p += 1
                        else:
                            # This deals with (P_a,b P_a,b) situations
                            pd_trimmed.append(Point(pd_trimmed[-1].components()[0],
                                                    pd_trimmed[-1].components()[0]))
                            del pd_trimmed[-2]
                            substituted_points.append(pd_points[j])
                if pd_trimmed_old == pd_trimmed:
                    totally_simplified = True
    return pd_trimmed

def contract_exponents(exponents_array):
    '''
    Takes a set of exponents of the form [[x1, y1, z1], [x2, y2, z2], ...] where,
    given a Jones polynomial state such as (-A^2 - A^-2)^y * A^z * (P_1,2 P_3,4)
    the y's and z's are the exponents shown and x is the number of terms with equal
    y, z and point collection.

    This functions gathers like terms and returns an array of the same form
    '''
    unique_yz = list(set([tuple(x[1:]) for x in exponents_array]))
    unique_yz = [list(x) for x in unique_yz]

    contracted_exponents = []

    for yzs in unique_yz:
        total = 0
        for terms in exponents_array:
            if terms[1:] == yzs:
                total += terms[0]
        contracted_exponents.append([total, yzs[0], yzs[1]])

    return contracted_exponents

