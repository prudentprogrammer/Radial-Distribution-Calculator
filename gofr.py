import unitcell
import sys
from math import sqrt, pi, pow
import time
import pprint
from visualizer import visualizer

class Gofr(object):
  def __init__(self, xyzInput, name1, name2, rmax, dr):
    self.xyzInput = xyzInput
    self.name1 = name1
    self.name2 = name2
    self.rmax = rmax
    self.dr = dr
    
  def process(self):
    name1 = self.name1
    name2 = self.name2
    rmax = self.rmax
    dr = self.dr
    nconfig = 0
    cum_counts = {}
  
    # This list holds the position of the atoms
    line_index = 0
  
    # Store the file contents in the list
    file_content = self.xyzInput

    # Read the number of atoms in the first line
    number_atoms = int(file_content[line_index])
    # Corresponds to the first atom
    isp1 = [0] * number_atoms
    # Corresponds to the second atom
    isp2 = [0] * number_atoms
    
    tau = [None] * number_atoms
    names_of_atoms = [None] * number_atoms
    
    species_1_count = 0
    species_2_count = 0
    
    line_index += 1
  
    nbin = (int) (rmax / dr)
  
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

      line_index += 1

      uc = unitcell.UnitCell(a0, a1, a2)
      omega = uc.getVolume()
      #print 'Number atoms = ' , number_atoms
      #print 'Volume = ', omega
      
      
      for i in range(number_atoms):
        line_clean = file_content[line_index].split()
        line_index += 1
      
        nm = line_clean[0]
        d3_vec = [float(x) for x in line_clean[1:4]]
        tau[i] = d3_vec
        if nconfig == 1:
          names_of_atoms.append(nm)
          if name1 in nm:
            species_1_count += 1
            isp1[species_1_count] = i
          if name2 in nm:
            species_2_count += 1
            isp2[species_2_count] = i
      
          
      for i in range(species_1_count):
        for j in range(species_2_count):
          first_vector = tau[isp1[i]]
          second_vector = tau[isp2[j]]
          difference_vector = [ai - bi for ai, bi in zip(first_vector, second_vector)]
          
          difference_vector = uc.fold_in_ws(difference_vector)
          
          scaled_vec = [x / dr for x in difference_vector]
          
          length_scaled_vec = sqrt(scaled_vec[0] ** 2 + scaled_vec[1] ** 2 + scaled_vec[2] ** 2)
         
          k = (int) (length_scaled_vec + 0.5)
          #print k
          if k < nbin:
            count[k] += 1
       
      cum_counts[nconfig] = count 
       
       
      if line_index < len(file_content):
        number_atoms = int(file_content[line_index])
        line_index += 1
  
    print 'nconfig = ', nconfig
    
  
    if species_1_count == 0:
      print ' no atoms %s found.' % name1
      sys.exit(1)
    if species_2_count == 0:
      print ' no atoms %s found.' % name2
      sys.exit(1)
  
    print '%d %s atoms found.' % (species_1_count, name1)
    print '%d %s atoms found.' % (species_2_count, name2)
  
    #print cum_counts
    # Dump it to a file
    
    
    # normalization differs for same species vs different species
    npairs = 0
    if name1 == name2:
      npairs = species_1_count * (species_2_count - 1)
    else:
      npairs = species_1_count * species_2_count
    
    
    visual_data = []
    initial_data = ['NConfig', 'Radius', 'G(r)']
    visual_data.append(initial_data)
    counter = 0
    for key, val in cum_counts.items():
      #nth_config = []
      for i in range(1, nbin):
        r = i * dr
        rmin = (i - 0.5) * dr
        rmax = (i + 0.5) * dr
        vshell = (4.0 * pi / 3.0) * (pow(rmax, 3.0) - pow(rmin, 3.0))
        count_id = vshell * nconfig * npairs / omega
        g = val[i] / count_id
        temp_data = [counter, r, g]
        #nth_config.append(temp_data)
        #print r, g
        visual_data.append(temp_data )
      counter += 1
    vis_obj = visualizer(visual_data, nconfig) 
    vis_obj.generateVisualFile()
    print ('Done generating visual file!')
    #pprint.pprint(visual_data)
    #f = open('cum_count.txt','w+')
    #data_string = pprint.pformat(visual_data)
    #f.write(data_string)
    # for key, val in cum_counts.items():
#       length = str(len(val))
#       step = str(key)
#       counts = '\n'.join([str(x) for x in val])
#       f.write('%s %s\n' % (length, step))
#       f.write('%s\n' % (counts))
#       f.write('\n\n')
    
    
    n = 0.0
    for i in range(1, nbin):
      r = i * dr
      n += count[i] / (species_1_count * nconfig)
      print 'r, n = %s, %s' % (r, n)
    


