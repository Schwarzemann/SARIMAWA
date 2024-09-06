// fetchdata.js

var ctxRealTime = document.getElementById('realTimeChart').getContext('2d');
var ctxGuess = document.getElementById('guessChart').getContext('2d');

var realTimeData = {
    labels: [],
    datasets: [{
        label: 'Real-time Price',
        data: [],
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1
    }]
};

var guessData = {
    labels: [],
    datasets: [{
        label: 'Price Guess',
        data: [],
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 1
    }]
};

var realTimeChart = new Chart(ctxRealTime, {
    type: 'line',
    data: realTimeData,
    options: {
        scales: {
            y: {
                beginAtZero: false
            }
        }
    }
});

var guessChart = new Chart(ctxGuess, {
    type: 'line',
    data: guessData,
    options: {
        scales: {
            y: {
                beginAtZero: false
            }
        }
    }
});

function fetchData() {
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            if (data.price !== undefined) {
                realTimeData.labels.push(new Date().toLocaleTimeString());
                realTimeData.datasets[0].data.push(data.price);

                realTimeChart.update();
            }
        })
        .catch(error => console.error('Error fetching real-time data:', error));

    fetch('/guess')
        .then(response => response.json())
        .then(data => {
            if (data.guess !== undefined) {
                guessData.labels.push(new Date().toLocaleTimeString());
                guessData.datasets[0].data.push(data.guess);

                guessChart.update();
            }
        })
        .catch(error => console.error('Error fetching guess data:', error));
}

// Fetch data initially
fetchData();

// Periodically fetch new data every 5 seconds
setInterval(fetchData, 5000);
