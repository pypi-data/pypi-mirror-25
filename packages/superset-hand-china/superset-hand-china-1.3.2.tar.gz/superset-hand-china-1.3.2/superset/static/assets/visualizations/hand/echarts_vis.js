// JS
const d3 = require('d3');
const echarts = require('echarts');
const $ = require('jquery');
require('echarts-wordcloud');
require('./SliceTheme.js');
const formatNumber = d3.format(',.2f');

function getTreeData(data, pid) {
  var result = [], temp;
  for (var i = 0; i < data.length; i++) {
    if (data[i].pid == pid) {
      var obj = { "name": data[i].name, "id": data[i].id, "value": data[i].value };
      temp = getTreeData(data, data[i].id);
      if (temp.length > 0) {
        obj.children = temp;
      }
      result.push(obj);
    }
  }
  return result;
}

function isValidNumber(num) {
  return num != null && isFinite(num);
}

function getLevelOption() {
  return [
    {
      itemStyle: {
        normal: {
          borderColor: '#777',
          borderWidth: 0,
          gapWidth: 1
        }
      },
      upperLabel: {
        normal: {
          show: false
        }
      }
    },
    {
      itemStyle: {
        normal: {
          borderColor: '#555',
          borderWidth: 5,
          gapWidth: 1
        },
        emphasis: {
          borderColor: '#ddd'
        }
      }
    },
    {
      colorSaturation: [0.35, 0.5],
      itemStyle: {
        normal: {
          borderWidth: 5,
          gapWidth: 1,
          borderColorSaturation: 0.6
        }
      }
    }
  ];
}

