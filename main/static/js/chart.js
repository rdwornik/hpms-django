Date.prototype.addHours = function(h) {
  this.setTime(this.getTime() + (h*60*60*1000));
  return this;
}

var sampling = $('#id_sampling').val()
var time_range = $("#mylink").attr("range")

add_hours_dictionary={ 
  "minute": (sampling/60), 
  "hour": (sampling/60), 
  "day":(sampling),
  "month":(24*sampling),
  "year": (8760*sampling)
};

var canvas = document.getElementById("myChart")
URL_ENDPOINT = canvas.attributes.getNamedItem("url-endpoint-chart").value;
URL = URL_ENDPOINT.concat(window.location.search)
$.ajax({
    method:"GET",
    url: URL,
    success: function(data){
        setChart(data)
    },     
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})
function setChart(data)
{
    var label = data.label;
    var ctx = canvas.getContext("2d")
    var myChart = new Chart(ctx, 
    {
        type: "line",
        data: 
          {
            datasets: 
              [{
                  label: "Number of transactions",
                  data: data.data,
              }]
          },
        options: 
        {
          scales: 
            {
              xAxes: 
                [{
                    type: "time",
                    // distribution: "series",
                    distribution: data.distribution_type,
                    time: 
                        {
                            unit: data.label,
                            displayFormats: data.displayFormats
                        }
                }],
              yAxes: 
                [{
                    ticks: 
                    {
                        beginAtZero: true,
                    }
                }]
            },
          animation: 
            {
              duration: 0 // general animation time
            },
          hover: 
            {
              animationDuration: 0 // duration of animations when hovering an item
            },
          responsiveAnimationDuration: 0, // animation duration after a resize
          elements: 
          {
            line: 
              {
                tension: 0 // disables bezier curves
              }
          },
          showLines: true // disable for all datasets
        }
    });
    canvas.onclick = function(evt) 
    {
      var activePoints = myChart.getElementsAtEvent(evt);
      if (activePoints[0]) 
      {
          chartData = activePoints[0]["_chart"].config.data
          idx = activePoints[0]["_index"]
          value = chartData.datasets[0].data[idx]
          params = new URLSearchParams(window.location.search)
          params.set('time_after',value['x'])
          time = new Date(value['x'])
          hours = add_hours_dictionary[time_range]
          time_before = time.addHours(hours)
          params.set('time_before', moment(time_before).format("YYYY-MM-DD HH:mm"))          
          transactions_url = this.attributes.getNamedItem("transactions").value
          url = transactions_url.concat("?", params.toString())
          window.location.href = url
        }
    };
}