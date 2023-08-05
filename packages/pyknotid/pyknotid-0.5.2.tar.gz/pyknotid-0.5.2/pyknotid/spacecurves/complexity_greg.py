from __future__ import print_function
from numpy import roll, zeros, cross, sqrt, sum, arcsin, isnan, pi


def higher_order_writhe_integral(points, order=(1, 3, 2, 4)):

    # The writhe contributions from each pair of segments
    # This is a matrix with side length the number of points in the curve
    contributions = zeros((len(points), len(points)))

    # This is just bookkeeping to ensure that the order of the writhe
    # comparison consists of the numbers 1 to 4
    assert len(set(order)) == len(order)
    assert set(order) == set((1, 2, 3, 4))
    order = [o - 1 for o in order]

    # First, we calculate the contribution to the writhe from every
    # pair of segments in the curve.
    for i1 in range(len(points) - 3):
        p1 = points[i]
        p2 = points[i1 + 1]
        for i2 in range(i1 + 2, len(points) - 1):
            p3 = points[i2]
            p4 = points[i2 + 1]

            # The algorithm here is just as from wikipedia

            r12 = p2 - p1
            r13 = p3 - p1
            r14 = p4 - p1
            r23 = p3 - p2
            r24 = p4 - p2
            r34 = p4 - p3

            n1 = cross(r13, r14)
            n1 /= sqrt(sum(n1**2))

            n2 = cross(r14, r24)
            n2 /= sqrt(sum(n2**2))

            n3 = cross(r24, r23)
            if any(abs(n3) > 0.):
                n3 /= sqrt(sum(n3**2))

            n4 = cross(r23, r13)
            if any(abs(n4) > 0.):
                n4 /= sqrt(sum(n4**2))

            # When the vectors are nearly the same, floating point
            # errors can apparently sometimes make the output a tiny
            # bit higher than 1. This code forces bounds on the
            # resulting values.
            t1, t2, t3, t4 = clip([n1.dot(n2),
                                   n2.dot(n3),
                                   n3.dot(n4),
                                   n4.dot(n1)],
                                  -1, 1)

            writhe_contribution = (arcsin(t1) +
                                   arcsin(t2) +
                                   arcsin(t3) +
                                   arcsin(t4))

            writhe_contribution *= sign(cross(r34, r12).dot(r13))
    
            contributions[i1, i2] = writhe_contribution
            contributions[i2, i1] = writhe_contribution

    # Now we can calculate the higher order writhe.

    writhe = 0.0

    for i1 in range(len(points) - 3):
        for i2 in range(i1 + 1, len(points) - 1):
            for i3 in range(i2 + 1, len(points) - 1):
                for i4 in range(i3 + 1, len(points) - 1):
                    indices = (i1, i2, i3, i4)

                    writhe += (contributions[indices[order[0]],
                                             indices[order[1]]] *
                               contributions[indices[order[2]],
                                             indices[order[3]]])
    print()

    return writhe / (2*pi)**2