function echartsVis(slice, payload, theme) {

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

    // some globe letibles
    const pie_data = [];
    const series = [];
    let legend = [];

    const xAxis = [];
    const yAxis = [];

    // set the height step
    let steps = 15;
    if (height <= 200) {
      steps = 40;
    } else if (height > 200 && height <= 320) {
      steps = 30;
    }

    let myOptions = null;
    // common properties
    let options = {
      height: height * 0.75 - steps,
      grid: {
        right: fd.right_padding == null ? '0%' : fd.right_padding,
        left: fd.left_padding == null ? '0%' : fd.left_padding,
        top: fd.top_padding == null ? '0%' : fd.top_padding,
        bottom: fd.bottom_padding == null ? '0%' : fd.bottom_padding,
        containLabel: true,
      },
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'cross',
          crossStyle: {
            color: '#999'
          }
        },
        formatter: function (list) {
          let tip = '';
          list.forEach(l => {
            tip += l.seriesName + ': ' + slice.d3format(l.seriesName, l.value) + '<br/>';
          });
          return tip;
        },
      },
      toolbox: {
        show: true,
        feature: {
          dataView: { show: true, readOnly: true },
          restore: { show: true },
          saveAsImage: { show: true }
        }
      },
    };

    const pie_tooltip = {
      trigger: 'item',
      axisPointer: {
        type: 'cross',
        crossStyle: {
          color: '#999'
        }
      },
      formatter: function (obj) {
        let tip = obj.seriesName + '<br/>' + obj.name + ': ' + slice.d3format(obj.name, obj.value) + '(' + obj.percent + '%)';
        return tip;
      },
    };
    const formatterLabel = function (obj, label_format) {
      label_format === '' ? '{d}%' : label_format;
      let str = label_format.replace('{a}', obj.seriesName);
      str = str.replace('{b}', obj.name);
      str = str.replace('{c}', slice.d3format(obj.name, obj.value));
      str = str.replace('{d}', obj.percent);
      return str;
    }

    const bar_line_toolbox = {
      show: true,
      feature: {
        magicType: { show: true, type: ['line', 'bar'] },
        dataView: { show: true, readOnly: true },
        restore: { show: true },
        saveAsImage: { show: true }
      }
    };

    let common_series = null;
    const format_label = function (show, position) {
      return {
        normal: {
          show: show,
          position: position,
          formatter: function (obj) {
            return slice.d3format(obj.seriesName, obj.value);
          }
        }
      }
    }
    if ($.inArray(fd.viz_type, ['echarts_bar', 'echarts_bar_h', 'echarts_line', 'echarts_line_bar']) != -1) {
      common_series = {
        markPoint: {
          symbolSize: 40,
          data: [
            {
              type: fd.is_max_min == false ? null : 'max',
              name: '最大值',
              label: format_label(true, fd.viz_type !== 'echarts_bar_h' ? 'top' : 'right')
            },
            {
              type: fd.is_max_min == false ? null : 'min',
              name: '最小值',
              label: format_label(true, fd.viz_type !== 'echarts_bar_h' ? 'top' : 'right')
            }
          ]
        },
        markLine: {
          data: fd.is_avg === true ? [
            {
              type: 'average',
              name: '平均值',
              label: format_label(true, 'end')
            }
          ] : null
        },
        label: format_label(fd.is_bar_value, fd.viz_type !== 'echarts_bar_h' ? 'top' : 'right')
      }
    }

    const formatAxias = function (value, format) {
      if (format === undefined || format === '') {
        return value;
      }
      const expr = format.substring(format.indexOf('{') + 1, format.indexOf('}'));
      return format.substring(0, format.indexOf('{')) + eval(expr) + format.substring(format.indexOf('}') + 1);
    }
    const drawGraph = function () {
      switch (fd.viz_type) {
        case 'echarts_bar':
          // setup the xAxis from fd.groupby
          for (let i = 0; i < fd.groupby.length; i++) {
            const xAxisValue = [];
            dt.records.forEach(d => {
              xAxisValue.push(d[fd.groupby[i]])
            });
            xAxis[i] = {
              type: 'category',
              data: xAxisValue,
              position: 'bottom',
              offset: 25 * i,
              axisPointer: {
                type: 'shadow'
              },
              axisLabel: {
                formatter: function (value) {
                  let result = '';
                  if (value.length > 8) {
                    result = value.substring(0, 8) + "...";
                  } else {
                    result = value;
                  }
                  return result;
                }
              }
            }
          }

          if (fd.y_metrics && fd.only_left) {
            // 1.setup the legend from fd.metrics
            legend = fd.y_metrics;
            // 2.setup yAxis
            const y_degree_p = fd.y_degree === '' ? {} : $.parseJSON(fd.y_degree);
            yAxis.push({
              type: 'value',
              name: fd.y_axis_name,
              position: 'left',
              axisLabel: {
                formatter: function (value) {
                  return formatAxias(value, fd.y_format);
                }
              },
              min: y_degree_p.min,
              max: y_degree_p.max,
            });
            // 3.setup the series
            for (let i = 0; i < fd.y_metrics.length; i++) {
              const yAxisValue = [];
              dt.records.forEach(d => {
                yAxisValue.push(d[fd.y_metrics[i]])
              });
              const props = {
                name: fd.y_metrics[i],
                type: 'bar',
                data: yAxisValue,
              };

              // set stack
              fd.stacks.forEach(function (stack, index) {
                if ($.inArray(fd.y_metrics[i], stack.metrics.split(',')) != -1) {
                  // the metric in this stack
                  props.stack = stack.name;
                }
              });
              series.push($.extend(props, common_series));
            }

          } else if (!fd.only_left) {
            // 1.setup the legend from fd.metrics
            legend = fd.y_left_metrics.concat(fd.y_right_metrics);
            // 2-0. left of the Y axis
            for (let i = 0; i < fd.y_left_metrics.length; i++) {
              const k = i;
              let y_degree_p = fd.y_left_degree === '' ? {} : $.parseJSON(fd.y_left_degree.split(';')[i]);
              yAxis.push({
                type: 'value',
                name: fd.y_left_metrics[i],
                offset: 80 * i,
                position: 'left',
                axisLabel: {
                  formatter: function (value) {
                    return formatAxias(value, fd.y_left_format.split(';')[k]);
                  }
                },
                min: y_degree_p == {} ? 'null' : y_degree_p.min,
                max: y_degree_p == {} ? 'null' : y_degree_p.max,
              });
            }
            // 2-1.right of the Y axis
            for (let i = 0; i < fd.y_right_metrics.length; i++) {
              const k = i;
              const y_degree_p = fd.y_right_degree === '' ? {} : $.parseJSON(fd.y_right_degree.split(';')[i]);
              yAxis.push({
                type: 'value',
                name: fd.y_right_metrics[i],
                offset: 80 * i,
                position: 'right',
                axisLabel: {
                  formatter: function (value) {
                    return formatAxias(value, fd.y_right_format.split(';')[k]);
                  }
                },
                min: y_degree_p == {} ? 'null' : y_degree_p.min,
                max: y_degree_p == {} ? 'null' : y_degree_p.max,
              });
            }
            // 3-0. left of the axis series
            for (let i = 0; i < fd.y_left_metrics.length; i++) {
              const yAxisValue = [];
              dt.records.forEach(d => {
                yAxisValue.push(d[fd.y_left_metrics[i]])
              });
              series.push(
                $.extend({
                  name: fd.y_left_metrics[i],
                  type: 'bar',
                  yAxisIndex: i,
                  data: yAxisValue,
                }, common_series)
              );
            }
            // 3-1. right of the axis series
            for (let i = 0; i < fd.y_right_metrics.length; i++) {
              const yAxisValue = [];
              dt.records.forEach(d => {
                yAxisValue.push(d[fd.y_right_metrics[i]])
              });
              series.push(
                $.extend({
                  name: fd.y_right_metrics[i],
                  type: 'bar',
                  yAxisIndex: i + parseInt(fd.y_left_metrics.length),
                  data: yAxisValue,
                }, common_series)
              );
            }
          }

          if (fd.enabled_bar_width) {
            myOptions = {
              toolbox: bar_line_toolbox,
              legend: {
                data: legend,
                left: 'left',
                itemWidth: 10,
                itemHeigt: 10
              },
              barWidth: fd.bar_width,
              xAxis: xAxis,
              yAxis: yAxis,
              series: series
            };
          } else {
            myOptions = {
              toolbox: bar_line_toolbox,
              legend: {
                data: legend,
                left: 'left',
                itemWidth: 10,
                itemHeigt: 10
              },
              xAxis: xAxis,
              yAxis: yAxis,
              series: series
            };
          }
          options = $.extend(options, myOptions);
          break;
        case 'echarts_bar_h':
          // setup yAxis from fd.groupby
          for (let i = 0; i < fd.groupby.length; i++) {
            const yAxisValue = [];
            for (let j = dt.records.length - 1; j >= 0; j--) {
              yAxisValue.push(dt.records[j][fd.groupby[i]]);
            }
            yAxis[i] = {
              type: 'category',
              data: yAxisValue,
              position: 'left',
              offset: 25 * i,
              axisPointer: {
                type: 'shadow'
              },
              axisLabel: {
                formatter: function (value) {
                  let result = '';
                  if (value.length > 8) {
                    result = value.substring(0, 8) + "...";
                  } else {
                    result = value;
                  }
                  return result;
                }
              }
            }
          }

          if (fd.x_metrics && fd.only_bottom) {
            // 1.setup the legend from fd.metrics
            legend = fd.x_metrics;

            // 2.setup xAxis
            const x_degree_p = fd.x_degree === '' ? {} : $.parseJSON(fd.x_degree);
            xAxis.push({
              type: 'value',
              name: fd.x_axis_name,
              position: 'left',
              axisLabel: {
                formatter: function (value) {
                  return formatAxias(value, fd.x_format);
                }
              },
              min: x_degree_p.min,
              max: x_degree_p.max,
            });

            // 3.setup the series
            for (let i = 0; i < fd.x_metrics.length; i++) {
              const xAxisValue = [];
              for (let j = dt.records.length - 1; j >= 0; j--) {
                xAxisValue.push(dt.records[j][fd.x_metrics[i]]);
              }
              const props = {
                name: fd.x_metrics[i],
                type: 'bar',
                data: xAxisValue,
              };
              // set stack
              fd.stacks.forEach(function (stack, index) {
                if ($.inArray(fd.x_metrics[i], stack.metrics.split(',')) != -1) {
                  // the metric in this stack
                  props.stack = stack.name;
                }
              });
              series.push(
                $.extend(props, common_series)
              );
            }

          } else if (!fd.only_bottom) {
            // 1.setup the legend from fd.metrics
            legend = fd.x_bottom_metrics.concat(fd.x_top_metrics);

            // 2-0. bottom of the xAxis
            for (let i = 0; i < fd.x_bottom_metrics.length; i++) {
              const k = i;
              const x_degree_p = fd.x_bottom_degree === '' ? {} : $.parseJSON(fd.x_bottom_degree.split(';')[i]);
              xAxis.push({
                type: 'value',
                name: fd.x_bottom_metrics[i],
                offset: 80 * i,
                position: 'bottom',
                axisLabel: {
                  formatter: function (value) {
                    return formatAxias(value, fd.x_bottom_format.split(';')[k]);
                  }
                },
                min: x_degree_p == {} ? 'null' : x_degree_p.min,
                max: x_degree_p == {} ? 'null' : x_degree_p.max,
              });
            }

            // 2-1.top of the xAxis
            for (let i = 0; i < fd.x_top_metrics.length; i++) {
              const k = i;
              const x_degree_p = fd.x_top_degree === '' ? {} : $.parseJSON(fd.x_top_degree.split(';')[i]);
              xAxis.push({
                type: 'value',
                name: fd.x_top_metrics[i],
                offset: 80 * i,
                position: 'top',
                axisLabel: {
                  formatter: function (value) {
                    return formatAxias(value, fd.x_top_format.split(';')[k]);
                  }
                },
                min: x_degree_p == {} ? 'null' : x_degree_p.min,
                max: x_degree_p == {} ? 'null' : x_degree_p.max,
              });
            }

            // 3-0. bottom of the axis series
            for (let i = 0; i < fd.x_bottom_metrics.length; i++) {
              const xAxisValue = [];
              // dt.records.forEach(d => {
              //   xAxisValue.push(d[fd.x_bottom_metrics[i]]);
              // });
              for (var j = dt.records.length - 1; j >= 0; j--) {
                xAxisValue.push(dt.records[j][fd.x_bottom_metrics[i]]);
              }
              series.push(
                $.extend({
                  name: fd.x_bottom_metrics[i],
                  type: 'bar',
                  xAxisIndex: i,
                  data: xAxisValue,
                }, common_series)
              );
            }

            // 3-1. top of the axis series
            for (let i = 0; i < fd.x_top_metrics.length; i++) {
              const xAxisValue = [];
              // dt.records.forEach(d => {
              //   xAxisValue.push(d[fd.x_top_metrics[i]]);
              // });
              for (var j = dt.records.length - 1; j >= 0; j--) {
                xAxisValue.push(dt.records[j][fd.x_top_metrics[i]]);
              }
              series.push(
                $.extend({
                  name: fd.x_top_metrics[i],
                  type: 'bar',
                  xAxisIndex: i + parseInt(fd.x_bottom_metrics.length),
                  data: xAxisValue,
                }, common_series)
              );
            }
          }

          if (fd.enabled_bar_width) {
            myOptions = {
              toolbox: bar_line_toolbox,
              legend: {
                data: legend,
                left: 'left',
                itemWidth: 10,
                itemHeigt: 10
              },
              barWidth: fd.bar_width,
              xAxis: xAxis,
              yAxis: yAxis,
              series: series
            };
          } else {
            myOptions = {
              toolbox: bar_line_toolbox,
              legend: {
                data: legend,
                left: 'left',
                itemWidth: 10,
                itemHeigt: 10
              },
              xAxis: xAxis,
              yAxis: yAxis,
              series: series
            };
          }
          options = $.extend(options, myOptions);
          break;

        case 'echarts_bar_progress':
          // setup yAxis from fd.groupby
          for (let i = 0; i < fd.groupby.length; i++) {
            const yAxisValue = [];
            for (let j = dt.records.length - 1; j >= 0; j--) {
              yAxisValue.push(dt.records[j][fd.groupby[i]]);
            }
            yAxis[i] = {
              type: 'category',
              data: yAxisValue,
              position: 'left',
              offset: 25 * i,
              axisPointer: {
                type: 'shadow'
              },
              axisLabel: {
                formatter: function (value) {
                  let result = '';
                  if (value.length > 8) {
                    result = value.substring(0, 8) + "...";
                  } else {
                    result = value;
                  }
                  return result;
                }
              }
            }
          }

          // 2.setup xAxis
          const x_degree_p = fd.x_degree === '' ? {} : $.parseJSON(fd.x_degree);
          xAxis.push({
            type: 'value',
            name: fd.x_axis_name,
            position: 'top',
            axisLabel: {
              formatter: function (value) {
                let format = fd.x_format;
                if (format === undefined || format === '') {
                  return value * 100 + '%';
                }
                const expr = format.substring(format.indexOf('{') + 1, format.indexOf('}'));
                return format.substring(0, format.indexOf('{')) + eval(expr) + format.substring(format.indexOf('}') + 1);
              }
            },
            min: x_degree_p.min,
            max: x_degree_p.max,
          });
          // set stack
          let stack_metrics = [];
          fd.stacks.forEach(stack => {
            stack_metrics = stack_metrics.concat(stack.metrics.split(','));
          });
          // 3.setup the series
          let pre = 0, next = 0;
          // Each two in one group
          const groupData = [];
          for (let j = dt.records.length - 1; j >= 0; j--) {
            for (let i = 0; i < stack_metrics.length; i++) {
              if (i % 2 === 0) {
                pre = dt.records[j][stack_metrics[i]];
              }
              if (i % 2 === 1) {
                next = dt.records[j][stack_metrics[i]];
                groupData.push(Math.abs(parseFloat(pre / next).toFixed(2)));
                groupData.push(Math.abs(parseFloat((next - pre) / next).toFixed(2)));
              }
            }
          }

          // deal groupData
          let xAxisValue = [];
          // init xAxisValue
          for (let i = 0; i < stack_metrics.length; i++) {
            xAxisValue[i] = [];
          }
          for (let j = 0; j < groupData.length; j++) {
            xAxisValue[j % stack_metrics.length].push(groupData[j]);
          }

          // console.info(xAxisValue);
          // console.info(stack_metrics);

          for (let i = 0; i < stack_metrics.length; i++) {
            const props = {
              name: stack_metrics[i],
              type: 'bar',
              data: xAxisValue[i],
              // stack: fd['stack_name_' + (parseInt(i / 2) + 1)]
              stack: fd.stacks[parseInt(i / 2)].name
            };
            series.push(
              $.extend(props, common_series)
            );
          }
          if (fd.enabled_bar_width) {
            myOptions = {
              toolbox: bar_line_toolbox,
              legend: {
                data: stack_metrics,
                left: 'left',
                itemWidth: 10,
                itemHeigt: 10
              },
              xAxis: xAxis,
              yAxis: yAxis,
              barWidth: fd.bar_width,
              series: series,
              tooltip: {
                trigger: 'axis',
                axisPointer: {
                  type: 'cross',
                  crossStyle: {
                    color: '#999'
                  }
                },
                formatter: function (list) {
                  console.info(list);
                  let tip = '';
                  list.forEach(function (item, index) {
                    if (index % 2 === 0) {
                      tip += item.seriesName + '(进度: ' + item.value * 100 + '%)<br/>';
                    }
                  });
                  return tip;
                },
              },
            };
          } else {
            myOptions = {
              toolbox: bar_line_toolbox,
              legend: {
                data: stack_metrics,
                left: 'left',
                itemWidth: 10,
                itemHeigt: 10
              },
              xAxis: xAxis,
              yAxis: yAxis,
              series: series,
              tooltip: {
                trigger: 'axis',
                axisPointer: {
                  type: 'cross',
                  crossStyle: {
                    color: '#999'
                  }
                },
                formatter: function (list) {
                  console.info(list);
                  let tip = '';
                  list.forEach(function (item, index) {
                    if (index % 2 === 0) {
                      tip += item.seriesName + '(进度: ' + item.value * 100 + '%)<br/>';
                    }
                  });
                  return tip;
                },
              },
            };
          }
          options = $.extend(options, myOptions);
          break;

        case 'echarts_line':
          // setup the xAxis from fd.groupby
          for (let i = 0; i < fd.groupby.length; i++) {
            const xAxisValue = [];
            dt.records.forEach(d => {
              xAxisValue.push(d[fd.groupby[i]]);
            });
            xAxis[i] = {
              type: 'category',
              data: xAxisValue,
              position: 'bottom',
              offset: 25 * i,
              axisPointer: {
                type: 'shadow'
              },
              axisLabel: {
                formatter: function (value) {
                  let result = '';
                  if (value.length > 8) {
                    result = value.substring(0, 8) + "...";
                  } else {
                    result = value;
                  }
                  return result;
                }
              }
            };
          }

          // set diffirent yAxis
          if (fd.y_metrics && fd.only_left) {
            // 1.setup the legend from fd.metrics
            legend = fd.y_metrics;

            // 2.setup yAxis
            const y_degree_p = fd.y_degree === '' ? {} : $.parseJSON(fd.y_degree);
            yAxis.push({
              type: 'value',
              name: fd.y_axis_name,
              position: 'left',
              axisLabel: {
                formatter: function (value) {
                  return formatAxias(value, fd.y_format);
                }
              },
              min: y_degree_p.min,
              max: y_degree_p.max,
            })

            // 3.setup the series from the fd.metrics and dt.records
            for (let i = 0; i < fd.y_metrics.length; i++) {
              const yAxisValue = [];
              dt.records.forEach(d => {
                yAxisValue.push(d[fd.y_metrics[i]]);
              });
              series.push(
                $.extend({
                  name: fd.y_metrics[i],
                  type: 'line',
                  data: yAxisValue,
                }, common_series)
              );
            }
          } else if (!fd.only_left) {
            // 1.setup the legend from fd.metrics
            legend = fd.y_left_metrics.concat(fd.y_right_metrics);

            // 2-0. left of the Y axis
            for (let i = 0; i < fd.y_left_metrics.length; i++) {
              const k = i;
              const y_degree_p = fd.y_left_degree === '' ? {} : $.parseJSON(fd.y_left_degree.split(';')[i]);
              yAxis.push({
                type: 'value',
                name: fd.y_left_metrics[i],
                offset: 80 * i,
                position: 'left',
                splitLine: {
                  show: fd.y_left_splitLine,
                },
                axisLabel: {
                  formatter: function (value) {
                    return formatAxias(value, fd.y_left_format.split(';')[k]);
                  }
                },
                min: y_degree_p == {} ? 'null' : y_degree_p.min,
                max: y_degree_p == {} ? 'null' : y_degree_p.max,
              })
            }

            // 2-1.right of the Y axis
            if (fd.y_right_metrics) {
              for (let i = 0; i < fd.y_right_metrics.length; i++) {
                const k = i;
                const y_degree_p = fd.y_right_degree === '' ? {} : $.parseJSON(fd.y_right_degree.split(';')[i]);
                yAxis.push({
                  type: 'value',
                  name: fd.y_right_metrics[i],
                  offset: 80 * i,
                  position: 'right',
                  splitLine: {
                    show: fd.y_right_splitLine,
                  },
                  axisLabel: {
                    formatter: function (value) {
                      return formatAxias(value, fd.y_right_format.split(';')[k]);
                    }
                  },
                  min: y_degree_p == {} ? 'null' : y_degree_p.min,
                  max: y_degree_p == {} ? 'null' : y_degree_p.max,
                })
              }
            }

            // 3-0. left of the axis series
            for (let i = 0; i < fd.y_left_metrics.length; i++) {
              const yAxisValue = [];
              dt.records.forEach(d => {
                yAxisValue.push(d[fd.y_left_metrics[i]]);
              });
              series.push(
                $.extend({
                  name: fd.y_left_metrics[i],
                  type: 'line',
                  yAxisIndex: i,
                  data: yAxisValue,
                }, common_series)
              );
            }

            // 3-1. right of the axis series
            for (let i = 0; i < fd.y_right_metrics.length; i++) {
              const yAxisValue = [];
              dt.records.forEach(d => {
                yAxisValue.push(d[fd.y_right_metrics[i]]);
              });
              series.push(
                $.extend({
                  name: fd.y_right_metrics[i],
                  type: 'line',
                  yAxisIndex: i + parseInt(fd.y_left_metrics.length),
                  data: yAxisValue,
                }, common_series)
              );
            }
          }

          myOptions = {
            toolbox: bar_line_toolbox,
            legend: {
              data: legend,
              left: 'left',
              itemWidth: 10,
              itemHeigt: 10
            },
            xAxis: xAxis,
            yAxis: yAxis,
            series: series
          };
          options = $.extend(options, myOptions);
          break;
        case 'echarts_line_bar':
          // setup the xAxis from fd.groupby
          for (let i = 0; i < fd.groupby.length; i++) {
            const xAxisValue = [];
            dt.records.forEach(d => {
              xAxisValue.push(d[fd.groupby[i]])
            });
            xAxis[i] = {
              type: 'category',
              data: xAxisValue,
              position: 'bottom',
              offset: 25 * i,
              axisPointer: {
                type: 'shadow'
              },
              axisLabel: {
                formatter: function (value) {
                  let result = '';
                  if (value.length > 8) {
                    result = value.substring(0, 8) + "...";
                  } else {
                    result = value;
                  }
                  return result;
                }
              }
            };
          }

          if (fd.y_metrics && fd.only_left) {
            // 1.setup the legend from fd.metrics
            legend = fd.y_metrics;
            // 2.setup yAxis
            const y_degree_p = fd.y_degree === '' ? {} : $.parseJSON(fd.y_degree);
            yAxis.push({
              type: 'value',
              name: fd.y_axis_name,
              position: 'left',
              axisLabel: {
                formatter: function (value) {
                  return formatAxias(value, fd.y_format);
                }
              },
              min: y_degree_p.min,
              max: y_degree_p.max,
            });
            // 3.setup the series
            for (let i = 0; i < fd.y_metrics.length; i++) {
              const yAxisValue = [];
              dt.records.forEach(d => {
                yAxisValue.push(d[fd.y_metrics[i]]);
              });
              let props = {
                name: fd.y_metrics[i],
                type: $.inArray(fd.y_metrics[i], fd.line_choice) !== -1 ? 'line' : 'bar',
                data: yAxisValue,
              };
              if (props.type === 'bar') {
                fd.stacks.forEach(function (stack, index) {
                  if ($.inArray(fd.y_metrics[i], stack.metrics.split(',')) != -1) {
                    // the metric in this stack
                    props.stack = stack.name;
                  }
                });
              }
              series.push(
                $.extend(props, common_series)
              );
            }

          } else if (!fd.only_left) {
            // 1.setup the legend from fd.metrics
            legend = fd.y_left_metrics.concat(fd.y_right_metrics);
            // 2-0. left of the Y axis
            for (let i = 0; i < fd.y_left_metrics.length; i++) {
              const k = i;
              const y_degree_p = fd.y_left_degree === '' ? {} : $.parseJSON(fd.y_left_degree.split(';')[i]);
              yAxis.push({
                type: 'value',
                name: fd.y_left_metrics[i],
                offset: 80 * i,
                position: 'left',
                axisLabel: {
                  formatter: function (value) {
                    return formatAxias(value, fd.y_left_format.split(';')[k]);
                  }
                },
                min: y_degree_p == {} ? 'null' : y_degree_p.min,
                max: y_degree_p == {} ? 'null' : y_degree_p.max,
              });
            }
            // 2-1.right of the Y axis
            for (let i = 0; i < fd.y_right_metrics.length; i++) {
              const k = i;
              const y_degree_p = fd.y_right_degree === '' ? {} : $.parseJSON(fd.y_right_degree.split(';')[i]);
              yAxis.push({
                type: 'value',
                name: fd.y_right_metrics[i],
                offset: 80 * i,
                position: 'right',
                axisLabel: {
                  formatter: function (value) {
                    return formatAxias(value, fd.y_right_format.split(';')[k]);
                  }
                },
                min: y_degree_p == {} ? 'null' : y_degree_p.min,
                max: y_degree_p == {} ? 'null' : y_degree_p.max,
              });
            }
            // 3-0. left of the axis series
            for (let i = 0; i < fd.y_left_metrics.length; i++) {
              const yAxisValue = [];
              dt.records.forEach(d => {
                yAxisValue.push(d[fd.y_left_metrics[i]]);
              });
              series.push(
                $.extend({
                  name: fd.y_left_metrics[i],
                  type: $.inArray(fd.y_left_metrics[i], fd.line_choice) !== -1 ? 'line' : 'bar',
                  yAxisIndex: i,
                  data: yAxisValue,
                }, common_series)
              );
            }
            // 3-1. right of the axis series
            for (let i = 0; i < fd.y_right_metrics.length; i++) {
              const yAxisValue = [];
              dt.records.forEach(d => {
                yAxisValue.push(d[fd.y_right_metrics[i]]);
              });
              series.push(
                $.extend({
                  name: fd.y_right_metrics[i],
                  type: $.inArray(fd.y_right_metrics[i], fd.line_choice) !== -1 ? 'line' : 'bar',
                  yAxisIndex: i + parseInt(fd.y_left_metrics.length),
                  data: yAxisValue,
                }, common_series)
              );
            }
          }
          if (fd.enabled_bar_width) {
            myOptions = {
              toolbox: bar_line_toolbox,
              legend: {
                data: legend,
                left: 'left',
                itemWidth: 10,
                itemHeigt: 10
              },
              barWidth: fd.bar_width,
              xAxis: xAxis,
              yAxis: yAxis,
              series: series
            };
          } else {
            myOptions = {
              toolbox: bar_line_toolbox,
              legend: {
                data: legend,
                left: 'left',
                itemWidth: 10,
                itemHeigt: 10
              },
              xAxis: xAxis,
              yAxis: yAxis,
              series: series
            };
          }
          options = $.extend(options, myOptions);
          break;
        case 'echarts_pie_m':
          for (let i = 0; i < fd.metrics.length; i++) {
            dt.records.forEach(d => {
              pie_data.push({
                value: d[fd.metrics[i]],
                name: fd.metrics[i]
              })
            })
          }

          series.push({
            name: '',
            type: 'pie',
            data: pie_data,
            radius: [fd.circle_type === 'none' ? '0%' : (fd.circle_type === 'big' ? '40%'
              : (fd.circle_type === 'medium' ? '20%' : '10%')), '55%'],
            roseType: fd.rose_type == 'none' ? '' : fd.rose_type,
            label: {
              normal: {
                show: true,
                position: fd.label_position,
                formatter: function (obj) {
                  return formatterLabel(obj, fd.label_format);
                }
              }
            },
            tooltip: pie_tooltip
          });

          myOptions = {
            legend: {
              orient: 'vertical',
              left: 'left',
              itemWidth: 10,
              itemHeigt: 10,
              data: fd.metrics
            },
            series: series
          };
          options = $.extend(options, myOptions);
          break;
        case 'echarts_pie_h':
          const inner_data = [], outer_data = [];
          for (let i = 0; i < fd.inner_metrics.length; i++) {
            dt.records.forEach(d => {
              inner_data.push({
                value: d[fd.inner_metrics[i]],
                name: fd.inner_metrics[i]
              })
            })
          }

          for (let i = 0; i < fd.outer_metrics.length; i++) {
            dt.records.forEach(d => {
              outer_data.push({
                value: d[fd.outer_metrics[i]],
                name: fd.outer_metrics[i]
              })
            })
          }

          // inner circle
          series.push({
            name: '',
            type: 'pie',
            selectedMode: 'single',
            data: inner_data,
            radius: ['0', '30%'],
            label: {
              normal: {
                position: fd.inner_label_position,
                formatter: function (obj) {
                  return formatterLabel(obj, fd.inner_label_format);
                },
                textStyle: {
                  color: fd.inner_lable_color,
                }
              }
            },
            labelLine: {
              normal: {
                show: false
              }
            },
            tooltip: pie_tooltip
          });

          // outer pie
          series.push({
            name: '',
            type: 'pie',
            radius: ['40%', '55%'],
            data: outer_data,
            label: {
              normal: {
                show: true,
                position: fd.outer_label_position, //center
                formatter: function (obj) {
                  return formatterLabel(obj, fd.outer_label_format);
                }
              }
            },
            tooltip: pie_tooltip
          });

          myOptions = {
            legend: {
              orient: 'vertical',
              left: 'left',
              itemWidth: 10,
              itemHeigt: 10,
              data: fd.inner_metrics.concat(fd.outer_metrics)
            },
            series: series
          };
          options = $.extend(options, myOptions);
          break;
        case 'echarts_pie_g':
          for (let i = 0; i < fd.metrics.length; i++) {
            pie_data[i] = [];
            for (let j = 0; j < dt.records.length; j++) {
              pie_data[i][j] = {
                value: dt.records[j][fd.metrics[i]],
                name: dt.records[j][fd.groupby[0]],
              };
            }
          }

          for (let i = 0; i < fd.metrics.length; i++) {
            const w = parseInt(fd.col_num);
            const h = Math.ceil(fd.metrics.length / w);
            const r = 90 / (w * 2);
            const r2 = 80 / (h * 2);

            series.push({
              name: fd.metrics[i],
              type: 'pie',
              data: pie_data[i],
              center: [
                (5 + r * (1 + i % w * 2)) + '%',
                (15 + r2 * (1 + parseInt(i / w) * 2)) + '%',
              ],
              radius: [
                fd.circle_type === 'none' ? '0%' : (fd.circle_type === 'big' ? (80 / (fd.metrics.length + 1) + '%')
                  : (fd.circle_type === 'medium' ? (40 / (fd.metrics.length + 1) + '%') : (20 / (fd.metrics.length + 1) + '%'))),
                100 / (fd.metrics.length + 0.5) + '%',
              ],
              roseType: fd.rose_type == 'none' ? '' : fd.rose_type,
              label: {
                normal: {
                  show: true,
                  position: fd.label_position,
                  formatter: function (obj) {
                    return formatterLabel(obj, fd.label_format);
                  }
                }
              },
              tooltip: pie_tooltip
            });
          }
          for (let j = 0; j < dt.records.length; j++) {
            legend.push(dt.records[j][fd.groupby[0]]);
          }
          myOptions = {
            legend: {
              data: legend,
              left: 'left',
              itemWidth: 10,
              itemHeigt: 10
            },
            series: series
          };
          options = $.extend(options, myOptions)
          break;

        case 'echarts_pie_h_g':
          const pie_data_inner = [];
          const pie_data_outer = [];

          // inner--series
          const inner_items = [];
          const inner_metrics_data = [];
          for (let i = 0; i < dt.records.length; i++) {
            if ($.inArray(dt.records[i][fd.inner_metrics_one], inner_items) == -1) {
              inner_items.push(dt.records[i][fd.inner_metrics_one]);
            }
          }
          // console.info(inner_items);
          // get every groupby's data
          for (let i = 0; i < fd.metrics.length; i++) {
            inner_metrics_data[i] = [];
            for (let m = 0; m < inner_items.length; m++) {
              inner_metrics_data[i][m] = 0;
              for (let n = 0; n < dt.records.length; n++) {
                if (dt.records[n][fd.inner_metrics_one] === inner_items[m]) {
                  inner_metrics_data[i][m] += dt.records[n][fd.metrics[i]];
                }
              }
            }
          }
          // console.info(inner_metrics_data);

          for (let i = 0; i < fd.metrics.length; i++) {
            pie_data_inner[i] = [];
            for (let j = 0; j < inner_metrics_data[i].length; j++) {
              pie_data_inner[i][j] = {
                value: inner_metrics_data[i][j],
                name: inner_items[j],
              };
            }
          }

          for (let i = 0; i < fd.metrics.length; i++) {
            const w = parseInt(fd.col_num);
            const h = Math.ceil(fd.metrics.length / w);
            const r = 90 / (w * 2);
            const r2 = 80 / (h * 2);

            series.push({
              name: fd.metrics[i],
              type: 'pie',
              data: pie_data_inner[i],
              center: [
                // 100/(w + 1) * (i % w + 1) + '%',
                // 100/(h + 1) * (parseInt(i/w) +1) + '%',
                (5 + r * (1 + i % w * 2)) + '%',
                (15 + r2 * (1 + parseInt(i / w) * 2)) + '%',
              ],
              radius: [
                '0%',
                60 / (fd.metrics.length + 0.5) + '%',
              ],
              roseType: fd.rose_type == 'none' ? '' : fd.rose_type,
              label: {
                normal: {
                  show: true,
                  position: fd.inner_label_position,
                  formatter: function (obj) {
                    return formatterLabel(obj, fd.inner_label_format);
                  },
                  textStyle: {
                    color: fd.inner_lable_color,
                  }
                }
              },
              tooltip: pie_tooltip
            });
          }
          for (let j = 0; j < dt.records.length; j++) {
            legend.push(dt.records[j][fd.inner_metrics_one]);
          }

          // outer--series
          for (let i = 0; i < fd.metrics.length; i++) {
            pie_data_outer[i] = [];
            for (let j = 0; j < dt.records.length; j++) {
              let inner_groupby = null;
              if (fd.outer_metrics_one === fd.inner_metrics_one) {
                inner_groupby = fd.outer_metrics_one;
              } else {
                inner_groupby = fd.inner_metrics_one;
              }
              pie_data_outer[i][j] = {
                value: dt.records[j][fd.metrics[i]],
                name: dt.records[j][fd.outer_metrics_one],
                // name: '(' + dt.records[j][inner_groupby] + ') ' + dt.records[j][fd.outer_metrics_one],
              };
            }
          }

          for (let i = 0; i < fd.metrics.length; i++) {
            const w = parseInt(fd.col_num);
            const h = Math.ceil(fd.metrics.length / w);
            const r = 90 / (w * 2);
            const r2 = 80 / (h * 2);

            series.push({
              name: fd.metrics[i],
              type: 'pie',
              data: pie_data_outer[i],
              center: [
                // 100/(w + 1) * (i % w + 1) + '%',
                // 100/(h + 1) * (parseInt(i/w) +1) + '%',
                (5 + r * (1 + i % w * 2)) + '%',
                (15 + r2 * (1 + parseInt(i / w) * 2)) + '%',
              ],
              radius: [
                (85 / (fd.metrics.length + 1) + '%'),
                100 / (fd.metrics.length + 0.5) + '%',
              ],
              roseType: fd.rose_type == 'none' ? '' : fd.rose_type,
              label: {
                normal: {
                  show: true,
                  position: fd.outer_label_position,
                  formatter: function (obj) {
                    return formatterLabel(obj, fd.outer_label_format);
                  }
                }
              },
              tooltip: pie_tooltip,
            });
          }
          legend = inner_items;
          for (let j = 0; j < dt.records.length; j++) {
            legend.push(dt.records[j][fd.outer_metrics_one])
          }
          myOptions = {
            legend: {
              data: legend,
              left: 'left',
              itemWidth: 10,
              itemHeigt: 10
            },
            series: series
          };
          options = $.extend(options, myOptions)

          break;

        case 'echarts_radar_map':
          let map_indicator = [];
          let map_data = [];
          let max_data = [];
          let data;

          // get map data
          for (let i = 0; i < dt.records.length; i++) {
            data = [];
            for (let j = 0; j < fd.metrics.length; j++) {
              data.push(dt.records[i][fd.metrics[j]]);
            }
            map_data.push({
              value: data,
              name: dt.records[i][fd.groupby[0]],
            });
          }

          // get metrics max value
          for (let m = 0; m < fd.metrics.length; m++) {
            max_data[m] = 0;
            for (let n = 0; n < dt.records.length; n++) {
              if (max_data[m] < dt.records[n][fd.metrics[m]]) {
                max_data[m] = dt.records[n][fd.metrics[m]];
              }
            }
          }

          // get map indicator
          for (let m = 0; m < fd.metrics.length; m++) {
            map_indicator.push({
              name: fd.metrics[m],
              max: (max_data[m] * 1.2).toFixed(1),
            })
          }

          // get lengend
          for (let i = 0; i < dt.records.length; i++) {
            legend.push(dt.records[i][fd.groupby[0]]);
          }

          myOptions = {
            legend: {
              data: legend,
              left: 'left',
              itemWidth: 10,
              itemHeigt: 10
            },
            radar: {
              shape: fd.circle === true ? 'circle' : 'polygon',
              indicator: map_indicator,
              radius: '55%',
            },
            series: [{
              name: '',
              type: 'radar',
              areaStyle: fd.normal === true ? { normal: {} } : null,
              data: map_data,
              tooltip: {
                trigger: 'item',
                axisPointer: {
                  type: 'cross',
                  crossStyle: {
                    color: '#999'
                  }
                },
                formatter: function (obj) {
                  let tip = obj.name + ':<br/>';
                  for (let i = 0; i < obj.value.length; i++) {
                    tip += fd.metrics[i] + ': ' + slice.d3format(obj.seriesName, obj.value[i]) + '<br/>';
                  }
                  return tip;
                },
              }
            }]
          }
          options = $.extend(options, myOptions);
          break;
        case 'echarts_dash_board':
          let dash_color = [];
          const d1 = fd.dash_style.split('+');
          d1.forEach(d => {
            const str = d.substring(1, d.length - 1);
            dash_color.push([parseFloat(str.split(',')[0]), str.split(',')[1].trim()]);
          });
          let value = eval(fd.dash_expr.replace('value', dt.records[0][fd.metric]));
          if (value.toString().indexOf('.') != -1) {
            value = value.toFixed(2);
          }
          options['tooltip'] = {
            formatter: "{b} : {c}%"
          },
            options['series'] = [
              {
                name: '',
                type: 'gauge',
                z: 3,
                min: fd.dash_min,
                max: fd.dash_max,
                splitNumber: parseInt(fd.dash_splitNum),
                radius: '75%',
                axisLine: {
                  lineStyle: {
                    color: dash_color,
                  }
                },
                detail: {
                  textStyle: {       // 其余属性默认使用全局文本样式，详见TEXTSTYLE
                    fontWeight: 'bolder'
                  },
                  formatter: function (value) {
                    return value + fd.dash_suffix;
                  }
                },
                data: [{
                  value: value,
                  name: fd.dash_name === '' ? fd.metric : fd.dash_name
                }]
              }
            ];
          break;

        case 'echarts_bar_waterfall':
          const yAxisValue = [], yAidValue = [];
          let total = 0;
          for (let i = 0; i < fd.metrics.length; i++) {
            dt.records.forEach(d => {
              yAxisValue.push(d[fd.metrics[i]]);
              total += d[fd.metrics[i]];
            });
          }
          yAxisValue.unshift(total);

          for (let i = 0; i < fd.metrics.length; i++) {
            dt.records.forEach(d => {
              total = total - d[fd.metrics[i]];
              yAidValue.push(total);
            });
          }
          yAidValue.unshift(0);

          const seriesValue = [
            {
              name: '辅助',
              type: 'bar',
              stack: '总量',
              itemStyle: {
                normal: {
                  barBorderColor: 'rgba(0,0,0,0)',
                  color: 'rgba(0,0,0,0)'
                }
              },
              data: yAidValue
            },
            {
              name: '',
              type: 'bar',
              stack: '总量',
              label: {
                normal: {
                  show: true,
                  position: 'inside'
                }
              },
              data: yAxisValue
            }
          ];

          const tooltip = {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
              type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            },
            formatter: function (params) {
              let tar = params[1];
              return tar.name + ' : ' + slice.d3format(tar.name, tar.value);
            }
          };
          const y_degree_p = fd.y_degree === '' ? {} : $.parseJSON(fd.y_degree);
          if (fd.enabled_bar_width) {
            myOptions = {
              tooltip: tooltip,
              xAxis: {
                type: 'category',
                splitLine: { show: false },
                data: ['总量'].concat(fd.metrics),
              },
              yAxis: {
                type: 'value',
                name: fd.y_axis_name,
                position: 'left',
                axisLabel: {
                  formatter: function (value) {
                    return formatAxias(value, fd.y_format);
                  }
                },
                min: y_degree_p.min,
                max: y_degree_p.max,
              },
              barWidth: fd.bar_width,
              series: seriesValue,
              label: format_label(true, 'top')
            };
          } else {
            myOptions = {
              tooltip: tooltip,
              xAxis: {
                type: 'category',
                splitLine: { show: false },
                data: ['总量'].concat(fd.metrics),
              },
              yAxis: {
                type: 'value',
                name: fd.y_axis_name,
                position: 'left',
                axisLabel: {
                  formatter: function (value) {
                    return formatAxias(value, fd.y_format);
                  }
                },
                min: y_degree_p.min,
                max: y_degree_p.max,
              },
              series: seriesValue,
              label: format_label(true, 'top')
            };
          }

          options = $.extend(options, myOptions);
          break;

        case 'echarts_big_number':
          let insideLabel = {
            normal: {
              position: 'center',
              formatter: function (params) {
                return slice.d3format(params.name, params.value) + '\n' + params.name;
              },
              textStyle: {
                fontStyle: 'normal',
                fontWeight: 'normal',
                fontSize: fd.fontSize
              }
            }
          };

          myOptions = {
            series: {
              type: 'pie',
              center: ['50%', '50%'],
              radius: ['50%', '60%'],
              label: insideLabel,
              tooltip: {
                trigger: 'item',
                axisPointer: {
                  type: 'cross',
                  crossStyle: {
                    color: '#999'
                  }
                },
                formatter: function (obj) {
                  let tip = obj.name + ': ' + slice.d3format(obj.name, obj.value);
                  return tip;
                },
              },
              data: [{
                name: fd.subheader === '' ? fd.metric : fd.subheader,
                value: dt.data[0][0]
              }]
            }
          }

          options = $.extend(options, myOptions);
          break;

        case 'echarts_big_number_compare':
          var labelTop = {
            normal: {
              label: {
                show: true,
                position: 'center',
                formatter: function (params) {
                  return ((fd.subheader == '' || fd.subheader == null) ? '指标比率' : fd.subheader) + '\n' +
                    (params.data.value2) + '%';
                },
                textStyle: {
                  fontSize: fd.fontSize * 2,
                }
              }
            }
          };

          var labelBottom = {
            normal: {
              label: {
                show: true,
                position: 'center',
                formatter: function (params) {
                  return params.name + ': ' + slice.d3format(params.name, params.value) + '\n' +
                    fd.metrics_two + ': ' + slice.d3format(params.name, dt.records[0][fd.metrics_two]);
                },
                textStyle: {
                  baseline: 'bottom',
                  fontSize: fd.fontSize,
                }
              }
            }
          };

          myOptions = {
            series: [{
              type: 'pie',
              center: ['50%', '50%'],
              radius: ['50%', '60%'],
              tooltip: {
                trigger: 'item',
                axisPointer: {
                  type: 'cross',
                  crossStyle: {
                    color: '#999'
                  }
                },
                formatter: function (obj) {
                  if (obj.name == 'other') {
                    return '';
                  }
                  let tip = obj.name + ': ' + slice.d3format(obj.name, obj.value) + '(' + obj.percent + '%)';
                  return tip;
                },
              },

              data: [{
                name: 'other',
                value: parseFloat(dt.records[0][fd.metrics_two]) - parseFloat(dt.records[0][fd.metrics_one]),
                value2: (parseFloat(dt.records[0][fd.metrics_one]) / parseFloat(dt.records[0][fd.metrics_two]) * 100).toFixed(2),
                itemStyle: labelTop,
              }, {
                name: fd.metrics_one,
                value: parseFloat(dt.records[0][fd.metrics_one]),
                itemStyle: labelBottom
              }]
            }]
          }
          options = $.extend(options, myOptions);
          break;

        case 'echarts_treemap':
          console.info(dt);
          // let _fd = slice.formData;
          let rootId = 0;
          let rootName = '';
          const visibleMin = fd.visible_min;
          const leafDepth = fd.leaf_depth;

          const flatData = [];
          let treeData = [];
          for (let i = 0; i < dt.records.length; i++) {
            // set the valus
            const value = [];
            for (let j = 0; j < fd.metrics.length; j++) {
              // let key = fd.metrics[j];
              let vl = dt.records[i][fd.metrics[j]];
              // values.push({
              //   key : key,
              //   value : value
              // });
              value.push(vl);
            }

            // set the id, pid, name
            const id = dt.records[i][fd.child_id];
            const pid = dt.records[i][fd.parent_id];
            const name = dt.records[i][fd.child_name];

            // get the init root id
            if (pid === null || pid === "0" || pid === 0 ) {
              rootId = dt.records[i][fd.child_id];
              rootName = dt.records[i][fd.child_name];
            }

            flatData.push(
              {
                id: id,
                pid: pid,
                name: name,
                value: value
              }
            )
          }

          // convert the flat json data to tree data.
          if (rootId != null && rootId != '') {
            treeData = getTreeData(flatData, rootId);
            console.info(treeData)
          } else {
            // throw new Error('Root ID is null!');
            // break;
          }

          var formatUtil = echarts.format;
          myOptions = {
            tooltip: {
              formatter: function (info) {
                var values = info.value;
                var treePathInfo = info.treePathInfo;
                var treePath = [];

                for (var i = 1; i < treePathInfo.length; i++) {
                  treePath.push(treePathInfo[i].name);
                }
                var tooltip = '';
                for (let j = 0; j < fd.metrics.length; j++) {
                  // let key = fd.metrics[j];
                  var name = fd.metrics[j];
                  var value = values[j];
                  var amount = isValidNumber(value)
                    ? formatUtil.addCommas(value)
                    : '-';
                  tooltip = tooltip + name + ': ' + amount.toString() + '<br>'
                }

                return [
                  '<div class="tooltip-title">' + formatUtil.encodeHTML(treePath.join('.')) + '</div>',
                  tooltip,
                ].join('');
              }
            },
            title: {
              text: '',
              left: 'center'
            },
            series: [
              {
                name: rootName,
                type: 'treemap',
                visibleMin: visibleMin,
                leafDepth: leafDepth,
                width: '100%',
                height: '90%',
                roam: false,
                label: {
                  show: true,
                  formatter: '{b}'
                },
                upperLabel: {
                  normal: {
                    show: true,
                    position: [10,15],
                    height: 30
                  }
                },
                itemStyle: {
                  normal: {
                    borderColor: '#fff'
                  }
                },
                levels: getLevelOption(),
                data: treeData
              }
            ]
          };
          options = $.extend(options, myOptions);
          break;
        case 'echarts_bubble':
          let groupby = [];
          data = [];
          let maxSize = 0;
          for (let i = 0; i < dt.length; i++) {
            groupby.push(dt[i].key);
            let gData = [];
            for (let j = 0; j < dt[i].values.length; j++) {
              // array[x, y, size, entity, key(series)]
              gData.push([dt[i].values[j][fd['x']], dt[i].values[j][fd['y']], dt[i].values[j][fd['size']], dt[i].values[j][fd['entity']], dt[i].key]);
              maxSize = maxSize < dt[i].values[j][fd['size']] ? dt[i].values[j][fd['size']] : maxSize;
            }
            data[i] = gData;
          }

          for (let k = 0; k < groupby.length; k++) {
            series.push({
              name: groupby[k],
              data: data[k],
              type: 'scatter',
              symbolSize: function (data) {
                return data[2] / maxSize * 50;
              },
              label: {
                emphasis: {
                  show: true,
                  formatter: function (param) {
                    return param.data[3];
                  },
                  position: 'top'
                }
              }
            });
          }

          const min_max_y = fd.y_degree === '' ? {} : $.parseJSON(fd.y_degree);
          const min_max_x = fd.x_degree === '' ? {} : $.parseJSON(fd.x_degree);
          myOptions = {
            toolbox: {
              show: true,
              feature: {
                dataView: { show: true, readOnly: true },
                restore: { show: true },
                saveAsImage: { show: true }
              }
            },
            legend: {
              left: 'left',
              itemWidth: 10,
              itemHeigt: 10,
              data: groupby
            },
            xAxis: {
              name: fd.x_axis_label,
              scale: true,
              axisLabel: {
                formatter: function (value) {
                  return formatAxias(value, fd.x_format);
                }
              },
              min: min_max_x.min,
              max: min_max_x.max,
            },
            yAxis: {
              name: fd.y_axis_label,
              scale: true,
              axisLabel: {
                formatter: function (value) {
                  return formatAxias(value, fd.y_format);
                }
              },
              min: min_max_y.min,
              max: min_max_y.max,
            },
            series: series,
            tooltip: {
              trigger: 'item',
              axisPointer: {
                type: 'cross',
                crossStyle: {
                  color: '#999'
                }
              },
              formatter: function (l) {
                let tip = l.data[3] + '(' + l.data[4] + ')' + '<br/>'
                  + fd['x'] + ': ' + slice.d3format(fd['x'], l.data[0]) + '<br/>'
                  + fd['y'] + ': ' + slice.d3format(fd['y'], l.data[1]) + '<br/>'
                  + fd['size'] + ': ' + slice.d3format(fd['size'], l.data[2]);
                return tip;
              },
            },
          };
          // options = $.extend(options, myOptions);
          options = myOptions;
          break;

        case 'echarts_word_cloud':
          let wordData = [];
          const rotation = [];
          const length = (fd.limit == null || dt.length < fd.limit) ? dt.length : fd.limit;
          for (let i = 0; i < length; i++) {
            wordData.push({
              name: dt[i].text.trim(),
              value: dt[i].size,
            });
          }
          myOptions = {
            tooltip: {
              show: true
            },
            series: [{
              type: 'wordCloud',
              top: '20',
              width: '90%',
              height: '95%',
              sizeRange: [parseInt(fd.size_from), parseInt(fd.size_to)],
              shape: 'circle',
              textPadding: 0,
              autoSize: {
                enable: true,
                minSize: 10
              },
              textStyle: {
                normal: {
                  color: function () {
                    return 'rgb(' + [
                      Math.round(Math.random() * 160),
                      Math.round(Math.random() * 160),
                      Math.round(Math.random() * 160)
                    ].join(',') + ')';
                  }
                },
                emphasis: {
                  shadowBlur: 10,
                  shadowColor: '#333'
                }
              },
              data: wordData,
            }]
          };

          if (fd.rotation === 'flat') {
            myOptions.series[0].rotationRange = [0, 0];
          } else if (fd.rotation === 'square') {
            myOptions.series[0].rotationStep = 90;
          } else {
            myOptions.series[0].rotationRange = [-45, 90];
          }
          options = $.extend(options, myOptions);
          break;

        case 'echarts_quadrant':
          const seris = [];
          const x_metric = fd.x_metric;
          const y_metric = fd.y_metric;
          const min_x = fd.min_x_axis;
          const max_x = fd.max_x_axis;
          const min_y = fd.min_y_axis;
          const max_y = fd.max_y_axis;
          const origin_x = fd.origin_x;
          const origin_y = fd.origin_y;
          const first_module_info = fd.first_module_infor;
          const second_module_info = fd.second_module_infor;
          const third_module_info = fd.third_module_infor;
          const fourth_module_info = fd.fourth_module_infor;
          const legends = [];
          const textStyle = { fontSize: 14, fontStyle: 'normal', fontWeight: 'normal' };
          dt.records.forEach(function (value, index, array) {
            const seriesData = [];
            // fd['metrics'].forEach(function (item, index, array) {
            for (let i = 0; i < fd['x_metric'].concat(fd['y_metric']).length; i++) {
              seriesData.push([value[x_metric], value[y_metric]]);
            };
            let serie = {};

            const markLineData = [];
            if (origin_x !== '') {
              markLineData.push({ xAxis: origin_x });
            }
            if (origin_y !== '') {
              markLineData.push({ yAxis: origin_y });
            }
            serie = {
              name: value[fd['series']],
              type: 'scatter',
              data: seriesData,
              symbolSize: fd.point_size == "" ? 10 : fd.point_size,
              markLine: {
                lineStyle: {
                  normal: {
                    type: 'solid'
                  }
                },
                data: markLineData
              }
            };
            seris.push(serie);
            legends.push(value[fd['series']]);
          });

          myOptions = {
            grid: {
              right: fd.right_padding == null ? '0%' : fd.right_padding,
              left: fd.left_padding == null ? '0%' : fd.left_padding,
              top: fd.top_padding == null ? '0%' : fd.top_padding,
              bottom: fd.bottom_padding == null ? '0%' : fd.bottom_padding,
              containLabel: true,
            },
            title: [
              {
                text: first_module_info,
                x: fd.first_x,
                y: fd.first_y,
                textStyle: textStyle
              },
              {
                text: second_module_info,
                x: fd.second_x,
                y: fd.second_y,
                textStyle: textStyle
              },
              {
                text: third_module_info,
                x: fd.third_x,
                y: fd.third_y,
                textStyle: textStyle
              },
              {
                text: fourth_module_info,
                x: fd.fourth_x,
                y: fd.fourth_y,
                textStyle: textStyle
              },
            ],
            tooltip: {
              trigger: 'item',
              showDelay: 0,
              formatter: function (params) {
                if (params.componentType === 'markLine') {
                  return params.value;
                } else if (params.componentType === 'series')
                  if (params.value.length > 1) {
                    return params.seriesName + ' :<br/>'
                      + params.value[0] + ' '
                      + params.value[1];
                  }
              },
              axisPointer: {
                show: true,
                type: 'cross',
                lineStyle: {
                  type: 'dashed',
                  width: 1
                },
                value: 0
              }
            },
            legend: {
              data: legends,
              left: 'left',
              itemWidth: 10,
              itemHeigt: 10
            },
            xAxis:
            {
              name: x_metric,
              nameLocation: 'middle',
              nameGap: 25,
              axisTick: {
                inside: false,
                length: 5,
                lineStyle: {
                  color: '#00f',
                  shadowColor: '#00f',
                  shadowOffsetY: -5
                },
              },

              splitLine: {
                show: false
              },
              scale: true,
            },
            yAxis:
            {
              name: y_metric,
              splitLine: {
                show: false,
              },
              type: 'value',
              scale: true,
              axisLabel: {
                formatter: '{value} '
              },
            },
            series: seris
          };
          if (min_x) {
            myOptions.xAxis.min = min_x;
          }
          if (max_x) {
            myOptions.xAxis.max = max_x;
          }
          if (min_y) {
            myOptions.yAxis.min = min_y;
          }
          if (max_y) {
            myOptions.yAxis.max = max_y;
          }
          options = $.extend(options, myOptions);
          break;

        case 'echarts_sankey':
          const data_nodes = [];
          const data_links = [];
          const source = [];
          const target = [];
          const nodes = [];
          const node_value = [];
          const lastNodes = [];

          for (let i = 0; i < dt.records.length; i++) {
            let sourceValue = dt.records[i][fd.groupby[0]];
            let targetValue = dt.records[i][fd.groupby[1]];
            source.push(sourceValue);
            target.push(targetValue);
            node_value.push(dt.records[i][fd.metric]);
            if ($.inArray(sourceValue, nodes) == -1) {
              nodes.push(sourceValue);
            }
            if ($.inArray(targetValue, nodes) == -1) {
              nodes.push(targetValue);
            }
            data_links.push(
              {
                source: sourceValue,
                target: targetValue,
                value: dt.records[i][fd.metric],
                source_value: 0,
                target_value: 0,
              }
            )
          }
          for (let i = 0; i < target.length; i++) {
            if ($.inArray(target[i], source) == -1 && $.inArray(target[i], lastNodes) == -1) {
              lastNodes.push(target[i]);
            }
          }
          for (let i = 0; i < nodes.length; i++) {
            if ($.inArray(nodes[i], lastNodes) == -1) {
              let nodeValue = 0;
              for (let j = 0; j < data_links.length; j++) {
                if (nodes[i] == data_links[j].source) {
                  nodeValue = nodeValue + data_links[j].value;
                }
              }
              for (let k = 0; k < data_links.length; k++) {
                if (nodes[i] == data_links[k].source) {
                  data_links[k].source_value = nodeValue;
                }
              }
              for (let k = 0; k < data_links.length; k++) {
                if (nodes[i] == data_links[k].target) {
                  data_links[k].target_value = nodeValue;
                }
              }
              data_nodes.push(
                {
                  name: nodes[i],
                  value: nodeValue,
                }
              )
            } else {
              let nodeValue = 0;
              for (let j = 0; j < data_links.length; j++) {
                if (nodes[i] == data_links[j].target) {
                  nodeValue = nodeValue + data_links[j].value;
                }
              }
              for (let k = 0; k < data_links.length; k++) {
                if (nodes[i] == data_links[k].source) {
                  data_links[k].source_value = nodeValue;
                }
              }
              for (let k = 0; k < data_links.length; k++) {
                if (nodes[i] == data_links[k].target) {
                  data_links[k].target_value = nodeValue;
                }
              }
              data_nodes.push(
                {
                  name: nodes[i],
                  value: nodeValue,
                  label: {
                    normal: {
                      position: 'left',
                    }
                  }
                }
              )
            }
          }
          myOptions = {
            color: ['rgb(255, 90, 95)', 'rgb(140, 224, 113)', 'rgb(255, 26, 177)', 'rgb(255, 180, 0)', 'rgb(187, 237, 171)', 'rgb(0, 255, 235)', 'rgb(123, 0, 81)', 'rgb(180, 167, 108)', 'rgb(0, 161, 179)', 'rgb(255, 51, 57)', 'rgb(152, 139, 78)'],
            toolbox: {
              show: true,
              feature: {
                dataView: { show: true, readOnly: true },
                restore: { show: true },
                saveAsImage: { show: true }
              }
            },
            tooltip: {
              extraCssText: 'position: absolute;width: auto;background: #ddd;padding: 10px;font-size: 12px;font-weight: 200;color: #333;border: 1px solid #fff;text-align: center;pointer-events: none;',
              trigger: 'item',
              triggerOn: 'mousemove',
              textStyle: {
                align: 'left'
              },
              formatter: function (params) {
                if (params.dataType == 'node') {
                  const html = params.data.name + " Value: <span class='emph'>" + formatNumber(params.data.value) + '</span>';
                  return html;
                } else if (params.dataType == 'edge') {
                  const val = formatNumber(params.data.value);
                  const sourcePercent = d3.round((params.data.value / params.data.source_value) * 100, 1);
                  const targetPercent = d3.round((params.data.value / params.data.target_value) * 100, 1);
                  const html = [
                    "<div class=''>Path Value: <span class='emph'>", val, '</span></div>',
                    "<div class='percents'>",
                    "<span class='emph'>",
                    (isFinite(sourcePercent) ? sourcePercent : '100'),
                    '%</span> of ', params.data.source, '<br/>',
                    "<span class='emph'>" +
                    (isFinite(targetPercent) ? targetPercent : '--') +
                    '%</span> of ', params.data.target, 'target',
                    '</div>',
                  ].join('');
                  return html;
                }
              }
            },
            width: '100%',
            height: '99%',
            series: [
              {
                left: 'left',
                top: 'top',
                nodeWidth: 15,
                type: 'sankey',
                layout: 'none',
                data: data_nodes,
                links: data_links,
                itemStyle: {
                  normal: {
                    borderWidth: 1,
                    borderColor: '#aaa'
                  }
                },
                lineStyle: {
                  normal: {
                    color: 'source',
                    curveness: 0.3
                  }
                }
              }
            ]
          };
          options = myOptions;
          break;
        case 'echarts_funnel':
          const so = fd.sort;
          let count = 0;
          let type = [];
          let returnData = [];
          let needOrder = [];
          let needData = [];
          let exchange = [];

          if (fd.order_type.length != 0) {
            //统计总数

            // 判断是否添加顺序
            const order_type = fd.order_type;
            for (let i = 0; i < order_type.length; i++) {
              needOrder.push(order_type[i].value);
            }
            exchange = count;
            //计算并返回数据
            let testEnt = Object.entries(dt.records[0]);
            //0号位是name
            if (fd.groupby_one == testEnt[0][0]) {
              //计算总数
              for (let i = 0; i < dt.records.length; i++) {
                let ent = Object.entries(dt.records[i]);
                count = count + ent[1][1];
              }
              for (let i = 0; i < fd.order_type.length; i++) {
                for (let j = 0; j < dt.records.length; j++) {
                  let ent = Object.entries(dt.records[j]);
                  if (order_type[i].value === ent[0][1]) {
                    let serie = {
                      value: ent[1][1] / count * 100,
                      name: order_type[i].value,
                      count: ent[1][1],
                    };
                    returnData.push(serie);
                  }
                }
              }
            }
            if (fd.groupby_one == testEnt[1][0]) {
              //计算总数
              for (let i = 0; i < dt.records.length; i++) {
                let ent = Object.entries(dt.records[i]);
                count = count + ent[0][1];
              }
              for (let i = 0; i < fd.order_type.length; i++) {
                for (let j = 0; j < dt.records.length; j++) {
                  let ent = Object.entries(dt.records[j]);
                  if (order_type[i].value === ent[1][1]) {
                    let serie = {
                      value: ent[0][1] / count * 100,
                      name: order_type[i].value,
                      count: ent[0][1],
                    };
                    returnData.push(serie);
                  }
                }
              }
            }

            for (let i = 0; i < returnData.length; i++) {
              let num = 0;
              for (let j = i; j < returnData.length; j++) {
                num = num + returnData[j].count;
                returnData[i].count = num;
                returnData[i].value = num / count * 100;
              }
            }
          }
          else {
            if (dt.hasOwnProperty('records')) {

              //判断计算属性
              let testEnt = Object.entries(dt.records[0]);
              //0号位是name
              if (fd.groupby_one == testEnt[0][0]) {
                // 计算总数
                for (let i = 0; i < dt.records.length; i++) {
                  let ent = Object.entries(dt.records[i]);
                  count = count + ent[1][1];
                }
                // 生成数据
                for (let j = 0; j < dt.records.length; j++) {
                  let ent = Object.entries(dt.records[j]);
                  // console.info(ent)
                  let serie = {
                    value: ent[1][1] / count * 100,
                    name: ent[0][1],
                    count: ent[1][1],
                  };
                  returnData.push(serie);
                }
              }
              //1号为是name
              if (fd.groupby_one == testEnt[1][0]) {
                // 生成数据
                // 计算总数
                for (let i = 0; i < dt.records.length; i++) {
                  let ent = Object.entries(dt.records[i]);
                  count = count + ent[0][1];
                }
                for (let j = 0; j < dt.records.length; j++) {
                  let ent = Object.entries(dt.records[j]);
                  // console.info(ent)
                  let serie = {
                    value: ent[0][1] / count * 100,
                    name: ent[1][1],
                    count: ent[0][1],
                  };
                  returnData.push(serie);
                }
              }

              //重算比例
              for (let i = 0; i < returnData.length; i++) {
                let num = 0;
                for (let j = i; j < returnData.length; j++) {
                  num = num + returnData[j].count;
                  returnData[i].count = num;
                  returnData[i].value = num / count * 100;
                }
              }
            }
          }

          myOptions = {
            tooltip: {
              trigger: 'item',
              formatter: "{a} <br/>{b} : {c}%"
            },
            toolbox: {
              feature: {
                dataView: { readOnly: false },
                restore: {},
                saveAsImage: {}
              }
            },
            legend: {
              data: type,
            },
            calculable: true,
            tooltip: {
              extraCssText: 'position: absolute;width: auto;background: #ddd;padding: 10px;font-size: 12px;font-weight: 200;color: #333;border: 1px solid #fff;text-align: center;pointer-events: none;',
              trigger: 'item',
              triggerOn: 'mousemove',
              textStyle: {
                align: 'left'
              },
              formatter: function (params) {
                const html = [
                  "<div class=''>百分比: <span class='emph'>", params.data.value, '%</span></div>',
                  "<div class=''>数目: <span class='emph'>", params.data.count, '</span></div>'
                ].join('');
                return html;

              }
            },
            series: [
              {
                name: '漏斗图',
                type: 'funnel',
                left: '10%',
                top: 60,
                //x2: 80,
                bottom: 60,
                width: '80%',
                // height: {totalHeight} - y - y2,
                min: 0,
                max: 100,
                minSize: '0%',
                maxSize: '100%',
                sort: 'descending',
                gap: 2,
                label: {
                  normal: {
                    show: true,
                    position: 'inside'
                  },
                  emphasis: {
                    textStyle: {
                      fontSize: 20
                    }
                  }
                },
                labelLine: {
                  normal: {
                    length: 10,
                    lineStyle: {
                      width: 1,
                      type: 'solid'
                    }
                  }
                },
                itemStyle: {
                  normal: {
                    borderColor: '#fff',
                    borderWidth: 1
                  }
                },
                data: returnData,
              }
            ]
          };
          options = myOptions;
          break;
        case 'echarts_area_stack':
          // setup the xAxis from fd.groupby
          for (let i = 0; i < fd.groupby.length; i++) {
            const xAxisValue = [];
            dt.records.forEach(d => {
              xAxisValue.push(d[fd.groupby[i]]);
            });
            xAxis[i] = {
              type: 'category',
              data: xAxisValue,
              position: 'bottom',
              offset: 25 * i,
              boundaryGap: false,
              axisPointer: {
                type: 'shadow'
              },
              axisLabel: {
                formatter: function (value) {
                  let result = '';
                  if (value.length > 8) {
                    result = value.substring(0, 8) + "...";
                  } else {
                    result = value;
                  }
                  return result;
                }
              }
            };
          }

          // set diffirent yAxis
          if (fd.y_metrics) {
            // 1.setup the legend from fd.metrics
            legend = fd.y_metrics;

            // 2.setup yAxis
            const y_degree_p = fd.y_degree === '' ? {} : $.parseJSON(fd.y_degree);
            yAxis.push({
              type: 'value',
              name: fd.y_axis_name,
              position: 'left',
              axisLabel: {
                formatter: function (value) {
                  return formatAxias(value, fd.y_format);
                }
              },
              min: y_degree_p.min,
              max: y_degree_p.max,
            })

            // 3.setup the series from the fd.metrics and dt.records
            for (let i = 0; i < fd.y_metrics.length; i++) {
              const yAxisValue = [];
              dt.records.forEach(d => {
                yAxisValue.push(d[fd.y_metrics[i]]);
              });
              if (fd.is_bar_value) {
                if (fd.normal) {
                  series.push(
                    {
                      name: fd.y_metrics[i],
                      type: 'line',
                      stack: '总量',
                      label: {
                        normal: {
                          show: true,
                          position: 'top',
                          textStyle: {
                            color: fd.lable_color,
                          },
                          formatter: function (params) {
                            return formatNumber(params.value);
                          }
                        }
                      },
                      areaStyle: { normal: {} },
                      data: yAxisValue,
                    }
                  );
                } else {
                  series.push(
                    {
                      name: fd.y_metrics[i],
                      type: 'line',
                      stack: '总量',
                      label: {
                        normal: {
                          show: true,
                          position: 'top',
                          textStyle: {
                            color: fd.lable_color,
                          },
                          formatter: function (params) {
                            return formatNumber(params.value);
                          }
                        }
                      },
                      areaStyle: '',
                      data: yAxisValue,
                    }
                  );
                }
              } else {
                if (fd.normal) {
                  series.push(
                    {
                      name: fd.y_metrics[i],
                      type: 'line',
                      stack: '总量',
                      areaStyle: { normal: {} },
                      data: yAxisValue,
                    }
                  );
                } else {
                  series.push(
                    {
                      name: fd.y_metrics[i],
                      type: 'line',
                      stack: '总量',
                      areaStyle: '',
                      data: yAxisValue,
                    }
                  );
                }
              }
            }
          }

          myOptions = {
            tooltip: {
              trigger: 'axis',
              axisPointer: {
                type: 'cross',
                label: {
                  backgroundColor: '#6a7985'
                }
              },
              formatter: function (params) {
                let totalNum = 0;
                for (let i = 0; i < params.length; i++) {
                  totalNum = totalNum + params[i].value;
                }
                let html = [
                  "<div class=''><span class='emph'>", params[0].name, '</span></div>',
                  "<div class=''>总量:<span class='emph'>", formatNumber(totalNum), '</span></div>',
                ].join('');
                for (let i = 0; i < params.length; i++) {
                  html = html + "<div class=''>" + params[i].seriesName + ":<span class='emph'>" + formatNumber(params[i].value) + '</span></div>';
                }
                return html;
              }
            },
            legend: {
              data: legend,
              left: 'left',
              itemWidth: 10,
              itemHeigt: 10
            },
            xAxis: xAxis,
            yAxis: yAxis,
            series: series
          };
          options = $.extend(options, myOptions);
          break;

        default:
          throw new Error('Unrecognized visualization for echarts' + fd.viz_type);
      }
      slice.container.css('height', height + 'px');
      chart.setOption(options);
      return chart;
    }
    const graph = drawGraph();
  };

  render();
}

module.exports = echartsVis;