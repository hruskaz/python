import numpy
import sys
from unittest import TestCase

def volume(*args):
    if type(args[0]) is not tuple:
        return 0
    dimension = len(args[0])
    points = []

    for arg in args:
        if type(arg) is not tuple:
            raise Exception("Bad input.")
        if(len(arg)!=dimension):
            raise Exception("Bad input.")
        points.append(arg)
    initialPoint = points[0]
    points.remove(initialPoint)
    vectors = []
    for point in points:
        newvect=[]
        for i in range(dimension):
            newvect.append(point[i]-initialPoint[i])
        vectors.append(newvect)	
    if len(vectors)!=(dimension):
        raise Exception("Bad input.")
    matrix = numpy.matrix(vectors)
    transposed = numpy.linalg.det(matrix.transpose())
    return numpy.abs(transposed/(numpy.math.factorial(dimension)))

#class TestMath(TestCase):
    def test_volume(self):
        self.assertAlmostEqual(volume((1,2),(4,1),(4,-1)),3)
        self.assertAlmostEqual(volume((0,0,0),(0,0,0),(0,0,0),(0,0,0)),0)
        self.assertAlmostEqual(volume((1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)), ((2*numpy.sqrt(2))**3)/(6*numpy.sqrt(2)))
        self.assertAlmostEqual(volume((0,0),(2,0),(1,numpy.sqrt(3))),numpy.sqrt(3),places=7)
        self.assertRaises(Exception, volume((1,1,1),(1,-1,1),(-1,1,-1)))
        self.assertRaises(Exception, volume((1,1,1),(1,-1,1),(-1,1,-1),(-1,-1)))
