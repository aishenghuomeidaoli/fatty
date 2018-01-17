function initAqi(mapId, pieId) {
    $.get('/api/aqi/current/', function (data) {
        if (data.code != '200') {
            console.log('AQI数据获取失败')
        }
        else {
            var dataSet = data.data.data_set;
            drawMap(mapId, dataSet);
            drawPie(pieId, dataSet)
        }
    })
}

var convertCurrentDsWithLocation = function (data) {
    var res = [];
    for (var i = 0; i < data.length; i++) {
        res.push({
            name: data[i].name,
            value: [data[i].lng, data[i].lat, data[i].aqi]
        });
    }
    return res;
};

var divideCurrentDs = function (data) {
    var count = {
        'greet': 0, 'good': 0, 'little': 0,
        'middle': 0, 'heavy': 0, 'max': 0
    };
    for (var i = 0; i < data.length; i++) {
        var aqi = data[i].aqi;
        if (aqi <= 50) {
            count.greet = count.greet + 1
        }
        else if (aqi < 100) {
            count.good = count.good + 1
        }
        else if (aqi < 150) {
            count.little = count.little + 1
        }
        else if (aqi < 200) {
            count.middle = count.middle + 1
        }
        else if (aqi < 300) {
            count.heavy = count.heavy + 1
        }
        else {
            count.max = count.max + 1
        }
    }
    return [
        {'name': '严重污染', 'value': count.max},
        {'name': '重度污染', 'value': count.heavy},
        {'name': '中度污染', 'value': count.middle},
        {'name': '轻度污染', 'value': count.little},
        {'name': '良', 'value': count.good},
        {'name': '优', 'value': count.greet}
    ]
}

function drawMap(element_id, currentDs) {
    var ele = $('#' + element_id);
    ele.css('height', ele.css('width'));
    var myChart = echarts.init(document.getElementById(element_id));
    $(document).ready(function () {
        var option = {
            backgroundColor: '#404a59',
            title: {
                text: '全国主要城市空气质量',
                subtext: 'data from api.weblist.site',
                sublink: 'http://api.weblist.site',
                x: 'center',
                textStyle: {
                    color: '#fff'
                }
            },
            tooltip: {
                trigger: 'item',
                formatter: function (params) {
                    return params.name + ' : ' + params.value[2];
                }
            },
            legend: {
                orient: 'vertical',
                y: 'bottom',
                x: 'right',
                data: ['pm2.5'],
                textStyle: {
                    color: '#fff'
                }
            },
            visualMap: {
                min: 0,
                max: 200,
                calculable: true,
                color: ['#d94e5d', '#eac736', '#50a3ba'],
                textStyle: {
                    color: '#fff'
                }
            },
            geo: {
                map: 'china',
                label: {
                    emphasis: {
                        show: false
                    }
                },
                itemStyle: {
                    normal: {
                        areaColor: '#323c48',
                        borderColor: '#111'
                    },
                    emphasis: {
                        areaColor: '#2a333d'
                    }
                }
            },
            series: [
                {
                    name: 'pm2.5',
                    type: 'scatter',
                    coordinateSystem: 'geo',
                    data: convertCurrentDsWithLocation(currentDs),
                    symbolSize: 12,
                    label: {
                        normal: {
                            show: false
                        },
                        emphasis: {
                            show: false
                        }
                    },
                    itemStyle: {
                        emphasis: {
                            borderColor: '#fff',
                            borderWidth: 1
                        }
                    }
                }
            ]
        };
        myChart.setOption(option);
    });
}

function drawPie(element_id, currentDs) {
    var ele = $('#' + element_id);
    ele.css('height', ele.css('width'));
    var myChart = echarts.init(document.getElementById(element_id));
    $(document).ready(function () {
        option = {
            title: {
                text: 'AQI梯度分布图',
                subtext: '纯属虚构',
                x: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                left: 'left',
                data: ['严重污染', '重度污染', '中度污染', '轻度污染', '良', '优']
            },
            series: [
                {
                    name: 'AQI',
                    type: 'pie',
                    radius: '60%',
                    center: ['50%', '60%'],
                    data: divideCurrentDs(currentDs),
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ]
        };
        myChart.setOption(option);
    });
}