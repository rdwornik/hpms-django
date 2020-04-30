var API_URL = document
                    .querySelector("div [url-endpoint]")
                    .attributes
                    .getNamedItem("url-endpoint")
                    .value;
var QUERY_PARAMS = window.location.search;
URL = "".concat(API_URL,QUERY_PARAMS)

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
}