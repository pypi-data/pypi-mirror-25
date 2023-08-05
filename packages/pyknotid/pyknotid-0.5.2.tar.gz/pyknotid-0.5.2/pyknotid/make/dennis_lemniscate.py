
import numpy as n
import itertools

def plain_lemniscate(bulbs, strands, repeats, numpoints=200):
    """Return sets of numpoints describing the space curve(s) obtained
    via the lemniscate construction.

    """

    ps = []

    xs = n.linspace(0, 2*n.pi * repeats, numpoints)
    ys = n.linspace(0, 2*n.pi * bulbs * repeats, numpoints)
    angles = n.linspace(0, 2*n.pi*strands, numpoints)

    for i in range(numpoints):
        r = 80 + 50*n.cos(xs[i])
        angle = angles[i]

        realx = r*n.cos(angle)
        realy = r*n.sin(angle)
        realz = 20*n.sin(ys[i])
        ps.append([realx, realy, realz])

    return n.array(ps)
    
def complex_lemniscate(strands=5, repeats=1, numpoints=200):
    '''Return sets of numpoints describing the space curve(s) obtained by
    a multidimensional lemniscate construction.

    '''

    ts = n.linspace(0, 2*n.pi*repeats, numpoints)
    xs = n.sin(2*ts)
    ys = n.sin(3*ts)

    angles = n.linspace(0, 2*n.pi*strands, numpoints)
    
    ps = []
    for i in range(numpoints):
        r = 80 + 50*xs[i]
        angle = angles[i]

        realx = r*n.cos(angle)
        realy = r*n.sin(angle)
        realz = 20*n.sin(ys[i])
        ps.append([realx, realy, realz])

    ps = n.array(ps)
    ps[-1] *= 0.99

    return ps
