class visualizer(object):

  def __init__(self, data):
    self.data = data
  
  
  def generateVisualFile(self):
    htmlString = r"""
    <html>
      <head>
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
          google.charts.load('current', {'packages':['corechart']});
          google.charts.setOnLoadCallback(drawChart);

          function drawChart() {
            var data = google.visualization.arrayToDataTable(%s);

            var options = {
              title: 'Radius vs G(r)',
              curveType: 'function',
              legend: { position: 'bottom' },
              width: 1200,
              height: 600,
              pointSize: 2
            };

            var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));

            chart.draw(data, options);
          }
        </script>
      </head>
      <body>
        <div id="curve_chart"></div>
      </body>
    </html>
    """ % str(self.data)
    
    f = open('sample_graph.html','w+')
    f.write(htmlString)

