console.log("Chart...on ! ")
// table--Activity
new Chart(document.getElementById("t_activity"), {
    type: "line",
    data: {
        labels: ["11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30"],
        datasets: [{
            data: [80, 88, 86, 78, 77, 90, 87, 91, 83],
            borderColor: "#3A7699",
            borderWidth: 2,
            backgroundColor: "#fff",
            pointBackgroundColor: "#fff",
            pointBorderColor: "#3A7699",
            fill: false
        }],
    },
    options: {
        layout: {
            padding: {
                top: 50,
            },
        },
        legend: {
            display: false,
        },
        scales: {
            // x軸
            xAxes: [{// 背景網格
                gridLines: {
                    display: false,// 取消x軸的豎線
                    color: "black",// 設置x軸線顏色
                },
                scaleLabel: {// x軸標題
                    display: true,
                    labelString: "time",
                },
            }],
            // y軸
            yAxes: [{
                gridLines: {
                    color: "gray",
                    borderDash: [2, 5],// 以點線顯示
                },
                scaleLabel: {
                    display: true,
                    labelString: "activity",
                },
                ticks: {// 設置起止數據和步長
                    min: 0,
                    max: 100,
                    stepSize: 10,
                },
            }],
        },
    },
});

//table--Temperature
new Chart(document.getElementById("t_temperature"), {
    type: "line",
    data: {
        labels: ["11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30"],
        datasets: [{
            data: [22, 25, 24, 26, 22, 23, 22, 24, 25],
            borderColor: "#3A7699",
            borderWidth: 2,
            backgroundColor: "#fff",
            pointBackgroundColor: "#fff",
            pointBorderColor: "#3A7699",
            fill: false
        }],
    },
    options: {
        layout: {
            padding: {
                top: 50,
            },
        },
        legend: {
            display: false,
        },
        scales: {
            // x軸
            xAxes: [{// 背景網格
                gridLines: {
                    display: false,// 取消x軸的豎線
                    color: "black",// 設置x軸線顏色
                },
                scaleLabel: {// x軸標題
                    display: true,
                    labelString: "time",
                },
            }],
            // y軸
            yAxes: [{
                gridLines: {
                    color: "gray",
                    borderDash: [2, 5],// 以點線顯示
                },
                scaleLabel: {
                    display: true,
                    labelString: "temperature",
                },
                ticks: {// 設置起止數據和步長
                    min: 0,
                    max: 40,
                    stepSize: 5,
                },
            }],
        },
    },
});

//table--Turbidity
new Chart(document.getElementById("t_turbidity"), {
    type: "line",
    data: {
        labels: ["11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30"],
        datasets: [{
            data: [80, 88, 86, 78, 77, 90, 87, 91, 83],
            borderColor: "#3A7699",
            borderWidth: 2,
            backgroundColor: "#fff",
            pointBackgroundColor: "#fff",
            pointBorderColor: "#3A7699",
            fill: false
        }],
    },
    options: {
        layout: {
            padding: {
                top: 50,
            },
        },
        legend: {
            display: false,
        },
        scales: {
            // x軸
            xAxes: [{// 背景網格
                gridLines: {
                    display: false,// 取消x軸的豎線
                    color: "black",// 設置x軸線顏色
                },
                scaleLabel: {// x軸標題
                    display: true,
                    labelString: "time",
                },
            }],
            // y軸
            yAxes: [{
                gridLines: {
                    color: "gray",
                    borderDash: [2, 5],// 以點線顯示
                },
                scaleLabel: {
                    display: true,
                    labelString: "activity",
                },
                ticks: {// 設置起止數據和步長
                    min: 0,
                    max: 100,
                    stepSize: 10,
                },
            }],
        },
    },
});