function aqiChose(type) {
    $.get('/api/aqi/current/', function (data) {
        if (data.code != '200') {
            console.log('AQI数据获取失败')
        }
        else {
            var time = data.data.time;
            $('#time').html(time);
            var dataSet = data.data.data_set;
            drawMap('aqi-map', dataSet, type);
            drawPie('aqi-pie', dataSet, type);
        }
    })
}

var convertCurrentDsWithLocation = function (data, type) {
    var res = [];
    for (var i = 0; i < data.length; i++) {
        res.push({
            name: data[i].name,
            value: [data[i].lng, data[i].lat, data[i][type]]
        });
    }
    return res;
};

var divideCurrentDs = function (data, type) {
    var count = {
        'greet': 0, 'good': 0, 'little': 0,
        'middle': 0, 'heavy': 0, 'max': 0
    };
    for (var i = 0; i < data.length; i++) {
        var aqi = data[i][type];
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
        {'name': '严重(300+)', 'value': count.max},
        {'name': '重度(200+)', 'value': count.heavy},
        {'name': '中度(150+)', 'value': count.middle},
        {'name': '轻度(100+)', 'value': count.little},
        {'name': '良好(50+)', 'value': count.good},
        {'name': '优秀(<=50)', 'value': count.greet}
    ]
}

function drawMap(element_id, currentDs, type) {
    var ele = $('#' + element_id);
    ele.css('height', ele.css('width'));
    var myChart = echarts.init(document.getElementById(element_id));
    $(document).ready(function () {
        var option = {
            backgroundColor: '#868e96',
            title: {
                text: '地理分布图',
                subtext: 'data from api.weblist.site',
                sublink: 'http://api.weblist.site',
                x: 'center',
                textStyle: {
                    color: '#000000'
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
                data: [type],
                textStyle: {
                    color: '#fff'
                }
            },
            visualMap: {
                min: 0,
                max: 500,
                calculable: true,
                color: ['#A52A2A', '#CD0000', '#78ea36'],
                textStyle: {
                    color: '#000'
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
                        areaColor: '#EEE5DE',
                        borderColor: '#111'
                    },
                    emphasis: {
                        areaColor: '#EEDFCC'
                    }
                }
            },
            series: [
                {
                    name: 'pm2.5',
                    type: 'scatter',
                    coordinateSystem: 'geo',
                    data: convertCurrentDsWithLocation(currentDs, type),
                    symbolSize: 6,
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
                        },
                        itemStyle: {
                            normal: {
                                color: 'blue'
                            }
                        }
                    }
                }
            ]
        };
        myChart.setOption(option);
    });
}

function drawPie(element_id, currentDs, type) {
    var ele = $('#' + element_id);
    ele.css('height', ele.css('width'));
    var myChart = echarts.init(document.getElementById(element_id));
    $(document).ready(function () {
        option = {
            title: {
                text: '梯度分类图',
                x: 'center'
            },
            tooltip: {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient: 'vertical',
                left: 'left',
                data: ['严重(300+)', '重度(200+)', '中度(150+)', '轻度(100+)', '良好(50+)', '优秀(<=50)']
            },
            color: ['#A52A2A', '#8B008B','#EE2C2C', '#EEB422', '#EEEE00', '#78ea36'],
            series: [
                {
                    name: 'AQI',
                    type: 'pie',
                    radius: '55%',
                    center: ['55%', '60%'],
                    data: divideCurrentDs(currentDs, type),
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
