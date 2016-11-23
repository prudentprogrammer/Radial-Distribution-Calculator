import pprint
import gofr_config as gc
import urllib2
import sys
import pprint
import os.path
import csv


argc = len(sys.argv)
if ( argc < 2 or argc > 3 ):
  print "use: ", sys.argv[0]
  sys.exit()
  
input_source = sys.argv[1]
fp = None
# test if input_source is a local file
# if not, process as a URL
if ( os.path.isfile(input_source) ):
  fp = open(input_source)
else:
  # attempt to open as a URL
  try:
    fp = urllib2.urlopen(input_source)
  except (ValueError,urllib2.HTTPError) as e:
    print 'Error opening the URL'
    sys.exit()

vis_data = []
rownum = 0
try:
  reader = csv.reader(fp) 
  for row in reader:
    # Save header row.
    if rownum == 0:
      header = row
      vis_data.append(header)
    else:
      float_list = [float(x) for x in row]
      vis_data.append(float_list)
    rownum += 1
finally:
  fp.close()


class visualizer(object):

  def __init__(self, data, nconfig):
    self.data = data
    self.total_nconfigs = nconfig
  
  
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
                'view': {'columns': [1, 2]},
                'options': {'title': 'Radius vs G(r) Difference - Molecules being compared are %s vs %s', width: 1200, height: 800, pointSize: 5, lineWidth: 2},
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
              columnsTable.addColumn('number', 'G(r)');
              
              // Get Slider Information
              var sliderState = nConfigSlider.getState();
              var leftValue = sliderState.lowValue;
              var rightValue = sliderState.highValue;
              
            
              // Corresponds to indices in original data Ex:- [5, 6, 7, 8, 9]
              var left_nconfigs = data.getFilteredRows([{column : 0, value: leftValue}]);
              var right_nconfigs = data.getFilteredRows([{column : 0, value: rightValue}]);
              
              for(var i = 0; i < left_nconfigs.length; i++) {
                var right_gofr = data.getValue(right_nconfigs[i], 2);
                var left_gofr =  data.getValue(left_nconfigs[i], 2);  
                columnsTable.addRow([leftValue, data.getValue(left_nconfigs[i], 1),(right_gofr-left_gofr)/(rightValue - leftValue)]);
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
    """ % (pprint.pformat(self.data), gc.first_molecule_name, gc.second_molecule_name, str(self.total_nconfigs) , str(gc.rmax), str(gc.dr), str(gc.first_molecule_name), str(gc.second_molecule_name))
    
    f = open('sample_graph.html','w+')
    f.write(htmlString)




nconfig = vis_data[-1][0]
vis_obj = visualizer(vis_data, nconfig) 
vis_obj.generateVisualFile()
print ('Done generating visual file!')