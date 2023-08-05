const d3 = require('d3');
const echarts = require('echarts');
const $ = require('jquery');
const geo = require('./china_city_geo');

function chinaCityMapMigrationVis(slice, payload, theme) {
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
      const metricValue = fd['metric'];
      const max_value = fd['max_legend'];
      const min_value = fd['min_legend'];

      const drawGraph = function () {
        let fromCityName;
        let toCityName;
        const geoCoordMap = geo.default;
        const planePath = 'path://M1705.06,1318.313v-89.254l-319.9-221.799l0.073-208.063c0.521-84.662-26.629-121.796-63.961-121.491c-37.332-0.305-64.482,36.829-63.961,121.491l0.073,208.063l-319.9,221.799v89.254l330.343-157.288l12.238,241.308l-134.449,92.931l0.531,42.034l175.125-42.917l175.125,42.917l0.531-42.034l-134.449-92.931l12.238-241.308L1705.06,1318.313z';
        const fromCityArr = [];
        const toCityArr = [];
        for(let i = 0; i< dt.records.length; i++){
          if(fromCityArr.indexOf(dt.records[i][fd.groupby[0]]) === -1){
            fromCityArr.push(dt.records[i][fd.groupby[0]]);
          }
          if(toCityArr.indexOf(dt.records[i][fd.groupby[1]]) === -1){
            toCityArr.push(dt.records[i][fd.groupby[1]]);
          }
        }

        //迁出量
        const mapFromValueData = {};
        for (let m = 0; m < fromCityArr.length; m++) {
          let value = 0;
          for (let n = 0; n < dt.records.length; n++) {
            if(dt.records[n][fd.groupby[0]] === fromCityArr[m]){
              value += Number(dt.records[n][metricValue]);
            }
          }
          mapFromValueData[fromCityArr[m]] = value;
        }

        //迁入量
        const mapToValueData = {}
        for (let m = 0; m < toCityArr.length; m++) {
          let value = 0;
          for (let n = 0; n < dt.records.length; n++) {
            if(dt.records[n][fd.groupby[1]] === toCityArr[m]){
              value += Number(dt.records[n][metricValue]);
            }
          }
          mapToValueData[toCityArr[m]] = value;
        }

        const mapData = [];
        const chinaData = [];
        for (let q = 0; q < dt.records.length; q++) {
          chinaData.push([{
            name: dt.records[q][fd.groupby[0]],
            fromValue: mapFromValueData[dt.records[q][fd.groupby[0]]] ? mapFromValueData[dt.records[q][fd.groupby[0]]] : 0,
            toValue: mapToValueData[dt.records[q][fd.groupby[0]]] ? mapToValueData[dt.records[q][fd.groupby[0]]] : 0
          },
          {
            name: dt.records[q][fd.groupby[1]],
            value: dt.records[q][metricValue],
            fromValue: mapFromValueData[dt.records[q][fd.groupby[1]]] ? mapFromValueData[dt.records[q][fd.groupby[1]]] : 0,
            toValue: mapToValueData[dt.records[q][fd.groupby[1]]] ? mapToValueData[dt.records[q][fd.groupby[1]]] : 0
          }]);
        }
        mapData.push(['全国', chinaData]);

        for (let m = 0; m < fromCityArr.length; m++) {
          const cityData = [];
          for (let n = 0; n < dt.records.length; n++) {
            if(dt.records[n][fd.groupby[0]] === fromCityArr[m]){
              cityData.push([{
                name: dt.records[n][fd.groupby[0]],
                fromValue: mapFromValueData[dt.records[n][fd.groupby[0]]] ? mapFromValueData[dt.records[n][fd.groupby[0]]] : 0,
                toValue: mapToValueData[dt.records[n][fd.groupby[0]]] ? mapToValueData[dt.records[n][fd.groupby[0]]] : 0
              },
              {
                name: dt.records[n][fd.groupby[1]],
                value: dt.records[n][metricValue],
                fromValue: mapFromValueData[dt.records[n][fd.groupby[1]]] ? mapFromValueData[dt.records[n][fd.groupby[1]]] : 0,
                toValue: mapToValueData[dt.records[n][fd.groupby[1]]] ? mapToValueData[dt.records[n][fd.groupby[1]]] : 0
              }]);
            }
          }
          mapData.push([fromCityArr[m], cityData]);
        }

        var convertData = function (data) {
          var res = [];
          for (var i = 0; i < data.length; i++) {
            var dataItem = data[i];
            var fromCoord = geoCoordMap[dataItem[0].name];
            var toCoord = geoCoordMap[dataItem[1].name];
            if (fromCoord && toCoord) {
              res.push([{
                coord: fromCoord
              },
              {
                coord: toCoord,
                value: dataItem[1].value
              }]);
            }
          }
          return res;
        };

        const series = [];
        const legendData = [];
        mapData.forEach(function (item, i) {
          series.push(
          {
            name: item[0],
            type: 'effectScatter',
            coordinateSystem: 'geo',
            zlevel: 2,
            rippleEffect: {
              brushType: 'stroke'
            },
            label: {
              normal: {
                show: true,
                position: 'right',
                formatter: '{b}'
              }
            },
            symbolSize: function (val) {
              return 10;
            },
            showEffectOn: 'render',
            itemStyle: {
              normal: {
                color: '#46bee9'
              }
            },
            data: item[1].map(function (dataItem) {
              return {
                name: dataItem[0].name,
                value: geoCoordMap[dataItem[0].name].concat(dataItem[1].value),
                fromValue: [dataItem[0].fromValue],
                toValue: [dataItem[0].toValue]
              };
            })
          },
          {
            name: item[0],
            type: 'lines',
            zlevel: 2,
            symbol: ['none', 'arrow'],
            symbolSize: 10,
            effect: {
              show: true,
              period: 6,
              trailLength: 0,
              symbol: planePath,
              symbolSize: 15
            },
            lineStyle: {
              normal: {
                color: '#46bee9',
                width: 1,
                opacity: 0.6,
                curveness: 0.2
              }
            },
            data: convertData(item[1])
          },
          {
            name: item[0],
            type: 'effectScatter',
            coordinateSystem: 'geo',
            zlevel: 2,
            rippleEffect: {
              brushType: 'stroke'
            },
            label: {
              normal: {
                show: true,
                position: 'right',
                formatter: '{b}'
              }
            },
            symbolSize: function (val) {
              return 10;
            },
            showEffectOn: 'render',
            itemStyle: {
              normal: {
                color: '#46bee9'
              }
            },
            data: item[1].map(function (dataItem) {
              return {
                name: dataItem[1].name,
                value: geoCoordMap[dataItem[1].name].concat(dataItem[1].value),
                fromValue: [dataItem[1].fromValue],
                toValue: [dataItem[1].toValue]
              };
            })
          });
          legendData.push(item[0]);
        });

        const option = {
          backgroundColor: '#404a59',
          animation: true,
          animationDuration: 1000,
          animationEasing: 'cubicInOut',
          animationDurationUpdate: 1000,
          animationEasingUpdate: 'cubicInOut',
          title : {
            // text: '模拟迁徙',
            // subtext: '数据纯属虚构',
            left: 'center',
            textStyle : {
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
            roam: true,
            itemStyle: {
              normal: {
                areaColor: '#323c48',
                borderColor: '#404a59'
              },
              emphasis: {
                areaColor: '#2a333d'
              }
            }
          },
          visualMap: {
            type: 'continuous',
            min: 0,
            max: 2500,
            left: 'left',
            top: 'bottom',
            calculable : true,
            color: ['orange', 'yellow','lime','aqua'],
            textStyle:{
              color:'#fff'
            }
          },
          tooltip: {
            trigger: 'item',
            formatter: function (params) {
              var res = params.name;
              if (params.seriesType === 'effectScatter') {
                res += '<br/>' + ' 迁出' + metricValue + ' : ' + params.data.fromValue[0] + '</br>';
                res += ' 迁入' + metricValue + ' : ' + params.data.toValue[0] + '</br>';
              }
              return res;
            }
          },
          legend: {
            orient: 'vertical',
            top: 'bottom',
            left: 'right',
            data: legendData,
            textStyle: {
              color: '#fff'
            },
            selectedMode: 'single'
          },
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
              restore: {},
              saveAsImage: {
                show: true
              }
            }
          },
          series: series
        };
        option.visualMap.min = min_value ? parseInt(min_value) : parseInt(option.visualMap.min);
        option.visualMap.max = max_value ? parseInt(max_value) : parseInt(option.visualMap.max);
        chart.setOption(option);
        slice.container.css('height', height + 'px');
        return chart;
      }
        const graph = drawGraph();
  };

  render();
}

module.exports = chinaCityMapMigrationVis;
