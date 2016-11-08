import pprint
class visualizer(object):

  def __init__(self, data):
    self.data = data
  
  
  def generateVisualFile(self):
    htmlString = r"""
    <html>
      <head>
        <!--Load the AJAX API-->
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.8/css/materialize.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.97.8/js/materialize.min.js"></script>
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
            var dashboard = new google.visualization.Dashboard(
                document.getElementById('dashboard_div'));

            // Create a range slider, passing some options
            var nConfigSlider = new google.visualization.ControlWrapper({
              'controlType': 'NumberRangeFilter',
              'containerId': 'filter_div',
              'options': {
                'filterColumnLabel': 'NConfig'
              }
            });
            
            var myLine = new google.visualization.ChartWrapper({
                'chartType' : 'LineChart',
                'containerId' : 'chart_div',
                'view': {'columns': [1, 2]},
                'width': 1200,
                'height':1200
            });
            //console.log(donutRangeSlider);
            // Create a pie chart, passing some options
           
            
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
            
            
          }
        </script>
      </head>

      <body class="container">
        <!--Div that will hold the dashboard-->
        <div id="dashboard_div">
          <!--Divs that will hold each control and chart-->
          <div id="filter_div"></div>
          <div id="chart_div"></div>
          <div id="display_div"></div>
          <div id="table_div"><!-- Table renders here --></div>
          
        </div>
      </body>
    </html>
    """ % pprint.pformat(self.data)
    
    f = open('sample_graph.html','w+')
    f.write(htmlString)

