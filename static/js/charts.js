// Function to parse the data attributes and create the charts
function createCharts() {
    // Get data from the HTML elements using data-attributes
    const teAmoNico = JSON.parse(document.getElementById('teAmoChart').getAttribute('data-te-amo-nico'));
    const teAmoMechi = JSON.parse(document.getElementById('teAmoChart').getAttribute('data-te-amo-mechi'));
    const hourlyMessages = JSON.parse(document.getElementById('horaHablamosChart').getAttribute('data-hourly-messages'));
    const mlemNico = JSON.parse(document.getElementById('mlemChart').getAttribute('data-mlem-nico'));
    const mlemMechi = JSON.parse(document.getElementById('mlemChart').getAttribute('data-mlem-mechi'));


    // Debug: Log the hourly messages data to the console
    console.log("Hourly Messages Data:", hourlyMessages);

    // Group the hourly messages into AM/PM
    const amMessages = hourlyMessages.slice(0, 12).reduce((acc, val) => acc + val, 0);  // Sum hours 0-11 (AM)
    const pmMessages = hourlyMessages.slice(12, 24).reduce((acc, val) => acc + val, 0);  // Sum hours 12-23 (PM)

    // Data for the "Quien dijo 'Te amo'" pie chart
    const teAmoData = {
        labels: ['Nicolas Yunes', 'Mecho Aguirre'],
        datasets: [{
            label: 'Te Amo Count',
            data: [teAmoNico, teAmoMechi],
            backgroundColor: ['#28a745', '#ff69b4']  // Green for Nicolas, Pink for Mecho
        }]
    };

   // Data for the "A que hora hablamos" line chart (12-hour AM/PM format)
   const horaHablamosData = {
        labels: ['12:00 AM', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', '6:00 AM', '7:00 AM', '8:00 AM', '9:00 AM', '10:00 AM', '11:00 AM', 
                '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM'],
        datasets: [{
            label: 'Messages by Hour',
            data: hourlyMessages,
            fill: false,
            borderColor: '#007bff',
            tension: 0.1
        }]
    };

     // Data for the AM/PM pie chart
     const amPmData = {
        labels: ['AM', 'PM'],
        datasets: [{
            label: 'Messages by AM/PM',
            data: [amMessages, pmMessages],
            backgroundColor: ['#ffcc00', '#3399ff']  // Yellow for AM, Blue for PM (example colors)
        }]
    };

    // Create the line chart for "A que hora hablamos"
    const horaHablamosChart = new Chart(document.getElementById('horaHablamosChart'), {
        type: 'line',
        data: horaHablamosData,
    });

    // Create the pie chart for AM/PM
    const amPmChart = new Chart(document.getElementById('amPmChart'), {
        type: 'pie',
        data: amPmData,
        options: {
            plugins: {
                datalabels: {
                    color: 'white',
                    formatter: (value) => value  // Show raw value (count) instead of percentage
                }
            }
        },
        plugins: [ChartDataLabels]  // Enable the Datalabels plugin
    });


    // Data for the "Mlem momento" pie chart
    const mlemData = {
        labels: ['Nicolas Yunes', 'Mecho Aguirre'],
        datasets: [{
            label: 'Mlem Count',
            data: [mlemNico, mlemMechi],
            backgroundColor: ['#28a745', '#ff69b4']  // Green for Nicolas, Pink for Mecho
        }]
    };

    // Create the pie chart for "Quien dijo 'Te amo'"
    const teAmoChart = new Chart(document.getElementById('teAmoChart'), {
        type: 'pie',
        data: teAmoData,
        options: {
            plugins: {
                datalabels: {
                    color: 'white',
                    formatter: (value) => value  // Show raw value (count) instead of percentage
                }
            }
        },
        plugins: [ChartDataLabels]  // Enable the Datalabels plugin
    });


    // Create the pie chart for "Mlem momento"
    const mlemChart = new Chart(document.getElementById('mlemChart'), {
        type: 'pie',
        data: mlemData,
        options: {
            plugins: {
                datalabels: {
                    color: 'white',
                    formatter: (value) => value  // Show raw value (count) instead of percentage
                }
            }
        },
        plugins: [ChartDataLabels]  // Enable the Datalabels plugin
    });
}

// Call the function to create charts
document.addEventListener('DOMContentLoaded', createCharts);
