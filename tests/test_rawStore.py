from __future__ import print_function
import sys, unittest
from descriptastorus import raw
import os, shutil, numpy, random, time

class TestCast(unittest.TestCase):
    directory = "mydir4"
    
    def startUp(self):
        if os.path.exists(self.directory):
            shutil.rmtree(self.directory)
    def tearDown(self):
        if os.path.exists(self.directory):
            shutil.rmtree(self.directory)

    def atestStore(self):
        counts = [("m3%d"%d, numpy.uint8) for d in range(2048)]
        rddescriptors = [("rd%d"%d, numpy.float64) for d in range(20)]
        cols = counts + rddescriptors

        N=4000
        t1 = time.time()
        s = raw.MakeStore(cols, N, self.directory)
        print (time.time()-t1, "seconds to make the raw storage")

        t1 = time.time()
        for i in range(N):
            if i % 100000 == 0:
                print (i, time.time()-t1)
            row = tuple([i%256] * len(counts) + [float(i)]*len(rddescriptors))
            s.putRow(i, row)
            self.assertEqual(s.get(i), row)

        for x in range(10000):
            i = random.randint(0,N)
            row = s.get(i)
            self.assertEqual(row,  tuple([i%256] * len(counts) + [float(i)]*len(rddescriptors)))
        s.close()
        
if __name__ == '__main__':  #pragma: no cover
    unittest.main()

        
