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
  print 'sf = ', source_file
  if ( os.path.isfile(source_file) ):
    fp = open(source_file)
  else:
    # attempt to open as a URL
    try:
      fp = urllib2.urlopen(source_file)
    except (ValueError,urllib2.HTTPError) as e:
      print 'Error opening the URL'
      #sys.exit()
  
  return fp 


argc = len(sys.argv)
input_source1 = sys.argv[1]
input_source2 = ''


# ./visualizer.py cum_counts.txt 
# ./visualizer.py cum_counts.txt -x 5 -y 5
# ./visualizer.py cum_counts.txt cum_counts2.txt
# ./visualizer.py cum_counts.txt cum_counts2.txt -x 5 -y 5

if argc > 2:
  if sys.argv[2] == '':
    input_source2 = ''
  elif sys.argv[2] == '-x' or sys.argv[2] == '--x':
    input_source2 = ''
  # If it is a file
  elif ".txt" in sys.argv[2]:
    input_source2 = sys.argv[2]

print argc
print sys.argv


#sys.exit(0)

try:
  if input_source2 == '':
    opts, args = getopt.getopt(sys.argv[2:], "hx:y:", ["help", "xlim=", "ylim="])
  else:
    opts, args = getopt.getopt(sys.argv[3:], "hx:y:", ["help", "xlim=", "ylim="])
except getopt.GetoptError:
  print 'visualizer.py counts.dat -x 4 -y 4'
  sys.exit(2)
  
print opts
print args
xlim = ''
ylim = ''
for o, a in opts:
    if o in ('-x', '--xlim'):
        xlim=a
    elif o in ('-y', '--ylim'):
        ylim=a
    else:
        print("Usage: %s -x 4 -y 4" % sys.argv[0])
     
print ("X Bound : %s and Y bound: %s" % (xlim,ylim) )


print 'input_source1 = %s' % input_source1
print 'input_source2 = %s' % input_source2


fp = None
fp = handle_files(fp, input_source1)



vis_data = []
first_source_vals = {}
second_source_vals = {}

if input_source2 == '':
  vis_data.append(['NConfig','Radius', 'Gr1']) # Only one file
elif input_source2 != '':
  vis_data.append(['NConfig','Radius', 'Gr1', 'Gr2']) # Two files

rownum = 0
try:
  reader = csv.reader(fp) 
  for row in reader:
    if rownum != 0:
      key = row[0] + ',' + row[1]
      first_source_vals[key] = row[2]
      float_list = [float(x) for x in row]
      if input_source2 == '':
        vis_data.append(float_list)
    rownum += 1
finally:
  fp.close()
  
if input_source2 != '':
  fp = handle_files(fp, input_source2)
  rownum = 0
  try:
    reader = csv.reader(fp) 
    for row in reader:
      if rownum != 0:
        try:
          key = row[0] + ',' + row[1]
          tempList = [float(row[0]), float(row[1]), float(first_source_vals[key]), float(row[2]) ]
          vis_data.append(tempList)
        except KeyError:
          continue
      rownum += 1
  finally:
    fp.close()

pprint.pprint(vis_data)
#sys.exit(0)


def seq(start, stop, step=1):
    n = int(round((stop - start)/float(step)))
    if n > 1:
        return([start + step*i for i in range(n+1)])
    else:
        return([])
  
#pprint.pprint(vis_data)

class visualizer(object):

  def __init__(self, data, nconfig, xlim, ylim, twoInputFiles):
    self.data = data
    self.total_nconfigs = nconfig
    self.xlim = xlim
    self.ylim = ylim
    self.twoInputFiles = twoInputFiles
    
  def generateVisualFile(self):
    tickValues = ''
    if self.xlim == '':
      tickValues = str(seq(0, float(self.data[-1][1]), 0.5))
    else:
      tickValues = str(seq(0, float(self.xlim), 0.5))
    #print tickValues

    columnStringInterpolation = ''
    gr2Add = ''
    dataframeAdjust = ''


    if not self.twoInputFiles:
      columnStringInterpolation = "'columns': [1, 2]"
      gr2Add = "//columnsTable.addColumn('number', 'Gr2');"
      dataframeAdjust = r'''
      columnsTable.addRow([leftValue, data.getValue(left_nconfigs[i], 1),(right_gofr_1-left_gofr_1)/(rightValue - leftValue)]);
      '''


    else:
      columnStringInterpolation = "'columns': [1, 2, 3]"
      gr2Add = "columnsTable.addColumn('number', 'Gr2');"
      dataframeAdjust = r'''
      var right_gofr_2 = data.getValue(right_nconfigs[i], 3);
      var left_gofr_2 =  data.getValue(left_nconfigs[i], 3); 
      columnsTable.addRow([leftValue, data.getValue(left_nconfigs[i], 1),(right_gofr_1-left_gofr_1)/(rightValue - leftValue),(right_gofr_2-left_gofr_2)/(rightValue - leftValue)]);
      '''

    xAxisString = ''
    yAxisString = ''
    if self.xlim != '':
      xAxisString = r'''
      hAxis: {viewWindow: {max: %s}, title: 'r (Angstrom)', ticks: %s},
      ''' % (self.xlim, tickValues)
    if self.ylim != '':
      yAxisString = r'''
      vAxis: {viewWindow: {max: %s}, title: 'g(r)'}
      ''' % self.ylim
  
    if xAxisString == '' or yAxisString == '':
      xAxisString = "hAxis: {title: 'r (Angstrom)', ticks: %s},\n" % tickValues
      yAxisString = "vAxis: {title: 'g(r)'}\n" 

    boundsString = xAxisString + yAxisString



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
                'view': {%s},

                'options': {
                  'title': 'g_%s%s(r)',
                  width: 1200, 
                  height: 800, 
                  pointSize: 5, 
                  lineWidth: 2,
                  %s
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
              %s
              
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
                
                %s
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
    """ % (
      pprint.pformat(self.data), 
      columnStringInterpolation,
      gc.first_molecule_name, 
      gc.second_molecule_name,
      boundsString,
      gr2Add,
      dataframeAdjust,
      str(self.total_nconfigs) , 
      str(gc.rmax), 
      str(gc.dr), 
      str(gc.first_molecule_name), 
      str(gc.second_molecule_name)
      )
    # CURRENTLY X AND Y LIMITS ARE TAKEN OUT
    #final_filename = "%s_%s_stepsize%s.html" % (gc.first_input_source, gc.second_input_source, gc.stepsize)
    final_filename = "test1.html"
    f = open(final_filename,'w+')
    f.write(htmlString)

    


nconfig = vis_data[-1][0]

twoFiles = False

if input_source2 != '':
  twoFiles = True

vis_obj = visualizer(vis_data, nconfig, xlim, ylim, twoFiles) 
vis_obj.generateVisualFile()
print ('Done generating visual file!')