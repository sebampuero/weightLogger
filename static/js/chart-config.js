var ctx = document.getElementById("canvas").getContext('2d');
var config = {
    type: 'line',
    data: {
	    labels: [],
	    datasets: [{
		    label: '',
		    data: [],
		    backgroundColor: "rgb(255, 99, 132)",
		    borderColor: "rgb(255, 99, 132)",
		    fill: false
		}]
	},
    options: {
				responsive: true,
				title: {
					display: true,
					text: 'Weight history chart'
				},
				tooltips: {
					mode: 'index',
					intersect: false,
				},
				hover: {
					mode: 'nearest',
					intersect: true
				},
				scales: {
					xAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: 'Weight'
						}
					}],
					yAxes: [{
						display: true,
						scaleLabel: {
							display: true,
							labelString: ''
						}
					}]
				}
	}
}
var myLineChart = new Chart(ctx, config);
