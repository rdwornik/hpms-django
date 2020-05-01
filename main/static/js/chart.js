var API_URL = document
                    .querySelector("div [url-endpoint]")
                    .attributes
                    .getNamedItem("url-endpoint")
                    .value;
var QUERY_PARAMS = window.location.search;
URL = "".concat(API_URL,QUERY_PARAMS)
// TODO make chart interactive on click
$.ajax({
    method:"GET",
    url: URL,
    success: function(data){
        console.log(data)
        setChart(data)
    },     
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
function setChart(data){
    var canvas =  document.getElementById("myChart");
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Number of transactions',
                data: data.data,
            }]
        },
        options: {
            scales: {
                xAxes: [{
                    type: 'time',
                    distribution: 'series',
                    time: {
                        unit: data.label,
                        displayFormats: data.displayFormats
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true,
                    }
                }]
            },
            animation: {
                duration: 0 // general animation time
            },
            hover: {
                animationDuration: 0 // duration of animations when hovering an item
            },
            responsiveAnimationDuration: 0, // animation duration after a resize
            elements: {
                line: {
                    tension: 0 // disables bezier curves
                }
            },
            showLines: true // disable for all datasets
        }
    });
      var canvas =  document.getElementById("myChart");
  canvas.onclick = function(evt) {
      var activePoints = myChart.getElementsAtEvent(evt);
      if (activePoints[0]) {
          var chartData = activePoints[0]['_chart'].config.data;
          var idx = activePoints[0]['_index'];
          var label = chartData.labels[idx];
          var value = chartData.datasets[0].data[idx];
          console.log(idx)
          console.log(label)
          console.log(value)
          location.href = "http://localhost:8000/hpms";
      }
  };
    

}