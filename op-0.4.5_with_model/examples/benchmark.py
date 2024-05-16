from win32com.client import Dispatch
import sys
import time;

pic_name = "test.bmp"

def testFindPic(obj, rect, sim):
	t1 = time.clock()
	ret, x, y = obj.FindPic(0,0,2000,2000,pic_name,"000000", sim, 0)
	t2 = time.clock()
	t = t2 - t1
	print("first time = {}, ret ={}, position ={}, {}".format(t, ret, x, y))

	t1 = time.clock()
	ret, x, y = obj.FindPic(0,0,2000,2000,pic_name,"000000", sim, 0)
	t2 = time.clock()
	t = t2 - t1
	print("second time = {}, ret ={}, position ={}, {}".format(t, ret, x, y))


def benchmark():
	t1 = time.clock();
	op = Dispatch("op.opsoft");
	t2 = time.clock();
	print("time of create op: {}".format(t2 - t1))
	t1 = time.clock();
	dm = Dispatch("dm.dmsoft")
	t2 = time.clock();
	print("time of create dm: {}".format(t2 - t1))

	rect = [0, 0, 2000, 2000]
	sim = 1.0
	print("-----------------op sim = 1.0 ------------------")
	testFindPic(op, rect, sim)
	print("-----------------dm sim = 1.0 -----------------")
	testFindPic(dm, rect, sim)

	sim = 0.9
	print("-----------------op sim = 0.9 ------------------")
	testFindPic(op, rect, sim)
	print("-----------------dm sim = 0.9 ------------------")
	testFindPic(dm, rect, sim)


benchmark()