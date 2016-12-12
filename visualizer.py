#!/usr/bin/python
import pprint
import gofr_config as gc
import urllib2
import sys
import pprint
import os.path
import getopt
import csv


def handle_files(fp, source_file):
  fp = None
  # test if input_source is a local file
  # if not, process as a URL
  if ( os.path.isfile(source_file) ):
    fp = open(source_file)
  else:
    # attempt to open as a URL
    try:
      fp = urllib2.urlopen(source_file)
    except (ValueError,urllib2.HTTPError) as e:
      print 'Error opening the URL'
      sys.exit()
  
  return fp 



argc = len(sys.argv)

#if ( argc < 2 or argc > 3 ):
#  print "use: ", sys.argv[0]
#  sys.exit()
  
input_source = sys.argv[1]
print argc
try:
  opts, args = getopt.getopt(sys.argv[3:], "hx:y:", ["help", "xlim=", "ylim="])
except getopt.GetoptError:
  print 'visualizer.py counts.dat -x 4 -y 4'
  sys.exit(2)
  
#print opts
#print args
xlim = ''
ylim = ''
for o, a in opts:
    if o in ('-x', '--xlim'):
        xlim=a
    elif o in ('-y', '--ylim'):
        ylim=a
    else:
        print("Usage: %s -x 4 -y 4" % sys.argv[0])
     
print ("Input file : %s and output file: %s" % (xlim,ylim) )

#sys.exit(0)

#if ( argc < 2 or argc > 3 ):
#  print "use: ", sys.argv[0]
#  sys.exit()
  
input_source = sys.argv[1]
second_source = sys.argv[2]

print 'second_source', second_source


fp = None
fp = handle_files(fp, input_source)

vis_data = []
first_source_vals = {}
second_source_vals = {}
vis_data.append(['NConfig','Radius', 'Gr1', 'Gr2'])
rownum = 0
try:
  reader = csv.reader(fp) 
  for row in reader:
    if rownum != 0:
      key = row[0] + ',' + row[1]
      first_source_vals[key] = row[2]
      #float_list = [float(x) for x in row]
      #vis_data.append(float_list)
    rownum += 1
finally:
  fp.close()
  
fp = handle_files(fp, second_source)
rownum = 0
try:
  reader = csv.reader(fp) 
  for row in reader:
    if rownum != 0:
      try:
        key = row[0] + ',' + row[1]
        tempList = [float(row[0]), float(row[1]), float(first_source_vals[key]), float(row[2]) ]
        vis_data.append(tempList)
        #print key + ',' + first_source_vals[key] + ',' + row[2]
        #second_source[key] = row[2]
      except KeyError:
        continue
      #float_list = [float(x) for x in row]
      #vis_data.append(float_list)
    rownum += 1
finally:
  fp.close()

  
  
#pprint.pprint(vis_data)

