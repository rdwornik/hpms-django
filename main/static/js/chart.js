var canvas = document.getElementById("myChart")
URL_ENDPOINT = canvas.attributes.getNamedItem("url-endpoint-chart").value;
QUERY_PARAMS = window.location.search;
URL = "".concat(URL_ENDPOINT,QUERY_PARAMS)
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
                    distribution: "series",
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
          tag_field = this.attributes.getNamedItem("tag-field").value
          query = new URLSearchParams(window.location.search)
          assigned_tags = query.has(tag_field) ? query.get(tag_field) : ""
          params = {
            [tag_field] : assigned_tags,
            "time_0" : value["x"],
            "time_1" : value["x"].substring(0,10).concat(" 23:59"),
          }
          search = new URLSearchParams(params)
          transactions = this.attributes.getNamedItem("transactions").value
          url = transactions.concat("?", search)
          window.location.href = url
        }
    };
}