$(document).ready(function() {
    $.ajax({
      method:"GET",
      url: "{% url 'transaction-list' %}?{{ request.GET.urlencode }}",
      success: function(data)
      {
        console.log(data)
          setChart(data)
      },     
      error: function(error_data)
      {
          console.log("error")
          console.log(error_data)
      }
    })
    function setChart(data)
    {
      var ctx = document.getElementById('myChart').getContext('2d')
      var myChart = new Chart(ctx, 
      {
          type: 'line',
          data: 
            {
              datasets: 
                [{
                    label: 'Number of transactions',
                    data: data.data,
                }]
            },
          options: 
          {
            scales: 
              {
                xAxes: 
                  [{
                      type: 'time',
                      distribution: 'series',
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
      canvas = document.getElementById("myChart")
      canvas.onclick = function(evt) 
      {
        var activePoints = myChart.getElementsAtEvent(evt);
        if (activePoints[0]) 
        {
            chartData = activePoints[0]['_chart'].config.data
            idx = activePoints[0]['_index']
            value = chartData.datasets[0].data[idx]
            time_0 = encodeURIComponent(value['x'])
            time_1 = encodeURIComponent(value['x'].substring(0,10).concat(" 23:59"))
            params = new URLSearchParams(window.location.search)
            assigned_tags = params.has("{{ tag_field }}") ? params.get("{{ tag_field }}") : ""
            url = "{% url 'transactions' %}?".concat("{{ tag_field }}=",assigned_tags,"&{{ time_0_field }}=",time_0,"&&{{ time_1_field }}=",time_1)
            window.location.href = url
          }
      };
    }
  });