
import numpy as np

from pyknot2.representations.gausscode import GaussCode

class ArrowDiagram(GaussCode):
    pass

class GaussDiagram(GaussCode):
    pass


class ReidemeisterMove(object):
    def __init__(self):
        self.before = []
        self.after = []

        self.builtin_crossings = {1}

    def get_subdiagrams(max_arrows=

class ReidemeisterOne(ReidemeisterMove):
    def __init__(self):

        self.before = [GaussCode('1+a,1-a')]

        self.after = []

        self.builtin_crossings = {1}


class ReidemeisterTwoA(ReidemeisterMove):
    def __init__(self):

        self.before = [GaussCode('1+a,2+c'),
                       GaussCode('2-c,1-a')]

        self.after = []

        self.builtin_crossings = {1, 2}
        
class ReidemeisterTwoB(ReidemeisterMove):
    def __init__(self):
        
        self.before = [GaussCode('1+a,2+c'),
                       GaussCode('1-a,2-c')]

        self.after = []

        self.builtin_crossings = {1, 2}

class ReidemeisterThreeA(ReidemeisterMove):
    def __init__(self):

        self.before = [GaussCode('1-a,2+c'),
                       GaussCode('1+a,3+c'),
                       GaussCode('2-c,3-c')]

        self.after = [GaussCode('2+c,1-a'),
                      GaussCode('3+c,1+a'),
                      GaussCode('3-c,2-c')]

        self.builtin_crossings = {1, 2, 3}

class ReidemeisterThreeB(ReidemeisterMove):
    def __init__(self):

        self.before = [GaussCode('1+c,2-a'),
                       GaussCode('1-c,3-a'),
                       GaussCode('2+a,3+a')]

        self.after = [GaussCode('2-a,1+c'),
                      GaussCode('3-a,1-c'),
                      GaussCode('3+a,2+a')]

        self.builtin_crossings = {1, 2, 3}