class visualizer(object):

  def __init__(self, data, nconfig, xlim, ylim):
    self.data = data
    self.total_nconfigs = nconfig
    self.xlim = xlim
    self.ylim = ylim
    
  def generateVisualFile(self):
    htmlString = r"""
    <html>
      <head>
        <!--Load the AJAX API-->
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">

          // Load the Visualization API and the controls package.
          google.charts.load('current', {'packages':['corechart', 'controls', 'table']});

          // Set a callback to run when the Google Visualization API is loaded.
          google.charts.setOnLoadCallback(drawDashboard);

          // Callback that creates and populates a data table,
          // instantiates a dashboard, a range slider and a pie chart,
          // passes in the data and draws it.
          function drawDashboard() {

            // Create our data table.
            var data = google.visualization.arrayToDataTable(%s);

            // Create a dashboard.
            var dashboard = new google.visualization.Dashboard(document.getElementById('dashboard_div'));

            var imageLink = document.getElementById('image_link');
            // Create a range slider, passing some options
            var nConfigSlider = new google.visualization.ControlWrapper({
              'controlType': 'NumberRangeFilter',
              'containerId': 'filter_div',
              'options': {
                'filterColumnLabel': 'NConfig',
                "ui": {"label": "Frame Number"}
              }
             
            });
            
            var myLine = new google.visualization.ChartWrapper({
                'chartType' : 'LineChart',
                'containerId' : 'chart_div',
                'view': {'columns': [1, 2, 3]},

                'options': {
                  'title': 'g_%s%s(r)',
                  width: 1200, 
                  height: 800, 
                  pointSize: 5, 
                  lineWidth: 2,
                  hAxis: {viewWindow: {max: %s}, title: 'r (Angstrom)'},
                  vAxis: {viewWindow: {max: %s}, title: 'g(r)'}
                },
                'dataTable': data
            });
           
            var myTable = new google.visualization.ChartWrapper({
               'chartType' : 'Table',
               'containerId' : 'table_div',
               'width': 800,
               'height': 600,
             });
             
            
            dashboard.bind(nConfigSlider, myTable);
            // Establish dependencies, declaring that 'filter' drives 'pieChart',
            // so that the pie chart will only display entries that are let through
            // given the chosen slider range.
            dashboard.bind(nConfigSlider, myLine);

            // Draw the dashboard.
            dashboard.draw(data);
            
            google.visualization.events.addListener(nConfigSlider, 'ready', setInitialState);
            google.visualization.events.addListener(nConfigSlider, 'statechange', setInitialState);
            
            function setInitialState() {
              // Temporary Filtered Table
              var columnsTable = new google.visualization.DataTable();
              columnsTable.addColumn('number', 'nconfig');
              columnsTable.addColumn('number', 'Radius');
              columnsTable.addColumn('number', 'Gr1');
              columnsTable.addColumn('number', 'Gr2');
              
              // Get Slider Information
              var sliderState = nConfigSlider.getState();
              var leftValue = sliderState.lowValue;
              var rightValue = sliderState.highValue;
              
            
              // Corresponds to indices in original data Ex:- [5, 6, 7, 8, 9]
              var left_nconfigs = data.getFilteredRows([{column : 0, value: leftValue}]);
              var right_nconfigs = data.getFilteredRows([{column : 0, value: rightValue}]);
              
              for(var i = 0; i < left_nconfigs.length; i++) {
                var right_gofr_1 = data.getValue(right_nconfigs[i], 2);
                var left_gofr_1 =  data.getValue(left_nconfigs[i], 2); 
                
                var right_gofr_2 = data.getValue(right_nconfigs[i], 3);
                var left_gofr_2 =  data.getValue(left_nconfigs[i], 3); 
                columnsTable.addRow([leftValue, data.getValue(left_nconfigs[i], 1),(right_gofr_1-left_gofr_1)/(rightValue - leftValue),
              (right_gofr_2-left_gofr_2)/(rightValue - leftValue)]);
              }
              myLine.setDataTable(columnsTable);
              myLine.draw();
              
              //imageLink.innerHTML = '<img src="' + myLine.getChart().getImageURI() + '">';
              //console.log(imageLink.innerHTML);
            }
            
          }
        </script>
      </head>

      <body class="container">
        <!--Div that will hold the dashboard-->
        <div id="dashboard_div">
          <div id="info">
            NConfigs: %s <br /> 
            Radius: %s <br /> 
            Dr: %s <br />
            First Molecule Name: %s <br />
            Second Molecule Name: %s <br />
          </div>
          <!--Divs that will hold each control and chart-->
          <div id="filter_div"></div>
          <div id="chart_div"></div>
          <div id="display_div"></div>
          <div id="image_link"></div>
          <div id="table_div"><!-- Table renders here --></div>
          
          
        </div>
      </body>
    </html>
    """ % (pprint.pformat(self.data), gc.first_molecule_name, gc.second_molecule_name, self.xlim, self.ylim, str(self.total_nconfigs) , str(gc.rmax), str(gc.dr), str(gc.first_molecule_name), str(gc.second_molecule_name))
    
    f = open('sample_graph.html','w+')
    f.write(htmlString)




nconfig = vis_data[-1][0]
vis_obj = visualizer(vis_data, nconfig, xlim, ylim) 
vis_obj.generateVisualFile()
print ('Done generating visual file!')