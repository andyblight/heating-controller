#!/usr/bin/python3

import gviz_api


page_template = """
<html>
  <script src="https://www.gstatic.com/charts/loader.js"></script>
  <script>
    google.charts.load('current', {packages:['table']});
    google.charts.setOnLoadCallback(drawTable);
    function drawTable() {
      %(jscode)s
      var jscode_table = new google.visualization.Table(document.getElementById('table_div_jscode'));
      jscode_table.draw(jscode_data, {showRowNumber: true});
    }

    google.charts.load('current', {'packages':['line']});
    google.charts.setOnLoadCallback(drawChart);
    function drawChart() {
      var data = new google.visualization.DataTable();
      data.addColumn('number', 'Day');
      data.addColumn('number', 'Guardians of the Galaxy');
      data.addColumn('number', 'The Avengers');
      data.addColumn('number', 'Transformers: Age of Extinction');
      data.addRows([
        [1,  37.8, 80.8, 41.8],
        [2,  30.9, 69.5, 32.4],
        [3,  25.4,   57, 25.7],
        [4,  11.7, 18.8, 10.5],
        [5,  11.9, 17.6, 10.4],
        [6,   8.8, 13.6,  7.7],
        [7,   7.6, 12.3,  9.6],
        [8,  12.3, 29.2, 10.6],
        [9,  16.9, 42.9, 14.8],
        [10, 12.8, 30.9, 11.6],
        [11,  5.3,  7.9,  4.7],
        [12,  6.6,  8.4,  5.2],
        [13,  4.8,  6.3,  3.6],
        [14,  4.2,  6.2,  3.4]
      ]);
      var options = {
        chart: {
          title: 'Box Office Earnings in First Two Weeks of Opening',
          subtitle: 'in millions of dollars (USD)'
        },
        width: 900,
        height: 500
      };
      var chart = new google.charts.Line(document.getElementById('linechart_material'));
      chart.draw(data, google.charts.Line.convertOptions(options));
    }
  </script>
  <body>
    <H1>Table created using ToJSCode</H1>
    <div id="table_div_jscode"></div>
    <H1>Line chart</H1>
    <div id="linechart_material"></div>
  </body>
</html>
"""


def main():
    # Creating the data
    description = {"name": ("string", "Name"),
                   "salary": ("number", "Salary"),
                   "full_time": ("boolean", "Full Time Employee")}
    data = [{"name": "Mike", "salary": (10000, "$10,000"), "full_time": True},
            {"name": "Jim", "salary": (800, "$800"), "full_time": False},
            {"name": "Alice", "salary": (12500, "$12,500"), "full_time": True},
            {"name": "Bob", "salary": (7000, "$7,000"), "full_time": True}]

    # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    # Create a JavaScript code string.
    jscode = data_table.ToJSCode("jscode_data",
                                 columns_order=("name", "salary", "full_time"),
                                 order_by="salary")
    # Create a JSON string.
    json = data_table.ToJSon(columns_order=("name", "salary", "full_time"),
                             order_by="salary")

    # Put the JS code and JSON string into the template.
    print("Content-type: text/html")
    print()
    print(page_template % vars())


if __name__ == '__main__':
    main()
