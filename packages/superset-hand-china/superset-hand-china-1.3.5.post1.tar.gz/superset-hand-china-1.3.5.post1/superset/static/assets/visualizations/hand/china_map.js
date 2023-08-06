const d3 = require('d3');
const echarts = require('echarts');
const $ = require('jquery');
require('./china.js');

function chinaMapVis(slice, payload, theme) {
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
      let metrics = fd['metrics'];
      const groupby = fd['groupby_one'];
      const max_value = fd['max_legend'];
      const min_value = fd['min_legend'];

      const drawGraph = function () {
        const seris = [];
        metrics.forEach(function (metric, index, array) {
          const data = [];
          dt.records.forEach(function (item, index, array) {
            data.push({ name: item[groupby], value: item[metric] });
          });
          const serie = {
            zlevel: 1,
            name: metric,
            type: 'map',
            mapType: 'china',
            selectedMode: 'multiple',
            roam: true,
            // left: 0,
            // right: '15%',
            label: {
              normal: {
                show: true
              },
              emphasis: {
                show: true
              }
            },
            data: data,
          };
          seris.push(serie);
        });

        const option = {
          center: [107.04, 33.08],
          zoom: 5,
          tooltip: {
            trigger: 'item',
            formatter: function (params) {
              var res = params.name + '<br/>';
              var myseries = option.series;
              for (var i = 0; i < myseries.length; i++) {
                if (myseries[i].name) {
                  res += myseries[i].name;
                  for (var j = 0; j < myseries[i].data.length; j++) {
                    if (myseries[i].data[j].name == params.name) {
                      res += ' : ' + myseries[i].data[j].value + '</br>';
                    }
                  }
                }
              }
              return res;
            }
          },
          legend: {
            orient: 'vertical',
            left: 'left',
            data: metrics,
          },
          visualMap: {
            min: 0,
            max: 2500,
            left: 'left',
            top: 'bottom',
            // text: [localMessage.high, localMessage.low],           // 文本，默认为数值文本
            calculable: true
          },
          toolbox: {
            show: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            feature: {
              dataView: { readOnly: false },
              restore: {},
              saveAsImage: {}
            }
          },
          series: seris
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

module.exports = chinaMapVis;