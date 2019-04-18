$(document).ready(function() {
	var attributeChart = $(".details-attribute-chart");
    var detailsRadarChart;

    var data = {
                labels: ["Agreeableness", "Extraversion", "Conscientiousness", "Emotional Stability", "Openness"],
                datasets: [{
                    label: "{{char1}}'s Big Five",
                    backgroundColor: "rgba(255,99,132,0.2)",
                    borderColor: "rgba(255,99,132,1)",
                    pointBackgroundColor: "rgba(255,99,132,1)",
                    pointBorderColor: "#fff",
                    pointHoverBackgroundColor: "#fff",
                    pointHoverBorderColor: "rgba(255,99,132,1)",
                    data: [0.1,0.2,0.3,0.4,0.5]
                }, {
                    label: currentGameTitle,
                    backgroundColor: "rgba(90, 179, 206, 0.2)",
                    borderColor: "rgba(90, 179, 206, 1)",
                    pointBackgroundColor: "rgba(90, 179, 206, 1)",
                    pointBorderColor: "#fff",
                    pointHoverBackgroundColor: "#fff",
                    pointHoverBorderColor: "rgba(90, 179, 206, 1)",
                    data: [0.5,-0.2,0.3,0.4,0.5]
                }]
            };

            if (detailsRadarChart !== undefined)
                detailsRadarChart.destroy();

            detailsRadarChart = new Chart(attributeChart, {
                type: 'radar',
                data: data,
                draggable: true,
                options: {
                    legend: {
                        position: 'bottom'
                    },
                    scale: {
                        ticks: {
                            display: false
                        }
                    },
                    tooltips: {
                        enabled: false
                    }
                }
            });
