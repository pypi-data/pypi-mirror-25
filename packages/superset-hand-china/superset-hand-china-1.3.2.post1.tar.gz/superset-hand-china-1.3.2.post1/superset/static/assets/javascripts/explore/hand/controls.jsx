import React from 'react';
import { formatSelectOptionsForRange, formatSelectOptions } from '../../modules/utils';
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
    label: 'hide_options',
    renderTrigger: true,
    default: false,
    description: 'hide_options',
  },
  show_modal: {
    type: 'ButtonControl',
    label: 'table_style',
    description: 'table_style',
  },
  header_style: {
    type: 'TextControl',
    label: 'Header Style',
    default: '',
    description: 'table header style',
  },
  table_style: {
    type: 'TextControl',
    label: 'Table Style',
    default: '',
    description: 'table style',
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
    label: 'Theme',
    choices: formatSelectOptions(['blue', 'fresh', 'bootstrap', 'dark']),
    default: 'blue',
    description: 'ag grid theme',
  },
  pageSize: {
    type: 'SelectControl',
    label: 'Page_Size',
    choices: formatSelectOptions(['15', '30', '50', '100', 'all']),
    default: '30',
    description: 'ag grid page size',
  },
  frozen_left: {
    type: 'SelectControl',
    multi: true,
    label: 'Frozen_Left',
    default: null,
    mapStateToProps: state => ({
      choices: (state.datasource) ? state.datasource.metrics_combo.concat(state.datasource.all_cols) : [],
    }),
    description: 'frozen left',
  },
  frozen_right: {
    type: 'SelectControl',
    multi: true,
    label: 'Frozen_Right',
    default: null,
    mapStateToProps: state => ({
      choices: (state.datasource) ? state.datasource.metrics_combo.concat(state.datasource.all_cols) : [],
    }),
    description: 'frozen right',
  },
  link_cols: {
    type: 'SelectControl',
    multi: true,
    label: 'Link_Cols',
    default: null,
    mapStateToProps: state => ({
      choices: (state.datasource) ? state.datasource.metrics_combo.concat(state.datasource.all_cols) : [],
    }),
    description: 'link cols',
  },
  is_pivot: {
    type: 'SelectControl',
    label: 'Is_Pivot',
    choices: formatSelectOptions(['false', 'true']),
    default: 'false',
    description: 'is pivot',
  },
  hide_cols: {
    type: 'SelectControl',
    multi: true,
    label: 'Hide_Cols',
    default: null,
    mapStateToProps: state => ({
      choices: (state.datasource) ? state.datasource.metrics_combo.concat(state.datasource.all_cols) : [],
    }),
    description: 'hide cols',
  },
  parent_node: {
    type: 'ParentNodeControl',
    label: '',
    default: [],
    description: 'parent node',
    mapStateToProps: state => ({
      datasource: state.datasource,
    }),
  },
  pivot_groupby: {
    type: 'SelectControl',
    multi: true,
    label: 'Group_By',
    default: [],
    description: 'One or many controls to group by',
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
    label: 'Metrics',
    validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: 'One or many metrics to display',
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
    label: 'Filter_Name',
    default: '',
    description: 'filter name, read by key-value, like: deptName-deptId',
  },
  width: {
    type: 'TextControl',
    label: 'Width',
    default: '100%',
    description: "filter box's width",
  },
  multi: {
    type: 'CheckboxControl',
    label: 'is_multi',
    renderTrigger: true,
    default: true,
    description: 'is  multi',
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
    label: 'Filter Combination',
    default: [],
    description: 'filter box combination',
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
    label: 'Only_Left',
    renderTrigger: true,
    default: true,
    description: 'only use left Y',
  },
  y_metrics: {
    type: 'SelectControl',
    multi: true,
    label: 'Y_Axis_Metrics',
    validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: 'One or many lines to display',
  },
  y_format: {
    type: 'TextControl',
    label: 'Y_Axis_Format',
    default: '',
    description: 'y_format, like: {value/100} hundred',
  },
  y_degree: {
    type: 'TextControl',
    label: 'Y_Axis_Degree',
    default: '',
    description: 'y_degree, like: {"min": 0, "max": 100}',
  },
  y_axis_name: {
    type: 'TextControl',
    label: 'Y_Axis_Name',
    default: '',
    description: 'Y Axis Name',
  },
  y_left_metrics: {
    type: 'SelectControl',
    multi: true,
    label: 'Y_Left_Metrics',
    // validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: 'One or many metrics to display',
  },
  y_right_metrics: {
    type: 'SelectControl',
    multi: true,
    label: 'Y_Right_Metrics',
    // validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: 'One or many metrics to display',
  },
  y_left_format: {
    type: 'TextControl',
    label: 'Y_Left_Format',
    default: '',
    description: 'y_left_format, like: {value/100} hundred',
  },
  y_right_format: {
    type: 'TextControl',
    label: 'Y_Right_Format',
    default: '',
    description: 'y_right_format, like: {value/100} hundred',
  },
  y_left_degree: {
    type: 'TextControl',
    label: 'Y_Left_Degree',
    default: '',
    description: 'y_left_degree, like: {"min": 0, "max": 100}',
  },
  y_right_degree: {
    type: 'TextControl',
    label: 'Y_Right_Degree',
    default: '',
    description: 'y_right_degree, like: {"min": 0, "max": 100}',
  },
  top_padding: {
    type: 'TextControl',
    label: 'Top_Padding',
    default: '80',
    description: 'top padding',
  },
  bottom_padding: {
    type: 'TextControl',
    label: 'Bottom_Padding',
    default: '20',
    description: 'bottom padding',
  },
  left_padding: {
    type: 'TextControl',
    label: 'Left_Padding',
    default: '20',
    description: 'left padding',
  },
  right_padding: {
    type: 'TextControl',
    label: 'Right_Padding',
    default: '20',
    description: 'right padding',
  },

  is_avg: {
    type: 'CheckboxControl',
    label: 'Is_Avg',
    renderTrigger: true,
    default: false,
    description: 'is avg',
  },
  is_max_min: {
    type: 'CheckboxControl',
    label: 'Is_Max_Min',
    renderTrigger: true,
    default: false,
    description: 'is max min',
  },
  is_bar_value: {
    type: 'CheckboxControl',
    label: 'Is_Value',
    renderTrigger: true,
    default: false,
    description: 'is value',
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
    label: 'Bar_Width',
    default: '70%',
    description: "bar width example:70%",
  },
  enabled_bar_width: {
    type: 'CheckboxControl',
    label: 'Enabled_Bar_Width',
    renderTrigger: true,
    default: false,
    description: 'enabled bar width',
  },


  // echart_bar_h
  only_bottom: {
    type: 'CheckboxControl',
    label: 'Only_Bottom',
    renderTrigger: true,
    default: true,
    description: 'only use bottom X',
  },
  x_metrics: {
    type: 'SelectControl',
    multi: true,
    label: 'Metrics',
    validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: 'One or many metrics to display',
  },
  x_format: {
    type: 'TextControl',
    label: 'X_Format',
    default: '',
    description: 'x_format, like: {value/100} hundred',
  },
  x_degree: {
    type: 'TextControl',
    label: 'X_Degree',
    default: '',
    description: 'x_degree, like: {value/100} hundred',
  },
  x_axis_name: {
    type: 'TextControl',
    label: 'X_Axis_Name',
    default: '',
    description: 'x_axis_name, like: {value/100} hundred',
  },
  x_bottom_metrics: {
    type: 'SelectControl',
    multi: true,
    label: 'Y_Left_Metrics',
    validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: 'One or many metrics to display',
  },
  x_top_metrics: {
    type: 'SelectControl',
    multi: true,
    label: 'Y_Left_Metrics',
    validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: 'One or many metrics to display',
  },
  x_bottom_format: {
    type: 'TextControl',
    label: 'X_Bottom_Format',
    default: '',
    description: 'x_bottom_format, like: {value/100} hundred',
  },
  x_top_format: {
    type: 'TextControl',
    label: 'X_Top_Format',
    default: '',
    description: 'x_top_format, like: {value/100} hundred',
  },
  x_bottom_degree: {
    type: 'TextControl',
    label: 'X_Bottom_Degree',
    default: '',
    description: 'x_bottom_degree, like: {value/100} hundred',
  },
  x_top_degree: {
    type: 'TextControl',
    label: 'X_Top_Degree',
    default: '',
    description: 'x_top_degree, like: {value/100} hundred',
  },

  // add new by lijf
  subheader: {
    type: 'TextControl',
    label: 'Subheader',
    default: '',
  },
  label_position: {
    type: 'SelectControl',
    freeForm: true,
    label: 'Label_Position',
    default: null,
    choices: formatSelectOptions(['inside', 'outside']),
  },
  circle_type: {
    type: 'SelectControl',
    freeForm: true,
    renderTrigger: true,
    label: 'Circle_Type',
    choices: formatSelectOptions(['none', 'big', 'medium', 'small']),
    default: 'none',
  },
  circle: {
    type: 'CheckboxControl',
    renderTrigger: true,
    label: 'Circle',
    default: true,
  },
  normal: {
    type: 'CheckboxControl',
    renderTrigger: true,
    label: 'Full',
    default: true,
  },
  rose_type: {
    type: 'SelectControl',
    freeForm: true,
    renderTrigger: true,
    label: 'Rose_Type',
    default: null,
    choices: formatSelectOptions(['radius', 'area']),
  },
  label_format: {
    type: 'TextControl',
    label: 'Label_Format',
    default: '{b}  : {c} ({d}%)',
  },
  metrics_one: {
    type: 'SelectControl',
    label: 'Metrics1',
    clearable: false,
    description: 'Choose the metric',
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
    label: 'Metrics2',
    clearable: false,
    description: 'Choose the metric',
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
    label: 'Parent_Id',
    default: '',
    description: 'One or many controls to group by',
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
    label: 'Line Metrics',
    validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: 'line metrics,other are bar metrics',
  },
  y_left_splitLine: {
    type: 'CheckboxControl',
    label: 'Y_Left_SplitLine',
    renderTrigger: true,
    default: true,
    description: 'onle show left splitLine',
  },
  y_right_splitLine: {
    type: 'CheckboxControl',
    label: 'Y_Right_SplitLine',
    renderTrigger: true,
    default: false,
    description: 'onle show right splitLine',
  },

  //echarts_pie_h
  inner_metrics: {
    type: 'SelectControl',
    multi: true,
    label: 'Inner_Metrics',
    validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: 'One or many metrics to display',
  },
  inner_label_position: {
    type: 'SelectControl',
    freeForm: true,
    label: 'Inner_Label_Position',
    choices: formatSelectOptions(LABEL_POSITION),
    default: 'inside',
  },
  inner_label_format: {
    type: 'TextControl',
    label: 'Label_Format',
    default: '{b}  : {c} ({d}%)',
    description: 'example:{b}  : {c} ({d}%)',
  },
  inner_lable_color: {
    type: 'TextControl',
    label: 'Inner_Lable_Color',
    default: '#fff',
    description: 'inner lable color example: #fff',
  },
  outer_metrics: {
    type: 'SelectControl',
    multi: true,
    label: 'Outer_Metrics',
    validators: [v.nonEmpty],
    valueKey: 'metric_name',
    optionRenderer: m => <MetricOption metric={m} />,
    valueRenderer: m => <MetricOption metric={m} />,
    default: c => c.options && c.options.length > 0 ? [c.options[0].metric_name] : null,
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.metrics : [],
    }),
    description: 'One or many metrics to display',
  },
  outer_label_position: {
    type: 'SelectControl',
    freeForm: true,
    label: 'Outer_Label_Position',
    choices: formatSelectOptions(LABEL_POSITION),
    default: 'outside',
  },
  outer_label_format: {
    type: 'TextControl',
    label: 'Label_Format',
    default: '{b}  : {c} ({d}%)',
    description: 'example:{b}  : {c} ({d}%)',
  },

  //echarts_pie_h_g
  col_num: {
    type: 'SelectControl',
    freeForm: true,
    label: 'Col_Num',
    choices: formatSelectOptions(ROW_COL_NUM),
    default: 1,
  },
  inner_metrics_one: {
    type: 'SelectControl',
    multi: false,
    label: 'Inner_Circle_Metrics',
    default: [],
    description: 'Inner Circle Metrics',
    optionRenderer: c => <ColumnOption column={c} />,
    valueRenderer: c => <ColumnOption column={c} />,
    valueKey: 'column_name',
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.columns : [],
    }),
  },  
  child_id: {
    type: 'SelectControl',

    label: 'Child_Id',
    default: '',
    description: 'One or many controls to group by',
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
    label: 'Outer_Circle_Metrics',
    default: [],
    description: 'Outer Circle Metrics',
    optionRenderer: c => <ColumnOption column={c} />,
    valueRenderer: c => <ColumnOption column={c} />,
    valueKey: 'column_name',
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.columns : [],
    }),
  },
  child_name: {
    type: 'SelectControl',
    label: 'Child_Name',
    default: '',
    description: 'One or many controls to group by',
    optionRenderer: c => <ColumnOption column={c} />,
    valueRenderer: c => <ColumnOption column={c} />,
    valueKey: 'column_name',
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.columns : [],
    }),
  },
  visible_min: {
    type: 'TextControl',
    label: 'Visible_Min',
    default: '1000',
  },
  leaf_depth: {
    type: 'SelectControl',
    freeForm: true,
    label: 'Leaf_Depth',
    default: '1',
    choices: formatSelectOptions(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']),
  },

  //echarts_dash_board
  dash_min: {
    type: 'TextControl',
    label: 'Dash_Min',
    default: '0',
    description: 'dash min',
  },
  dash_max: {
    type: 'TextControl',
    label: 'Dash_Max',
    default: '100',
    description: 'dash max',
  },
  dash_name: {
    type: 'TextControl',
    label: 'Dash_Name',
    default: 'completion rate',
    description: 'dash name',
  },
  dash_splitNum: {
    type: 'TextControl',
    label: 'Dash_SplitNum',
    default: '10',
    description: 'dash splitNum',
  },
  dash_expr: {
    type: 'TextControl',
    label: 'Dash_Expr',
    default: 'value',
    description: 'dash expr',
  },
  dash_suffix: {
    type: 'TextControl',
    label: 'Dash_Suffix',
    default: '%',
    description: 'dash suffix',
  },
  dash_style: {
    type: 'TextControl',
    label: 'Dash_Style',
    default: '[0.2, #91c7ae]+[0.8, #63869e]+[1, #c23531]',
    description: 'dash style',
  },

  //echarts_big_number
  fontSize: {
    type: 'TextControl',
    label: 'FontSize',
    default: '15',
    description: 'fontSize',
  },

  //echarts_quadrant
  x_metric: {
    type: 'SelectControl',
    label: 'X_Axis_Metrics',
    clearable: false,
    description: 'X axis metrics',
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
    label: 'Y_Axis_Metrics',
    clearable: false,
    description: 'Y axis metrics',
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
    label: 'Focus_X_Axis',
    default: '',
    description: 'Focus X Axis',
  },
  origin_y: {
    type: 'TextControl',
    label: 'Focus_Y_Axis',
    default: '',
    description: 'Focus Y Axis',
  },
  min_x_axis: {
    type: 'TextControl',
    label: 'Min_X_Axis',
    default: '',
    description: 'Min X Axis',
  },
  max_x_axis: {
    type: 'TextControl',
    label: 'Max_X_Axis',
    default: '',
    description: 'Max X Axis',
  },
  min_y_axis: {
    type: 'TextControl',
    label: 'Min_Y_Axis',
    default: '',
    description: 'Min Y Axis',
  },
  max_y_axis: {
    type: 'TextControl',
    label: 'Max_Y_Axis',
    default: '',
    description: 'Max Y Axis',
  },
  first_module_infor: {
    type: 'TextControl',
    label: 'First_Module_Information',
    default: '',
    description: 'First Module Information',
  },
  first_x: {
    type: 'TextControl',
    label: 'First_X',
    default: '80%',
    description: 'example: 80%',
  },
  first_y: {
    type: 'TextControl',
    label: 'First_Y',
    default: '5%',
    description: 'example: 5%',
  },
  second_module_infor: {
    type: 'TextControl',
    label: 'Second_Module_Information',
    default: '',
    description: 'Second Module Information',
  },
  second_x: {
    type: 'TextControl',
    label: 'Second_X',
    default: '12%',
    description: 'example: 12%',
  },
  second_y: {
    type: 'TextControl',
    label: 'Second_Y',
    default: '5%',
    description: 'example: 5%',
  },
  third_module_infor: {
    type: 'TextControl',
    label: 'Third_Module_Information',
    default: '',
    description: 'Third Module Information',
  },
  third_x: {
    type: 'TextControl',
    label: 'Third_X',
    default: '12%',
    description: 'example: 12%',
  },
  third_y: {
    type: 'TextControl',
    label: 'Third_Y',
    default: '75%',
    description: 'example: 75%',
  },
  fourth_module_infor: {
    type: 'TextControl',
    label: 'Fourth_Module_Information',
    default: '',
    description: 'Fourth Module Information',
  },
  fourth_x: {
    type: 'TextControl',
    label: 'Fourth_X',
    default: '80%',
    description: 'example: 80%',
  },
  fourth_y: {
    type: 'TextControl',
    label: 'Fourth_Y',
    default: '75%',
    description: 'example: 75%',
  },
  point_size:{
    type: 'TextControl',
    label: 'Point_Size',
    default: '10',
    description: 'point size',
  },

  //china map
  groupby_one: {
    type: 'SelectControl',
    multi: false,
    label: 'Group by',
    default: [],
    description: 'One or many controls to group by',
    optionRenderer: c => <ColumnOption column={c} />,
    valueRenderer: c => <ColumnOption column={c} />,
    valueKey: 'column_name',
    mapStateToProps: state => ({
      options: (state.datasource) ? state.datasource.columns.filter(c => c.groupby) : [],
    }),
  },
  min_legend: {
    type: 'TextControl',
    label: 'Legend_Minimum',
    default: '',
    description: 'Enter the minimum value of the histogram',
  },
  max_legend: {
    type: 'TextControl',
    label: 'Legend_Maximum',
    default: '',
    description: 'Enter the minimum value of the histogram',
  },
  //china city map
  standard_point: {
    type: 'SelectControl',
    freeForm: true,
    label: 'Standard_Point',
    choices: formatSelectOptions(STANDARD_POINT),
    default: 4,
  },
  //big number
  head_color: {
    type: 'TextControl',
    label: 'Head_Color',
    default: '#4490ca',
    description: 'head color example: #4490ca',
  },
  body_color: {
    type: 'TextControl',
    label: 'Body_Color',
    default: '#4c9eda',
    description: 'body color example: #4490ca',
  },
  icone_select: {
    type: 'IconControl',
    label: 'icone select',
    renderTrigger: true,
    default: 'fa-comments',
    description: 'select icone',
  },
  format: {
    type: 'TextControl',
    label: 'Format',
    default: '',
    description: 'format, like: {value/100} hundred',
  },
  titleSize: {
    type: 'TextControl',
    label: 'TitleSize',
    default: '15',
    description: 'titleSize',
  },

  // echats_funnel
  order_type: {
    showHeader: true,
    label: 'flow',
    description: 'Required process',
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
    label: 'Lable_Color',
    default: '#96CDCD',
    description: 'lable color example: #96CDCD',
  },
  //big number two
  fontColor: {
    type: 'TextControl',
    label: 'Font_Color',
    default: '#2ab4c0',
    description: 'fontColor example: #2ab4c0',
  },
  number_description: {
    type: 'TextControl',
    label: 'Number_Description',
    default: '',
  },
  progress_description: {
    type: 'TextControl',
    label: 'Progress_Description',
    default: '',
  },
  big_number_fontSize: {
    type: 'TextControl',
    label: 'FontSize',
    default: '30',
    description: 'fontSize',
  },
  //big number tree
  icon_color: {
    type: 'TextControl',
    label: 'Icon_Color',
    default: '#2ab4c0',
    description: 'Icon_Color example: #2ab4c0',
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