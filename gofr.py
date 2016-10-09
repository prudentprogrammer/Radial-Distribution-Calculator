import unitcell
import sys
from math import sqrt, pi, pow

if __name__ == "__main__":
  if len(sys.argv) != 5:
    print 'use: gofr name1 name2 rmax dr < file.xyz > g.dat'
    sys.exit(1)
  
  name1 = sys.argv[1]
  name2 = sys.argv[2]
  rmax = float(sys.argv[3])
  dr = float(sys.argv[4])
  nconfig = 0
  
  # This list holds the position of the atoms
  tau = []
  names_of_atoms = []
  
  # Corresponds to the first atom
  isp1 = []
  # Corresponds to the second atom
  isp2 = []
  line_index = 0
  
  # Store the file contents in the list
  file_content = [x.strip() for x in sys.stdin.readlines()]
  
  # Read the number of atoms in the first line
  number_atoms = int(file_content[line_index])
  line_index += 1
  
  nbin = (int) (rmax / dr)
  print 'Number of bins = ', nbin
  
  count = [0.0] * nbin
  omega = 0.0
  
  # Loop through the file contents line by line
  while line_index < len(file_content):
    nconfig += 1
    
    line_clean = file_content[line_index].split()

    # The iteration number
    iteration = line_clean[0]
    # The D3 vectors
    a0 = [float(x) for x in line_clean[1:4]]
    a1 = [float(x) for x in line_clean[4:7]]
    a2 = [float(x) for x in line_clean[7:10]]
    #print a0, a1, a2
    line_index += 1

    uc = unitcell.UnitCell(a0, a1, a2)
    omega = uc.getVolume()
    print 'Number atoms = ' , number_atoms
    print 'Volume = ', omega
    
    for i in range(number_atoms):
      line_clean = file_content[line_index].split()
      line_index += 1
      
      nm = line_clean[0]
      d3_vec = [float(x) for x in line_clean[1:4]]
      #print nm
      #print d3_vec
      tau.append(d3_vec)
    
      names_of_atoms.append(nm)
      if name1 in nm:
        isp1.append(i)
      if name2 in nm:
        isp2.append(i)
        
    print 'isp1 = ', len(isp1)
    print 'isp2 = ', len(isp2) 
    
       
    for i in range(len(isp1)):
      for j in range(len(isp2)):
        first_vector = tau[isp1[i]]
        second_vector = tau[isp2[j]]
        difference_vector = [ai - bi for ai, bi in zip(first_vector, second_vector)]
        print 'diff = ', difference_vector
        difference_vector = uc.fold_in_ws(difference_vector)
        print 'p = ', difference_vector
        
        scaled_vec = [x / dr for x in difference_vector]
        length_scaled_vec = sqrt(scaled_vec[0] ** 2 + scaled_vec[1] ** 2 + scaled_vec[2] ** 2)
        print 'scaled vec = ', scaled_vec
        print 'length scaled vec ', length_scaled_vec
        k = (int) (length_scaled_vec + 0.5)
        if k < nbin:
          count[k] += 1
    
    #print 'line_index = ' , line_index
    if line_index < len(file_content):
      number_atoms = int(file_content[line_index])
      line_index += 1
  
  print 'nconfig = ', nconfig
  
  if len(isp1) == 0:
    print ' no atoms %s found.' % name1
    sys.exit(1)
  if len(isp2) == 0:
    print ' no atoms %s found.' % name2
    sys.exit(1)
  
  print '%d %s atoms found.' % (len(isp1), name1)
  print '%d %s atoms found.' % (len(isp2), name2)
  
  # normalization differs for same species vs different species
  npairs = 0
  if name1 == name2:
    npairs = len(isp1) * (len(isp2) - 1)
  else:
    npairs = len(isp1) * len(isp2)
    
  for i in range(1, nbin):
    r = i * dr
    rmin = (i - 0.5) * dr
    rmax = (i + 0.5) * dr
    vshell = (4.0 * pi / 3.0) * (pow(rmax, 3.0) - pow(rmin, 3.0))
    count_id = vshell * nconfig * npairs / omega
    g = count[i] / count_id
    print r, g
  
  n = 0.0
  for i in range(1, nbin):
    r = i * dr
    n += count[i] / (len(isp1) * nconfig)
    print 'r, n = %s, %s' % (r, n)
  

