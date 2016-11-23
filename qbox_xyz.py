#!/usr/bin/python
# Copyright 2016 The Regents of the University of California
# This file is part of Qbox
#
# qbox_xyz.py: extract first (or all) set(s) of atomic positions in xyz format
# from a Qbox output file or from a Qbox sample file using SAX 
# incremental parsing
#
# use: qbox_xyz.py [-all] {file|URL}
import os.path
import xml.sax
import sys
import urllib2
from sax_handler import QboxOutputHandler

class QBox_XYZ(object):
  def __init__(self, allOrFirst, inputSource):
    self.allOrFirst = allOrFirst
    self.input_source = inputSource
    
  def process(self):
    first_only = True
    if self.allOrFirst == 'a':
      first_only = False

    print 'Now parsing file .....'

    parser = xml.sax.make_parser()
    handler = QboxOutputHandler()
    parser.setContentHandler(handler)
    
    # test if input_source is a local file
    # if not, process as a URL
    if ( os.path.isfile(self.input_source) ):
      file = open(self.input_source)
      s = file.read(8192)
      while ( s !="" and not (first_only and handler.done_first) ):
        parser.feed(s)
        s = file.read(8192)
      file.close()
    else:
      # attempt to open as a URL
      try:
        f = urllib2.urlopen(self.input_source)
        s = f.read(8192)
        while ( s !="" and not (first_only and handler.done_first) ):
          parser.feed(s)
          s = f.read(8192)
        f.close()
      except (ValueError,urllib2.HTTPError) as e:
        print e
        sys.exit()

    parser.reset()

    #print 'Finished processing....'
    data = handler.output
    return data


