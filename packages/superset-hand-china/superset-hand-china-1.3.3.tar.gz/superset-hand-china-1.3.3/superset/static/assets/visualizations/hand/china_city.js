const d3 = require('d3');
const echarts = require('echarts');
const $ = require('jquery');
const geo = require('./china_city_geo');

function chinaCityMapVis(slice, payload, theme) {
  let chart;
  const render = function (sliceTheme) {
    if (payload.error !== null) {
      slice.error(error.responseText, error);
      return;
    }
    slice.container.html('')
    // init the echarts
    let height = slice.height();
    $('#' + slice.containerId).css('height', height).css('width', '100%');
    if (sliceTheme) {
      theme = sliceTheme;
    }
    echarts.dispose(document.getElementById(slice.containerId));
    chart = echarts.init(document.getElementById(slice.containerId), theme === null ? 'macarons' : theme);
    slice.clearError();
    const fd = slice.formData;
    const dt = payload.data;
    let metrics = [fd['metric']];
    const groupby = fd['groupby_one'];
    const latitude = fd['latitude'];
    const longitude = fd['longitude'];
    const metric_one = fd['metric'];
    const bar_column = metric_one;
    const standard_point = fd['standard_point'];
    const drawGraph = function () {
      const data = [];
      let geoSerieName;
      let barSerieName;
      const geoCoordMap = geo.default;
      dt.records.sort(function (a, b) {
        return a[metric_one] - b[metric_one]
      });
      for (let i = 0; i < dt.records.length; i++) {
        const value = [];
        value.push(dt.records[i][metric_one]);
        geoSerieName = metric_one;
        data.push({
          name: dt.records[i][groupby],
          value: value
        });
        // geoCoordMap[dt[i][groupby]] = [dt[i][latitude], dt[i][longitude]];
      }
      var convertData = function (data) {
        var res = [];
        for (var i = 0; i < data.length; i++) {
          var geoCoord = geoCoordMap[data[i].name];
          if (geoCoord) {
            res.push({
              name: data[i].name,
              value: geoCoord.concat(data[i].value)
            });
          }
        }
        return res;
      };

      var convertedData = [
        convertData(data),
        convertData(data.sort(function (a, b) {
          return b.value - a.value;
        }).slice(0, 6))
      ];
      const standard = data[0].value[0] / 10;
      data.sort(function (a, b) {
        return a.value - b.value;
      });
      var selectedItems = [];
      var categoryData = [];
      var barData = [];
      //   var maxBar = 30;
      var sum = 0;
      var count = data.length;
      for (var i = 0; i < data.length; i++) {
        categoryData.push(data[i].name);
        barData.push({
          name: dt.records[i][groupby],
          value: dt.records[i][bar_column]
        });
        sum += barData[i].value;
      }
      barData.sort(function (a, b) {
        return a.value - b.value;
      });
      const option = {
        backgroundColor: '#404a59',
        animation: true,
        animationDuration: 1000,
        animationEasing: 'cubicInOut',
        animationDurationUpdate: 1000,
        animationEasingUpdate: 'cubicInOut',
        title: [
          {
            // text: '全国主要城市 业务量',
            // subtext: '内部数据请勿外传',
            left: 'center',
            textStyle: {
              color: '#fff'
            }
          },
          {
            id: 'statistic',
            text: count ? '平均: ' + parseInt((sum / count).toFixed(4)) : '',
            right: 120,
            top: 40,
            width: 100,
            textStyle: {
              color: '#fff',
              fontSize: 16
            }
          }],
        toolbox: {
          iconStyle: {
            normal: {
              borderColor: '#fff'
            },
            emphasis: {
              borderColor: '#b1e4ff'
            }
          },
          feature: {
            dataZoom: {},
            brush: {
              type: ['rect', 'polygon', 'clear']
            },
            saveAsImage: {
              show: true
            }
          }
        },
        brush: {
          outOfBrush: {
            color: '#abc'
          },
          brushStyle: {
            borderWidth: 2,
            color: 'rgba(0,0,0,0.2)',
            borderColor: 'rgba(0,0,0,0.5)',
          },
          seriesIndex: [0, 1],
          throttleType: 'debounce',
          throttleDelay: 300,
          geoIndex: 0
        },
        geo: {
          map: 'china',
          left: '10',
          right: '35%',
          center: [117.98561551896913, 31.205000490896193],
          zoom: 1.5,
          label: {
            emphasis: {
              show: false
            }
          },
          roam: true,
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
        // tooltip: {
        //   trigger: 'item'
        // },
        tooltip: {
          trigger: 'item',
          formatter: function (params) {
            var res = params.name + '<br/>';
            if (params.seriesType === 'bar') {
              res += bar_column;
              for (var j = 0; j < barData.length; j++) {
                if (barData[j].name === params.name) {
                  res += ' : ' + barData[j].value + '</br>';
                }
              }
            }
            else if (params.seriesType === 'effectScatter') {
              var myseries = option.series;
              for (var i = 0; i < myseries.length; i++) {
                if (myseries[i].name && myseries[i].type !== 'bar') {
                  res += myseries[i].name;
                  for (var j = 0; j < myseries[i].data.length; j++) {
                    if (myseries[i].data[j].name == params.name) {
                      res += ' : ' + myseries[i].data[j].value[2] + '</br>';
                    }
                  }

                }
              }
            }

            return res;
          }
        },
        grid: {
          right: 40,
          top: 100,
          bottom: 40,
          width: '30%'
        },
        xAxis: {
          type: 'value',
          scale: true,
          position: 'top',
          boundaryGap: false,
          splitLine: {
            show: false
          },
          axisLine: {
            show: false
          },
          axisTick: {
            show: false
          },
          axisLabel: {
            margin: 2,
            textStyle: {
              color: '#aaa'
            }
          },
        },
        yAxis: {
          type: 'category',
          //  name: 'TOP 20',
          nameGap: 16,
          axisLine: {
            show: false,
            lineStyle: {
              color: '#404a59'
            }
          },
          axisTick: {
            show: false,
            lineStyle: {
              color: '#ddd'
            }
          },
          axisLabel: {
            interval: 0,
            textStyle: {
              color: '#ddd'
            }
          },
          data: categoryData
        },
        series: [
          {
            name: geoSerieName,
            type: 'scatter',
            coordinateSystem: 'geo',
            data: convertedData[0],
            symbolSize: function (val) {
              return Math.max(val[2] / standard, standard_point);
            },
            label: {
              normal: {
                formatter: '{b}',
                position: 'right',
                show: false
              },
              emphasis: {
                show: true
              }
            },
            itemStyle: {
              normal: {
                color: '#ddb926',
                position: 'right',
                show: true
              }
            }
          },
          {
            // name: geoSerieName,
            type: 'effectScatter',
            coordinateSystem: 'geo',
            data: convertedData[0],
            symbolSize: function (val) {
              return Math.max(val[2] / standard, standard_point);
            },
            showEffectOn: 'emphasis',
            rippleEffect: {
              brushType: 'stroke'
            },
            hoverAnimation: true,
            label: {
              normal: {
                formatter: '{b}',
                position: 'right',
                show: true
              }
            },
            itemStyle: {
              normal: {
                color: '#f4e925',
                shadowBlur: 10,
                shadowColor: '#333'
              }
            },
            zlevel: 1
          },
          {
            name: bar_column,
            id: 'bar',
            zlevel: 2,
            type: 'bar',
            symbol: 'none',
            itemStyle: {
              normal: {
                color: '#ddb926'
              }
            },
            data: barData
          }]
      };

      chart.on('brushselected', renderBrushed);

      function renderBrushed(params) {
        var mainSeries = params.batch[0].selected[0];

        var selectedItems = [];
        var categoryData = [];
        // var barData = [];
        var maxBar = 30;
        var sum = 0;
        var count = 0;

        for (var i = 0; i < mainSeries.dataIndex.length; i++) {
          var rawIndex = mainSeries.dataIndex[i];
          var dataItem = convertedData[0][rawIndex];
          var pmValue = dataItem.value[2];

          sum += pmValue;
          count++;

          selectedItems.push(dataItem);
        }

        selectedItems.sort(function (a, b) {
          return a.value[2] - b.value[2];
        });

        for (var i = 0; i < Math.min(selectedItems.length, maxBar); i++) {
          categoryData.push(selectedItems[i].name);
          //barData.push(selectedItems[i].value[2]);
        }
        
        this.setOption({
          yAxis: {
            data: categoryData
          },
          xAxis: {
            axisLabel: { show: !!count }
          },
          title: {
            id: 'statistic',
            text: count ? '平均: ' + (sum / count).toFixed(4) : ''
          },
          series: {
            id: 'bar',
            data: barData
          }
        });
      }
      chart.setOption(option);
      slice.container.css('height', height + 'px');
      return chart;
    }
    const graph = drawGraph();
  };

  render();
}

module.exports = chinaCityMapVis;