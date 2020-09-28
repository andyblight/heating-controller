#!/usr/bin/python3
# Made by merging
# https://developers.google.com/chart/interactive/docs/dev/gviz_api_lib
# with
# https://developers.google.com/chart/interactive/docs/gallery/linechart
#
# To make test this:
#  . ../server/web-ui/venv/bin/activate
#  python3 chart_demo.py > ./temp.html
# firefox ./temp.html


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
      %(jscode_chart)s
      var options = {
        chart: {
          title: 'Box Office Earnings in First Two Weeks of Opening',
          subtitle: 'in millions of dollars (USD)'
        },
        width: 900,
        height: 500
      };
      var chart = new google.charts.Line(document.getElementById('linechart_material'));
      chart.draw(jscode_chart_data, google.charts.Line.convertOptions(options));
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


def create_table():
    # Creating the data
    description = {
        "name": ("string", "Name"),
        "salary": ("number", "Salary"),
        "full_time": ("boolean", "Full Time Employee"),
    }
    data = [
        {"name": "Mike", "salary": (10000, "$10,000"), "full_time": True},
        {"name": "Jim", "salary": (800, "$800"), "full_time": False},
        {"name": "Alice", "salary": (12500, "$12,500"), "full_time": True},
        {"name": "Bob", "salary": (7000, "$7,000"), "full_time": True},
    ]

    # Loading it into gviz_api.DataTable
    data_table = gviz_api.DataTable(description)
    data_table.LoadData(data)

    # Create a JavaScript code string.
    jscode = data_table.ToJSCode(
        "jscode_data", columns_order=("name", "salary", "full_time"), order_by="salary"
    )
    return jscode


def create_chart():
    description = {
        "day": ("number", "Day"),
        "guardians": ("number", "Guardians of the Galaxy"),
        "avengers": ("number", "The Avengers"),
        "transformers": ("number", "Transformers: Age of Extinction"),
    }
    # [1,  37.8, 80.8, 41.8],
    # [2,  30.9, 69.5, 32.4],
    # [3,  25.4,   57, 25.7],
    # [4,  11.7, 18.8, 10.5],
    # [5,  11.9, 17.6, 10.4],
    # [6,   8.8, 13.6,  7.7],
    # [7,   7.6, 12.3,  9.6],
    # [8,  12.3, 29.2, 10.6],
    # [9,  16.9, 42.9, 14.8],
    # [10, 12.8, 30.9, 11.6],
    # [11,  5.3,  7.9,  4.7],
    # [12,  6.6,  8.4,  5.2],
    # [13,  4.8,  6.3,  3.6],
    # [14,  4.2,  6.2,  3.4]
    data = [
        {"day": 1, "guardians": 37.8, "avengers": 80.8, "transformers": 41.8},
        {"day": 2, "guardians": 30.9, "avengers": 69.5, "transformers": 32.4},
        {"day": 3, "guardians": 25.4, "avengers": 57.0, "transformers": 25.7},
        {"day": 4, "guardians": 11.7, "avengers": 18.8, "transformers": 10.5},
    ]
    chart_data_table = gviz_api.DataTable(description)
    chart_data_table.LoadData(data)
    # Create a JavaScript code string.
    jscode = chart_data_table.ToJSCode(
        "jscode_chart_data",
        columns_order=("day", "guardians", "avengers", "transformers"),
    )
    return jscode


def main():
    jscode = create_table()
    jscode_chart = create_chart()
    # Put the JS code and JSON string into the template.
    print("Content-type: text/html")
    print()
    print(page_template % vars())


if __name__ == "__main__":
    main()
