/* global Plotly */
let file =  "https://raw.githubusercontent.com/mattmurphey25/data_trafficers_project/master/incident_counts.csv"

Plotly.d3.csv(file, function(err, rows){

  function unpack(rows, key) {
      return rows.map(row => row[key])
  }

    console.log(rows)
  
  var dates = unpack(rows, "Date")
  var counts = unpack(rows, "Counts")

      var trace1 = {
        type: "scatter",
        mode: "lines",
        x: dates,
        y: counts,
        line: {
          color: "#17BECF"
        }
      };

      var data = [trace1];

      var layout = {
        title: "Traffic incident counts by day",
        xaxis: {
          autorange: true,
<<<<<<< HEAD
          type: "date",
          title: "Date"
        },
        yaxis: {
          autorange: true,
          type: "linear",
          title: "Incident Counts"
=======
          type: "date"
        },
        yaxis: {
          autorange: true,
          type: "linear"
>>>>>>> master
        }
      };

      Plotly.newPlot("plot", data, layout);

    })

