
import numpy as n
cimport numpy as n
cimport cython

from pyknot2.utils import vprint

from pyknot2.writhes import validate_diagram

@cython.wraparound(False)
@cython.boundscheck(False)
def writhing_numbers_cython(gc, diagrams, based=False):

    if not isinstance(diagrams, (list, tuple)):
        diagrams = [diagrams]

    for d in diagrams:
        validate_diagram(d)

    level = 0

    code = gc._gauss_code
    code = code[0]
    gc_len = len(gc)
    code_len = len(code)
    from pyknot2.invariants import _crossing_arrows_and_signs
    arrows, signs = _crossing_arrows_and_signs(code, gc.crossing_numbers)

    crossing_numbers = list(gc.crossing_numbers)

    # degrees = [len(diagram.split(',')) for diagram in diagrams]

    degrees = defaultdict(lambda: [])
    for diagram in diagrams:
        degrees[len(diagram.split(',')) // 2].append(diagram)

    relations = {diagram: [] for diagram in diagrams}
    for diagram in diagrams:
        degree = len(diagram.split(',')) // 2
        num_relations = factorial(degree - 1) * 4

        terms = diagram.split(',')
        numbers = [term[:-1] for term in terms]

        number_strs = list(sorted(set(numbers), key=lambda j: int(j)))
        for i, number in enumerate(number_strs):
            for oi, other_number in enumerate(number_strs[i+1:]):
                oi += i + 1
                if i != 0:
                    if terms.index(number + '-') < terms.index(other_number + '-'):
                        relations[diagram].append(lambda l, i=i, oi=oi: l[i][0] < l[oi][0])
                    else:
                        relations[diagram].append(lambda l, i=i, oi=oi: l[i][0] > l[oi][0])

                    if terms.index(number + '-') < terms.index(other_number + '+'):
                        relations[diagram].append(lambda l, i=i, oi=oi: l[i][0] < l[oi][1])
                    else:
                        relations[diagram].append(lambda l, i=i, oi=oi: l[i][0] > l[oi][1])

                if terms.index(number + '+') < terms.index(other_number + '-'):
                    relations[diagram].append(lambda l, i=i, oi=oi: l[i][1] < l[oi][0])
                else:
                    relations[diagram].append(lambda l, i=i, oi=oi: l[i][1] > l[oi][0])

                if i == 0:
                    if terms.index(number + '+') < terms.index(other_number + '+'):
                        relations[diagram].append(lambda l, i=i, oi=oi: l[i][1] < l[oi][1])
                    else:
                        relations[diagram].append(lambda l, i=i, oi=oi: l[i][1] > l[oi][1])


    max_degree = max(degrees.keys())

    used_sets = set()

    # representations_sums = [0 for _ in diagrams]
    representations_sums = {d: 0 for d in diagrams}
    used_sets = {d: set() for d in diagrams}

    print('arrows are', arrows)

    try:
        num_combs = (factorial(len(crossing_numbers)) //
                     factorial(max_degree) //
                     factorial(len(crossing_numbers) - max_degree))
    except ValueError:
        num_combs = 0

    combs = combinations(crossing_numbers, max_degree)

    counter = n.zeros(max_degree)
    arrows = 
    while counter[0] < max_degree:
        
    for ci, comb in enumerate(combs):
        if ci % 10000 == 0:
            vprint('\rCombination {} of {}    '.format(ci + 1, num_combs),
                   newline=False)

        if based:
            perms = [comb]
        else:
            perms = permutations(comb)

        ordered_indices = tuple(sorted(comb))
        for diagram in diagrams:
            if ordered_indices not in used_sets[diagram]:
                break
        else:
            continue

        for perm in perms:
            cur_arrows = [list(arrows[i]) for i in perm]

            a1s = cur_arrows[0][0]
            if based:
                a1s = 0

            for i, arrow in enumerate(cur_arrows):
                arrow[0] = (arrow[0] - a1s) % code_len
                arrow[1] = (arrow[1] - a1s) % code_len


            for diagram in diagrams:
                if ordered_indices in used_sets[diagram]:
                    continue
                for relation in relations[diagram]:
                    if not relation(cur_arrows):
                        break
                else:
                    representations_sums[diagram] += (
                        reduce(lambda x, y: x*y,
                               [signs[arrow_i] for arrow_i in perm]))
                    used_sets[diagram].add(ordered_indices)
                        
    vprint()

    return representations_sums
