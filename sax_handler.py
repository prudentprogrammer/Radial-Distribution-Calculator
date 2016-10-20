import xml.sax

# conversion from Bohr to Angstrom
a0 = 0.529177

# Qbox output handler to extract and process data
class QboxOutputHandler(xml.sax.handler.ContentHandler):
  def __init__(self):
    self.step = 0
    self.inAtomset = 0
    self.inAtom = 0
    self.inPosition = 0
    self.done_first = False
    self.output = []

  def startElement(self, name, attributes):
    if name == "atomset":
      self.tau=[]
      self.atomname=[]
      self.inAtomset = 1
    elif (name == "unit_cell") & self.inAtomset:
      self.cell_a = attributes["a"]
      self.cell_b = attributes["b"]
      self.cell_c = attributes["c"]
    elif (name == "atom") & self.inAtomset:
      self.atomname.append(attributes["name"])
      self.inAtom = 1
    elif (name == "position") & self.inAtom:
        self.buffer = ""
        self.inPosition = 1

  def characters(self, data):
    if self.inPosition:
      self.buffer += data

  def endElement(self, name):
    if (name == "atom") and self.inAtomset:
      self.inAtom = 0
    if (name == "position") & self.inAtom:
      pos = self.buffer.split()
      x = a0*float(pos[0])
      y = a0*float(pos[1])
      z = a0*float(pos[2])
      self.tau.append([x,y,z])
      self.inPosition = 0
    elif name == "atomset":
      self.step += 1
      output = str(len(self.tau)) + "\n"
      avec = self.cell_a.split()
      bvec = self.cell_b.split()
      cvec = self.cell_c.split()
      
      temp = str(self.step),\
      '%.6f'%(a0*float(avec[0])),\
      '%.6f'%(a0*float(avec[1])),\
      '%.6f'%(a0*float(avec[2])),\
      '%.6f'%(a0*float(bvec[0])),\
      '%.6f'%(a0*float(bvec[1])),\
      '%.6f'%(a0*float(bvec[2])),\
      '%.6f'%(a0*float(cvec[0])),\
      '%.6f'%(a0*float(cvec[1])),\
      '%.6f'%(a0*float(cvec[2]))
      
      #print temp
      output += (' '.join(temp)) + "\n"
      
      for i in range(len(self.tau)):
         test_string = self.atomname[i],'%.6f'%self.tau[i][0],\
                               '%.6f'%self.tau[i][1],\
                               '%.6f'%self.tau[i][2]
         output += (' '.join(test_string)) + "\n"
      self.inAtomset = 0
      self.done_first = True
      self.output.append(output)
      
