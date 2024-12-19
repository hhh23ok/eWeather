document.addEventListener('DOMContentLoaded', function() {
    const ctx = document.getElementById('weatherChart').getContext('2d');

    // Ensure chartData is not undefined or null before proceeding
    if (typeof chartData !== 'undefined' && chartData !== null && chartData.dates && chartData.dates.length > 0) {
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartData.dates,
                datasets: [{
                    label: 'Max Temp (°C)',
                    data: chartData.temp_max,
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1,
                    fill: false
                }, {
                    label: 'Min Temp (°C)',
                    data: chartData.temp_min,
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1,
                    fill: false
                }]
            },
            options: {
                scales: {
                    x: {
                        type: 'category',
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        beginAtZero: false,
                        title: {
                            display: true,
                            text: 'Temperature (°C)'
                        }
                    }
                }
            }
        });
    } else {
        console.warn('No valid chart data available.');
    }
});
