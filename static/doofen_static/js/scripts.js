// SIDEBAR TOGGLE

var sidebarOpen = false;
var sidebar = document.getElementById("sidebar");

function openSidebar() {
	if(!sidebarOpen) {
		sidebar.classList.add("sidebar-responsive");
		sidebarOpen = true;
	}
}

function closeSidebar() {
	if(sidebarOpen) {
		sidebar.classList.remove("sidebar-responsive");
		sidebarOpen = false;
	}
}



// ---------- CHARTS ----------
function init_charts(){
	// BAR CHART
	var barChartOptions = {
		series: [{
			data: [15, 12, 10, 9, 6]
		}],
		chart: {
			type: 'bar',
			height: 400,
			toolbar: {
				show: false
			},
		},
		colors: [
			"#246dec",
			"#cc3c43",
			"#367952",
			"#f5b74f",
			"#4f35a1",
			"#4f35a1"
			],
		plotOptions: {
			bar: {
				distributed: true,
				borderRadius: 4,
				horizontal: false,
				columnWidth: '40%',
			}
		},
		dataLabels: {
			enabled: false
		},
		legend: {
			show: false
		},
		xaxis: {
			categories: ["NATIONAL LEVEL", "REGIONAL LEVEL", "PROVINCIAL LEVEL", "MUNICIPAL LEVEL" , "COMMUNITY LEVEL"],
		},
		yaxis: {
			title: {
				text: ""
			}
		}
	};



	// AREA CHART
	var areaChartOptions = {
		series: [{
			name: 'COMMUNICATION',
			data: [31, 40, 28, 51, 42, 109, 100]
		}, {
			name: 'PLANNING',
			data: [11, 32, 45, 32, 34, 52, 41]
		}],
		chart: {
			height: 350,
			type: 'area',
			toolbar: {
				show: false,
			},
		},
		colors: ["#4f35a1", "#246dec"],
		dataLabels: {
			enabled: false,
		},
		stroke: {
			curve: 'smooth'
		},
		labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
		markers: {
			size: 0
		},
		yaxis: [
		{
			title: {
				text: '',
			},
		},
		{
			opposite: true,
			title: {
				text: '',
			},
		},
		],
		tooltip: {
			shared: true,
			intersect: false,
		}
	};

	var areaChart = new ApexCharts(document.querySelector("#area-chart"), areaChartOptions);
	areaChart.render();

	var barChart = new ApexCharts(document.querySelector("#bar-chart"), barChartOptions);
	barChart.render();
}