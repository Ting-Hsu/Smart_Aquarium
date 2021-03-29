console.log("Chart...on ! ")
// table--Activity
// var t_activity = new Chart(document.getElementById("t_activity"), {
//     type: "line",
//     data: {
//         labels: [],
//         datasets: [{
//             data: [],
//             borderColor: "#3A7699",
//             borderWidth: 2,
//             backgroundColor: "#C1FFC1",
//             pointRadius: 2,
//             pointBackgroundColor: "#fff",
//             pointBorderColor: "#3A7699",
//             fill: true
//         }],
//     },
//     options: {
//         layout: {
//             padding: {
//                 top: 50,
//             },
//         },
//         legend: {
//             display: false,
//         },
//         scales: {
//             // x軸
//             xAxes: [{// 背景網格
//                 gridLines: {
//                     display: false,// 取消x軸的豎線
//                     color: "black",// 設置x軸線顏色
//                 },
//                 scaleLabel: {// x軸標題
//                     display: true,
//                     labelString: "time",
//                 },
//             }],
//             // y軸
//             yAxes: [{
//                 gridLines: {
//                     color: "gray",
//                     borderDash: [2, 5],// 以點線顯示
//                 },
//                 scaleLabel: {
//                     display: true,
//                     labelString: "temperature",
//                 },
//                 ticks: {// 設置起止數據和步長
//                     min: 0,
//                     max: 50,
//                     stepSize: 0,
//                 },
//             }],
//         },
//     },
// });


//table--Temperature
var t_temperature = new Chart(document.getElementById("t_temperature"), {
    type: "line",
    data: {
        labels: [],
        datasets: [{
            data: [],
            borderColor: "#3A7699",
            borderWidth: 2,
            pointRadius: 2,
            pointBackgroundColor: "#fff",
            pointBorderColor: "#3A7699",
            fill: true
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
                    min: 10,
                    max: 40,
                    stepSize: 0,
                },
            }],
        },
    },
});
var t_temperature2 = new Chart(document.getElementById("t_temperature2"), {
    type: "line",
    data: {
        labels: [],
        datasets: [{
            data: [],
            borderColor: "#3A7699",
            borderWidth: 2,
            pointRadius: 2,
            pointBackgroundColor: "#fff",
            pointBorderColor: "#3A7699",
            fill: true
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
                    min: 30,
                    max: 60,
                    stepSize: 0,
                },
            }],
        },
    },
});



function addData(chart, label, data) {
    chart.data.labels.push(label);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data);
    });
    chart.update();
}

function removeData(chart) {
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}

// 需先預載入一整天資料
dataset=[]
labels=[]
for(let i=0;i<50; i++){
    dataset.push(moment().format("HH:mm:ss"))
    // addData(t_activity, moment().format("HH:mm:ss"), Math.floor(Math.random()*20))
    addData(t_temperature, moment().format("HH:mm:ss"), Math.floor(Math.random()*(24.1-22.3)+22.3))
    addData(t_temperature2, moment().format("HH:mm:ss"), Math.floor(Math.random()*(45.5-39.8)+39.8))
}



// setInterval(function(){
//     var data_length = t_activity.data.datasets[0].data.length;
//     // addData(t_activity, label_time, data_temp) 在這裡接收資料，並加入到表中 一組資料x時間,y溫度  
//     addData(t_activity, moment().format("HH:mm:ss"), Math.floor(Math.random()*20))
//     if(data_length==50){
//         t_activity.data.datasets[0].data.shift()
//         t_activity.data.labels.shift()
//         console.log(t_activity.data)
//         t_activity.update();
//     }
// },2000)

// setInterval(function(){
//     var data_length = t_turbidity.data.datasets[0].data.length;
//     // addData(t_turbidity, label_time, data_temp) 在這裡接收資料，並加入到表中 一組資料x時間,y溫度  
//     addData(t_turbidity, moment().format("HH:mm:ss"), Math.floor(Math.random()*20))
//     if(data_length==50){
//         t_turbidity.data.datasets[0].data.shift()
//         t_turbidity.data.labels.shift()
//         console.log(t_turbidity.data)
//         t_turbidity.update();
//     }
// },2000)

setInterval(function(){
    var data_length = t_temperature.data.datasets[0].data.length;
    // addData(t_temperature, label_time, data_temp) 在這裡接收資料，並加入到表中 一組資料x時間,y溫度  
    addData(t_temperature, moment().format("HH:mm:ss"), Math.floor(Math.random()*(24.1-22.3)+22.3))
    if(data_length==50){
        t_temperature.data.datasets[0].data.shift()
        t_temperature.data.labels.shift()
        console.log(t_temperature.data)
        t_temperature.update();
    }
    addData(t_temperature2, moment().format("HH:mm:ss"), Math.floor(Math.random()*(45.5-39.8)+39.8))
    if(data_length==50){
        t_temperature2.data.datasets[0].data.shift()
        t_temperature2.data.labels.shift()
        console.log(t_temperature.data)
        t_temperature2.update();
    }
},2000)