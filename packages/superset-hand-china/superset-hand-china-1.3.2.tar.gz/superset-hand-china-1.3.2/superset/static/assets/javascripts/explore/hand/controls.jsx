import React from 'react';
import { formatSelectOptionsForRange, formatSelectOptions } from '../../modules/utils';
import { t } from '../../locales';
import MetricOption from '../../components/MetricOption';
import ColumnOption from '../../components/ColumnOption';
import * as v from '../validators'

const ROW_COL_NUM = [1, 2, 3, 4, 5];
const LABEL_POSITION = ['outside', 'inside', 'center'];
const STANDARD_POINT = [1, 2, 3, 4, 5, 6, 7];
let timeStamp = new Date().getTime();
let nowDate =new Date(timeStamp).getFullYear() + '-' + (new Date(timeStamp).getMonth()+1) + '-' + new Date(timeStamp).getDate();

export const controls = {
  // ag_grid
  hide_options: {
    type: 'CheckboxControl',
    label: t('Hide Options'),
    renderTrigger: true,
    default: false,
    description: t('hide options'),
  },
  show_modal: {
    type: 'ButtonControl',
    label: t('Table Style'),
    description: t('table style'),
  },
  header_style: {
    type: 'TextControl',
    label: t('Header Style'),
    default: '',
    description: t('table header style'),
  },
  table_style: {
    type: 'TextControl',
    label: t('Table Style'),
    default: '',
    description: t('table style'),
  },
  col_style: {
    type: 'ColStyleControl',
    label: '',
    default: [],
    description: '',
    mapStateToProps: state => ({
      datasource: state.datasource,
    }),
  },
  condition_style: {
    type: 'ConditionStyleControl',
    label: '',
    default: [],
    description: '',
    mapStateToProps: state => ({
      datasource: state.datasource,
    }),
  },
  compare_style: {
    type: 'CompareStyleControl',
    label: '',
    default: [],
    description: '',
    mapStateToProps: state => ({
      datasource: state.datasource,
    }),
  },
  navigator: {
    type: 'NavigatorControl',
    label: '',
    default: [],
    description: '',
    mapStateToProps: state => ({
      datasource: state.datasource,
    }),
  },
  theme: {
    type: 'SelectControl',
    label: t('Theme'),
    choices: formatSelectOptions(['blue', 'fresh', 'bootstrap', 'dark']),
    default: 'blue',
    description: t('ag grid theme'),
  },
  pageSize: {
    type: 'SelectControl',
    label: t('Page Size'),
    choices: formatSelectOptions(['15', '30', '50', '100', 'all']),
    default: '30',
    description: t('ag grid page size'),
  },
  frozen_left: {
    type: 'SelectControl',
    multi: true,
    label: t('Frozen Left'),
    default: null,
    mapStateToProps: state => ({
      choices: (state.datasource) ? state.datasource.metrics_combo.concat(state.datasource.all_cols) : [],
    }),
    description: t('frozen left'),
  },
  frozen_right: {
    type: 'SelectControl',
    multi: true,
    label: t('Frozen Right'),
    default: null,
    mapStateToProps: state => ({
      choices: (state.datasource) ? state.datasource.metrics_combo.concat(state.datasource.all_cols) : [],
    }),
    description: t('frozen right'),
  },
  link_cols: {
    type: 'SelectControl',
    multi: true,
    label: t('Link Cols'),
    default: null,
    mapStateToProps: state => ({
      choices: (state.datasource) ? state.datasource.metrics_combo.concat(state.datasource.all_cols) : [],
    }),
    description: t('link cols'),
  },
  is_pivot: {
    type: 'SelectControl',
    label: t('Is Pivot'),
    choices: formatSelectOptions(['false', 'true']),
    default: 'false',
    description: t('is pivot'),
  },
  hide_cols: {
    type: 'SelectControl',
    multi: true,
    label: t('Hide Cols'),
    default: null,
    mapStateToProps: state => ({
      choices: (state.datasource) ? state.datasource.metrics_combo.concat(state.datasource.all_cols) : [],
    }),
    description: t('hide cols'),
  },
  parent_node: {
    type: 'ParentNodeControl',
    label: '',
    default: [],
    description: t('parent node'),
    mapStateToProps: state => ({
      datasource: state.datasource,
    }),
  },
  pivot_groupby: {
    type: 'SelectControl',
    multi: true,
    label: t('Group By'),
    default: [],
    description: t('One or many controls to group by'),
    optionRenderer: c => <ColumnOption column={c} />,
    valueRenderer: c => <ColumnOption column={c} />,
    valueKey: 'column_name',
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.columns : [],
    }),
  },
  pivot_metrics: {
    type: 'SelectControl',
    multi: true,
    label: t('Metrics'),
    validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: t('One or many metrics to display'),
  },

  // filter_box
  filterSetting: {
    type: 'FilterSettingControl',
    label: '',
    default: [],
    description: '',
    mapStateToProps: state => ({
      datasource: state.datasource,
    }),
  },
  defaultValueSetting: {
    type: 'DefaultValueControl',
    label: '',
    default: [],
    description: '',
    mapStateToProps: state => ({
      datasource: state.datasource,
    }),
  },
  dateValueSetting: {
    type: 'DateValueControl',
    label: '',
    default: [],
    description: '',
    mapStateToProps: state => ({
      datasource: state.datasource,
    }),
  },

  // filter_box_tree
  filter_name: {
    type: 'TextControl',
    label: t('Filter Name'),
    default: '',
    description: t('filter name, read by key-value, like: deptName-deptId'),
  },
  width: {
    type: 'TextControl',
    label: t('Width'),
    default: '100%',
    description: t('filter box\'s width'),
  },
  multi: {
    type: 'CheckboxControl',
    label: t('Is Multi'),
    renderTrigger: true,
    default: true,
    description: t('is  multi'),
  },
  defaultValueFilterTreeSetting: {
    type: 'DefaultValueFilterTreeControl',
    label: '',
    default: [],
    description: '',
    mapStateToProps: state => ({
      datasource: state.datasource,
    }),
  },

  // filter_box_combination
  filter_combination: {
    type: 'FilterCombinationControl',
    label: t('Filter Combination'),
    default: [],
    description: t('filter box combination'),
  },

  // filter_box_cascade
  cascade: {
    type: 'CascadeControl',
    label: '',
    default: [],
    description: '',
    mapStateToProps: state => ({
      datasource: state.datasource,
    }),
  },

  // echarts_bar
  only_left: {
    type: 'CheckboxControl',
    label: t('Only Left'),
    renderTrigger: true,
    default: true,
    description: t('only use left Y'),
  },
  y_metrics: {
    type: 'SelectControl',
    multi: true,
    label: t('Y Axis Metrics'),
    validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: t('One or many lines to display'),
  },
  y_format: {
    type: 'TextControl',
    label: t('Y Axis Format'),
    default: '',
    description: t('Y axis format. e.g.:{value}'),
  },
  y_degree: {
    type: 'TextControl',
    label: t('Y Axis Degree'),
    default: '',
    description: t('y degree, like: {"min": 0, "max": 100}'),
  },
  y_axis_name: {
    type: 'TextControl',
    label: t('Y Axis Name'),
    default: '',
    description: t('Y Axis Name'),
  },
  y_left_metrics: {
    type: 'SelectControl',
    multi: true,
    label: t('Y Left Metrics'),
    // validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: t('One or many metrics to display'),
  },
  y_right_metrics: {
    type: 'SelectControl',
    multi: true,
    label: t('Y Right Metrics'),
    // validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: t('One or many metrics to display'),
  },
  y_left_format: {
    type: 'TextControl',
    label: t('Y Left Format'),
    default: '',
    description: t('Y left format. e.g.:{value}'),
  },
  y_right_format: {
    type: 'TextControl',
    label: t('Y Right Format'),
    default: '',
    description: t('Y right format. e.g.:{value}'),
  },
  y_left_degree: {
    type: 'TextControl',
    label: t('Y Left Degree'),
    default: '',
    description: t('y left degree, like: {"min": 0, "max": 100}'),
  },
  y_right_degree: {
    type: 'TextControl',
    label: t('Y Right Degree'),
    default: '',
    description: t('y right degree, like: {"min": 0, "max": 100}'),
  },
  top_padding: {
    type: 'TextControl',
    label: t('Top Padding'),
    default: '80',
    description: t('top padding'),
  },
  bottom_padding: {
    type: 'TextControl',
    label: t('Bottom Padding'),
    default: '20',
    description: t('bottom padding'),
  },
  left_padding: {
    type: 'TextControl',
    label: t('Left Padding'),
    default: '20',
    description: t('left padding'),
  },
  right_padding: {
    type: 'TextControl',
    label: t('Right Padding'),
    default: '20',
    description: t('right padding'),
  },

  is_avg: {
    type: 'CheckboxControl',
    label: t('Is Avg'),
    renderTrigger: true,
    default: false,
    description: t('is avg'),
  },
  is_max_min: {
    type: 'CheckboxControl',
    label: t('Is Max Min'),
    renderTrigger: true,
    default: false,
    description: t('is max min'),
  },
  is_bar_value: {
    type: 'CheckboxControl',
    label: t('Is Value'),
    renderTrigger: true,
    default: false,
    description: t('is value'),
  },
  stacks: {
    type: 'StackControl',
    label: '',
    default: [],
    description: '',
    mapStateToProps: state => ({
      datasource: state.datasource,
    }),
  },
  bar_width: {
    type: 'TextControl',
    label: t('Bar Width'),
    default: '70%',
    description: t('bar width example:70%'),
  },
  enabled_bar_width: {
    type: 'CheckboxControl',
    label: t('Enabled Bar Width'),
    renderTrigger: true,
    default: false,
    description: t('enabled bar width'),
  },


  // echart_bar_h
  only_bottom: {
    type: 'CheckboxControl',
    label: t('Only Bottom'),
    renderTrigger: true,
    default: true,
    description: t('only use bottom X'),
  },
  x_metrics: {
    type: 'SelectControl',
    multi: true,
    label: t('Metrics'),
    validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: t('One or many metrics to display'),
  },
  x_format: {
    type: 'TextControl',
    label: t('X Format'),
    default: '',
    description: t('X format. e.g.:{value}'),
  },
  x_degree: {
    type: 'TextControl',
    label: t('X Degree'),
    default: '',
    description: t('X degree. e.g.:{"min":0,"max":100}'),
  },
  x_axis_name: {
    type: 'TextControl',
    label: t('X Axis Name'),
    default: '',
    description: t('x axis name'),
  },
  x_bottom_metrics: {
    type: 'SelectControl',
    multi: true,
    label: t('X Bottom Metrics'),
    validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: t('One or many metrics to display'),
  },
  x_top_metrics: {
    type: 'SelectControl',
    multi: true,
    label: t('X Top Metrics'),
    validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: t('One or many metrics to display'),
  },
  x_bottom_format: {
    type: 'TextControl',
    label: t('X Bottom Format'),
    default: '',
    description: t('x bottom format. e.g.:{value};{value}'),
  },
  x_top_format: {
    type: 'TextControl',
    label: t('X Top Format'),
    default: '',
    description: t('x top format. e.g.:{value}'),
  },
  x_bottom_degree: {
    type: 'TextControl',
    label: t('X Bottom Degree'),
    default: '',
    description: t('x bottom degree. e.g.:{"min":0,"max":100}'),
  },
  x_top_degree: {
    type: 'TextControl',
    label: t('X Top Degree'),
    default: '',
    description: t('x top degree. e.g.:{"min":0,"max":100}'),
  },

  // add new by lijf
  subheader: {
    type: 'TextControl',
    label: t('Subheader'),
    default: '',
  },
  label_position: {
    type: 'SelectControl',
    freeForm: true,
    label: t('Label Position'),
    default: null,
    choices: formatSelectOptions(['inside', 'outside']),
  },
  circle_type: {
    type: 'SelectControl',
    freeForm: true,
    renderTrigger: true,
    label: t('Circle Type'),
    choices: formatSelectOptions(['none', 'big', 'medium', 'small']),
    default: 'none',
  },
  circle: {
    type: 'CheckboxControl',
    renderTrigger: true,
    label: t('Circle'),
    default: true,
  },
  normal: {
    type: 'CheckboxControl',
    renderTrigger: true,
    label: t('Full'),
    default: true,
  },
  rose_type: {
    type: 'SelectControl',
    freeForm: true,
    renderTrigger: true,
    label: t('Rose Type'),
    default: null,
    choices: formatSelectOptions(['radius', 'area']),
  },
  label_format: {
    type: 'TextControl',
    label: t('Label Format'),
    default: '{b}  : {c} ({d}%)',
  },
  metrics_one: {
    type: 'SelectControl',
    label: t('Metrics1'),
    clearable: false,
    description: t('Choose the metric'),
    validators: [v.nonEmpty],
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? c.options[0].metric_name : null,
    valueKey: 'metric_name',
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
  },
  metrics_two: {
    type: 'SelectControl',
    label: t('Metrics2'),
    clearable: false,
    description: t('Choose the metric'),
    validators: [v.nonEmpty],
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? c.options[0].metric_name : null,
    valueKey: 'metric_name',
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
  },
  parent_id: {
    type: 'SelectControl',
    label: t('Parent Id'),
    default: '',
    description: t('One or many controls to group by'),
    optionRenderer: c => <ColumnOption column={c} />,
    valueRenderer: c => <ColumnOption column={c} />,
    valueKey: 'column_name',
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.columns : [],
    }),
  },

  //echarts_line_bar
  line_choice: {
    type: 'SelectControl',
    multi: true,
    label: t('Line Metrics'),
    validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: t('line metrics,other are bar metrics'),
  },
  y_left_splitLine: {
    type: 'CheckboxControl',
    label: t('Y Left SplitLine'),
    renderTrigger: true,
    default: true,
    description: t('onle show left splitLine'),
  },
  y_right_splitLine: {
    type: 'CheckboxControl',
    label: t('Y Right SplitLine'),
    renderTrigger: true,
    default: false,
    description: t('onle show right splitLine'),
  },

  //echarts_pie_h
  inner_metrics: {
    type: 'SelectControl',
    multi: true,
    label: t('Inner Metrics'),
    validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: t('One or many metrics to display'),
  },
  inner_label_position: {
    type: 'SelectControl',
    freeForm: true,
    label: t('Inner Label Position'),
    choices: formatSelectOptions(LABEL_POSITION),
    default: 'inside',
  },
  inner_label_format: {
    type: 'TextControl',
    label: t('Label Format'),
    default: '{b}  : {c} ({d}%)',
    description: t('example:{b}  : {c} ({d}%)'),
  },
  inner_lable_color: {
    type: 'TextControl',
    label: t('Inner Lable Color'),
    default: '#fff',
    description: t('inner lable color example: #fff'),
  },
  outer_metrics: {
    type: 'SelectControl',
    multi: true,
    label: t('Outer Metrics'),
    validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: t('One or many metrics to display'),
  },
  outer_label_position: {
    type: 'SelectControl',
    freeForm: true,
    label: t('Outer Label Position'),
    choices: formatSelectOptions(LABEL_POSITION),
    default: 'outside',
  },
  outer_label_format: {
    type: 'TextControl',
    label: t('Label Format'),
    default: '{b}  : {c} ({d}%)',
    description: t('example:{b}  : {c} ({d}%)'),
  },

  //echarts_pie_h_g
  col_num: {
    type: 'SelectControl',
    freeForm: true,
    label: t('Col Num'),
    choices: formatSelectOptions(ROW_COL_NUM),
    default: 1,
  },
  inner_metrics_one: {
    type: 'SelectControl',
    multi: false,
    label: t('Inner Circle Metrics'),
    default: [],
    description: t('Inner Circle Metrics'),
    optionRenderer: c => <ColumnOption column={c} />,
    valueRenderer: c => <ColumnOption column={c} />,
    valueKey: 'column_name',
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.columns : [],
    }),
  },  
  child_id: {
    type: 'SelectControl',

    label: t('Child Id'),
    default: '',
    description: t('One or many controls to group by'),
    optionRenderer: c => <ColumnOption column={c} />,
    valueRenderer: c => <ColumnOption column={c} />,
    valueKey: 'column_name',
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.columns : [],
    }),
  },
  outer_metrics_one: {
    type: 'SelectControl',
    multi: false,
    label: t('Outer Circle Metrics'),
    default: [],
    description: t('Outer Circle Metrics'),
    optionRenderer: c => <ColumnOption column={c} />,
    valueRenderer: c => <ColumnOption column={c} />,
    valueKey: 'column_name',
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.columns : [],
    }),
  },
  child_name: {
    type: 'SelectControl',
    label: t('Child Name'),
    default: '',
    description: t('One or many controls to group by'),
    optionRenderer: c => <ColumnOption column={c} />,
    valueRenderer: c => <ColumnOption column={c} />,
    valueKey: 'column_name',
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.columns : [],
    }),
  },
  visible_min: {
    type: 'TextControl',
    label: t('Visible Min'),
    default: '1000',
  },
  leaf_depth: {
    type: 'SelectControl',
    freeForm: true,
    label: t('Leaf Depth'),
    default: '1',
    choices: formatSelectOptions(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']),
  },

  //echarts_dash_board
  dash_min: {
    type: 'TextControl',
    label: t('Dash Min'),
    default: '0',
    description: t('dash min'),
  },
  dash_max: {
    type: 'TextControl',
    label: t('Dash Max'),
    default: '100',
    description: t('dash max'),
  },
  dash_name: {
    type: 'TextControl',
    label: t('Dash Name'),
    default: 'completion rate',
    description: t('dash name'),
  },
  dash_splitNum: {
    type: 'TextControl',
    label: t('Dash SplitNum'),
    default: '10',
    description: t('dash splitNum'),
  },
  dash_expr: {
    type: 'TextControl',
    label: t('Dash Expr'),
    default: 'value',
    description: t('dash expr'),
  },
  dash_suffix: {
    type: 'TextControl',
    label: t('Dash Suffix'),
    default: '%',
    description: t('dash suffix'),
  },
  dash_style: {
    type: 'TextControl',
    label: t('Dash Style'),
    default: '[0.2, #91c7ae]+[0.8, #63869e]+[1, #c23531]',
    description: t('dash style'),
  },

  //echarts_big_number
  fontSize: {
    type: 'TextControl',
    label: t('FontSize'),
    default: '15',
    description: t('fontSize'),
  },

  //echarts_quadrant
  x_metric: {
    type: 'SelectControl',
    label: t('X Axis Metrics'),
    clearable: false,
    description: t('X axis metrics'),
    validators: [v.nonEmpty],
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? c.options[0].metric_name : null,
    valueKey: 'metric_name',
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
  },
  y_metric: {
    type: 'SelectControl',
    label: t('Y Axis Metrics'),
    clearable: false,
    description: t('Y axis metrics'),
    validators: [v.nonEmpty],
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? c.options[0].metric_name : null,
    valueKey: 'metric_name',
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
  },
  origin_x: {
    type: 'TextControl',
    label: t('Focus X Axis'),
    default: '',
    description: t('Focus X Axis'),
  },
  origin_y: {
    type: 'TextControl',
    label: t('Focus Y Axis'),
    default: '',
    description: t('Focus Y Axis'),
  },
  min_x_axis: {
    type: 'TextControl',
    label: t('Min X Axis'),
    default: '',
    description: t('Min X Axis'),
  },
  max_x_axis: {
    type: 'TextControl',
    label: t('Max X Axis'),
    default: '',
    description: t('Max X Axis'),
  },
  min_y_axis: {
    type: 'TextControl',
    label: t('Min Y Axis'),
    default: '',
    description: t('Min Y Axis'),
  },
  max_y_axis: {
    type: 'TextControl',
    label: t('Max Y Axis'),
    default: '',
    description: t('Max Y Axis'),
  },
  first_module_infor: {
    type: 'TextControl',
    label: t('First Module Information'),
    default: '',
    description: t('First Module Information'),
  },
  first_x: {
    type: 'TextControl',
    label: t('First X'),
    default: '80%',
    description: t('example: 80%'),
  },
  first_y: {
    type: 'TextControl',
    label: t('First Y'),
    default: '5%',
    description: t('example: 5%'),
  },
  second_module_infor: {
    type: 'TextControl',
    label: t('Second Module Information'),
    default: '',
    description: t('Second Module Information'),
  },
  second_x: {
    type: 'TextControl',
    label: t('Second X'),
    default: '12%',
    description: t('example: 12%'),
  },
  second_y: {
    type: 'TextControl',
    label: t('Second Y'),
    default: '5%',
    description: t('example: 5%'),
  },
  third_module_infor: {
    type: 'TextControl',
    label: t('Third Module Information'),
    default: '',
    description: t('Third Module Information'),
  },
  third_x: {
    type: 'TextControl',
    label: t('Third X'),
    default: '12%',
    description: t('example: 12%'),
  },
  third_y: {
    type: 'TextControl',
    label: t('Third Y'),
    default: '75%',
    description: t('example: 75%'),
  },
  fourth_module_infor: {
    type: 'TextControl',
    label: t('Fourth Module Information'),
    default: '',
    description: t('Fourth Module Information'),
  },
  fourth_x: {
    type: 'TextControl',
    label: t('Fourth X'),
    default: '80%',
    description: t('example: 80%'),
  },
  fourth_y: {
    type: 'TextControl',
    label: t('Fourth Y'),
    default: '75%',
    description: t('example: 75%'),
  },
  point_size:{
    type: 'TextControl',
    label: t('Point Size'),
    default: '10',
    description: t('point size'),
  },

  //china map
  groupby_one: {
    type: 'SelectControl',
    multi: false,
    label: t('Group by'),
    default: [],
    description: t('One or many controls to group by'),
    optionRenderer: c => <ColumnOption column={c} />,
    valueRenderer: c => <ColumnOption column={c} />,
    valueKey: 'column_name',
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.columns.filter(c => c.groupby) : [],
    }),
  },
  min_legend: {
    type: 'TextControl',
    label: t('Legend Minimum'),
    default: '',
    description: t('Enter the minimum value of the histogram'),
  },
  max_legend: {
    type: 'TextControl',
    label: t('Legend Maximum'),
    default: '',
    description: t('Enter the maximum value of the histogram'),
  },
  //china city map
  standard_point: {
    type: 'SelectControl',
    freeForm: true,
    label: t('Standard Point'),
    choices: formatSelectOptions(STANDARD_POINT),
    default: 4,
  },
  //big number
  head_color: {
    type: 'TextControl',
    label: t('Head_Color'),
    default: '#4490ca',
    description: t('head color example: #4490ca'),
  },
  body_color: {
    type: 'TextControl',
    label: t('Body Color'),
    default: '#4c9eda',
    description: t('body color example: #4490ca'),
  },
  icone_select: {
    type: 'IconControl',
    label: t('Icone Select'),
    renderTrigger: true,
    default: 'fa-comments',
    description: t('select icone'),
  },
  format: {
    type: 'TextControl',
    label: t('Format'),
    default: '',
    description: t('format, e.g: {b} : {c} ({d}%)'),
  },
  titleSize: {
    type: 'TextControl',
    label: t('Title Size'),
    default: '15',
    description: t('titleSize'),
  },

  // echats_funnel
  order_type: {
    showHeader: true,
    label: t('flow'),
    description: t('Required process'),
    type: 'OrderSelectControl',
    multi: true,
    default: [],
    mapStateToProps: state => ({
      datasource: state.datasource,
    }),
  },
  //echarts area stack
  lable_color: {
    type: 'TextControl',
    label: t('Lable Color'),
    default: '#96CDCD',
    description: t('lable color example: #96CDCD'),
  },
  //big number two
  fontColor: {
    type: 'TextControl',
    label: t('Font Color'),
    default: '#2ab4c0',
    description: t('fontColor example: #2ab4c0'),
  },
  number_description: {
    type: 'TextControl',
    label: t('Number Description'),
    default: '',
  },
  progress_description: {
    type: 'TextControl',
    label: t('Progress Description'),
    default: '',
  },
  big_number_fontSize: {
    type: 'TextControl',
    label: t('Font Size'),
    default: '30',
    description: t('fontSize'),
  },
  //big number tree
  icon_color: {
    type: 'TextControl',
    label: t('Icon Color'),
    default: '#2ab4c0',
    description: t('Icon_Color example: #2ab4c0'),
  },

  // since: {
  //   type: 'DatePickerControl',
  //   label: 'since',
  //   date: '1900-01-01',
  //   description:'Timestamp from filter. This supports free form typing and ' +
  //   'natural language as in `1 day ago`, `28 days` or `3 years`',
  // },
  // until: {
  //   type: 'DatePickerControl',
  //   label: 'until',
  //   date:nowDate
  // },

}
