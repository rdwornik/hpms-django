var API_URL = document
                    .querySelector("div [url-endpoint]")
                    .attributes
                    .getNamedItem("url-endpoint")
                    .value;
console.log(API_URL);

const myForm = document.getElementById("myForm");

// myForm.addEventListener('submit',function(e){
//     e.preventDefault();

// });

const data3 = [
    {
        "hour": "13:00:00",
        "y": 2
    },
    {
        "hour": "12:00:00",
        "y": 6
    }
]
const data2 = [{
    hour: 10,
    y: 20
}, {
    hour: 15,
    y: 10
}]
$.ajax({
    method:"GET",
    url: API_URL,
    success: function(data){
        console.log(data)
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    label: '# of Votes',
                    data: data3,
                }]
            },
            options:{}
        });
    },
    error: function(error_data){
        console.log("error")
        console.log(error_data)
    }
})