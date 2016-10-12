import unitcell
import sys
from math import sqrt, pi, pow
from qbox_xyz import QBox_XYZ
import gofr_config as gc
from gofr import Gofr

if __name__ == "__main__":
  x = QBox_XYZ(gc.all_or_first, gc.input_source)
  output = x.process()
  #output = [x.strip() for x in output]
  output =  (' '.join(output))
  output = output.split("\n")
  output = [x.strip() for x in output]
  output = [x for x in output if len(x) != 0]
  gofr_obj = Gofr(output, gc.first_molecule_name, gc.second_molecule_name, gc.rmax, gc.dr)
  gofr_obj.process()
  #print output

