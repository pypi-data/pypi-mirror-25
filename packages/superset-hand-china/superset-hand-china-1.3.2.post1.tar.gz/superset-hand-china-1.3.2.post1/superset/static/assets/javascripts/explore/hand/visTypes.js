export const visTypes = {
  filter_box: {
    label: 'Filter Box',
    controlPanelSections: [
      {
        label: 'Filter Options',
        expanded: true,
        controlSetRows: [
          ['date_filter', 'instant_filtering'],
          ['groupby'],
          ['metric'],
        ],
      },
      {
        label: 'Setting Options',
        controlSetRows: [
          ['show_modal']
        ]
      },
      {
        label: 'baseSetting',
        controlSetRows: [
          ['filterSetting'],
        ]
      },
      {
        label: 'setDefaultValue',
        controlSetRows: [
          ['defaultValueSetting'],
        ]
      },
      {
        label: 'setDateValue',
        controlSetRows: [
          ['dateValueSetting'],
        ]
      },
    ],
    controlOverrides: {
      groupby: {
        label: 'Filter controls',
        description: (
          'The controls you want to filter on. Note that only columns ' +
          'checked as "filterable" will show up on this list.'
        ),
        mapStateToProps: state => ({
          options: (state.datasource) ? state.datasource.columns.filter(c => c.filterable) : [],
        }),
      },
    },
  },
  filter_box_tree: {
    label: 'Filter Box Tree',
    controlPanelSections: [
      {
        label: 'metrics and dismensions',
        expanded: true,
        controlSetRows: [
          ['groupby', 'metrics'],
          ['parent_id', 'child_id'],
          ['child_name'],
          ['filter_name', 'width'],
          ['instant_filtering', 'multi'],
        ]
      },
      {
        label: 'Setting Options',
        controlSetRows: [
          ['show_modal']
        ]
      },
      {
        label: 'setDefaultValueFilterTree',
        controlSetRows: [
          ['defaultValueFilterTreeSetting'],
        ]
      },
      // {
      //   label: 'setDateValue',
      //   controlSetRows: [
      //     ['dateValueSetting'],
      //   ]
      // },
    ]
  },
  filter_box_combination: {
    label: 'Filter Box Combination',
    controlPanelSections: [
      {
        label: 'Filter Combination',
        expanded: true,
        controlSetRows: [
          ['filter_combination'],
        ]
      },
    ]
  },
  // filter_box_cascade: {
  //   label: 'Filter Box Cascade',
  //   controlPanelSections: [
  //     {
  //       label: 'Cascade Options',
  //       expanded: true,
  //       controlSetRows: [
  //         ['groupby', 'metric'],
  //         ['width'],
  //         ['instant_filtering'],
  //       ]
  //     },
  //     {
  //       label: 'Setting Options',
  //       expanded: true,
  //       controlSetRows: [
  //         ['show_modal']
  //       ]
  //     },
  //     {
  //       label: 'cascadeSetting',
  //       controlSetRows: [
  //         ['cascade'],
  //       ]
  //     },
  //     {
  //       label: 'setDefaultValue',
  //       controlSetRows: [
  //         ['defaultValueSetting'],
  //       ]
  //     },
  //   ]
  // },
  ag_grid: {
    label: 'Ag-Grid',
    controlPanelSections: [
      {
        label: 'Chart Options',
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
        ]
      },
      {
        label: 'AgGrid Options',
        expanded: true,
        controlSetRows: [
          ['order_by_cols'],
          ['row_limit'],
          ['hide_options'],
        ]
      },
      {
        label: 'Setting Options',
        controlSetRows: [
          ['show_modal']
        ]
      },
      {
        label: 'baseStyle',
        controlSetRows: [
          ['table_style'],
          ['col_style']
        ]
      },
      {
        label: 'condition',
        controlSetRows: [
          ['condition_style']
        ]
      },
      {
        label: 'compare',
        controlSetRows: [
          ['compare_style']
        ]
      },
      {
        label: 'navigator',
        controlSetRows: [
          ['navigator']
        ]
      },
      {
        label: 'agGrid',
        controlSetRows: [
          ['theme', 'pageSize'],
          ['frozen_left', 'frozen_right'],
          ['link_cols', 'hide_cols'],
          ['is_pivot'],
          ['parent_node']
        ]
      },
      {
        label: 'agGrid_pivot',
        controlSetRows: [
          ['pivot_groupby'],
          ['columns'],
          ['pivot_metrics']
        ]
      }
    ]
  },
  echarts_bar_progress: {
    label: 'Echarts - Bar progress',
    controlPanelSections: [
      {
        label: 'Metrics And Dim',
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: 'Only Bottom X Options',
        controlSetRows: [
          ['x_format', 'x_degree'],
          ['x_axis_name'],
        ]
      },
      {
        label: 'Padding Options',
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
          ['bar_width'],
        ]
      },
      {
        label: 'Other Options',
        controlSetRows: [
          ['enabled_bar_width'],
        ]
      },
      {
        label: 'Bar Stacks',
        description: 'bar stacks',
        controlSetRows: [['stacks']],
      }
    ],
    controlOverrides: {
      groupby: {
        label: 'Y_Axis',
        description: 'One or many fields to group by',
      },
    },
  },
  echarts_bar: {
    label: 'Echart - Bar Chart',
    controlPanelSections: [
      {
        label: 'Chart Options',
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: 'Only Left Options',
        controlSetRows: [
          ['only_left', 'y_metrics'],
          ['y_format', 'y_degree'],
          ['y_axis_name'],
        ]
      },
      {
        label: 'Multi Y Options',
        controlSetRows: [
          ['y_left_metrics', 'y_right_metrics'],
          ['y_left_format', 'y_right_format'],
          ['y_left_degree', 'y_right_degree'],
        ]
      },
      {
        label: 'Padding Options',
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
          ['bar_width'],
        ]
      },
      {
        label: 'Other Options',
        controlSetRows: [
          ['is_avg', 'is_max_min'],
          ['is_bar_value', 'enabled_bar_width'],
        ]
      },
      {
        label: 'Bar Stacks',
        description: 'bar stacks',
        controlSetRows: [['stacks']],
      },
    ],
    // controlOverrides: {
    //   groupby: {
    //     label: 'Series',
    //   },
    //   columns: {
    //     label: 'Breakdowns',
    //     description: 'Defines how each series is broken down',
    //   },
    // },
  },
  echarts_bar_waterfall: {
    label: 'echarts bar waterfall View',
    controlPanelSections: [
      {
        label: 'metrics and dismensions',
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: 'Padding',
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
          ['y_format', 'y_degree'],
          ['y_axis_name'],
          ['bar_width'],
        ],
      },
      {
        label: 'Other Options',
        controlSetRows: [
          ['enabled_bar_width'],
        ]
      },
    ]
  },
  echarts_bar_h: {
    label: 'Echart - Bar Chart horizohtal',
    controlPanelSections: [
      {
        label: 'Chart Options',
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: 'Only Bottom Options',
        controlSetRows: [
          ['only_bottom', 'x_metrics'],
          ['x_format', 'x_degree'],
          ['x_axis_name'],
        ]
      },
      {
        label: 'Multi X Options',
        controlSetRows: [
          ['x_bottom_metrics', 'x_top_metrics'],
          ['x_bottom_format', 'x_top_format'],
          ['x_bottom_degree', 'x_top_degree'],
        ]
      },
      {
        label: 'Padding Options',
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
          ['bar_width'],
        ]
      },
      {
        label: 'Other Options',
        controlSetRows: [
          ['is_avg', 'is_max_min'],
          ['is_bar_value', 'enabled_bar_width'],
        ]
      },
      {
        label: 'Bar Stacks',
        description: 'bar stacks',
        controlSetRows: [['stacks']],
      },
    ]
  },
  echarts_line_bar: {
    label: 'Echart - Line Bar',
    controlPanelSections: [
      {
        label: 'Metrics And Dimensions',
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: 'Line and Bar',
        controlSetRows: [
          ['line_choice'],
        ]
      },
      {
        label: 'Only Left Options',
        controlSetRows: [
          ['only_left', 'y_metrics'],
          ['y_format', 'y_degree'],
          ['y_axis_name'],
        ]
      },
      {
        label: 'Muti Y Axis Options',
        controlSetRows: [
          ['y_left_metrics', 'y_right_metrics'],
          ['y_left_format', 'y_right_format'],
          ['y_left_degree', 'y_right_degree'],
        ]
      },
      {
        label: 'Padding Options',
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
          ['bar_width'],
        ]
      },
      {
        label: 'Other Options',
        controlSetRows: [
          ['is_avg', 'is_max_min'],
          ['is_bar_value', 'enabled_bar_width'],
        ]
      },
      {
        label: 'Bar Stacks',
        description: 'bar stacks',
        controlSetRows: [['stacks']],
      },
    ],
    controlOverrides: {
      groupby: {
        label: 'Y_Axis',
        description: 'One or many fields to group by',
      },
    },
  },
  echarts_line: {
    label: 'Echart - line View',
    controlPanelSections: [
      {
        label: 'Chart Options',
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],

        ]
      },
      {
        label: 'Only Left Options',
        controlSetRows: [
          ['only_left', 'y_metrics'],
          ['y_format', 'y_degree'],
          ['y_axis_name'],
        ]
      },
      {
        label: 'Multi Y Options',
        controlSetRows: [
          ['y_left_metrics', 'y_right_metrics'],
          ['y_left_format', 'y_right_format'],
          ['y_left_degree', 'y_right_degree'],
          ['y_left_splitLine','y_right_splitLine']
        ]
      },
      {
        label: 'Padding Options',
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
        ]
      },
      {
        label: 'Other Options',
        controlSetRows: [
          ['is_avg', 'is_max_min'],
          ['is_bar_value'],
        ]
      },
    ]
  },
  echarts_pie_m: {
    label: 'echarts Pie Metrics View',
    controlPanelSections: [
      {
        label: 'metrics',
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['order_by_cols'],
          ['row_limit'],

        ]
      },
      {
        label: 'Other Options',
        controlSetRows: [
          ['label_position', 'label_format'],
          ['circle_type', 'rose_type'],
        ],
      },
    ]
  },
  echarts_pie_h: {
    label: 'Echart - Echarts Pie h',
    controlPanelSections: [
      {
        label: 'Metrics Options',
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['order_by_cols'],
          ['row_limit'],

        ]
      },
      {
        label: 'Inner Circle',
        controlSetRows: [
          ['inner_metrics'],
          ['inner_label_position', 'inner_label_format'],
          ['inner_lable_color'],
        ]
      },
      {
        label: 'Outer Circle',
        controlSetRows: [
          ['outer_metrics'],
          ['outer_label_position', 'outer_label_format'],
        ]
      },
    ]
  },
  echarts_pie_g: {
    label: 'echarts Pie GroupBy View',
    controlPanelSections: [
      {
        label: 'metrics',
        expanded: true,
        controlSetRows: [
          ['groupby', 'metrics'],
          ['order_by_cols'],
          ['row_limit'],

        ]
      },
      {
        label: 'Other Options',
        controlSetRows: [
          ['label_position', 'label_format'],
          ['circle_type', 'rose_type'],
          ['col_num']
        ],
      },
    ]
  },

  echarts_pie_h_g: {
    label: 'Echart - Pie Hierarchical GroupBy View',
    controlPanelSections: [
      {
        label: 'Metrics Options',
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['order_by_cols'],
          ['col_num'],
          ['row_limit'],
        ]
      },
      {
        label: 'Inner Circle',
        controlSetRows: [
          ['inner_metrics_one'],
          ['inner_label_position', 'inner_label_format'],
          ['inner_lable_color'],
        ]
      },
      {
        label: 'Outer Circle',
        controlSetRows: [
          ['outer_metrics_one'],
          ['outer_label_position', 'outer_label_format'],
        ]
      },
    ]
  },
  echarts_dash_board: {
    label: 'Echart - Dash Board',
    controlPanelSections: [
      {
        label: 'Metrics Options',
        controlSetRows: [
          ['metric'],
          ['row_limit'],
        ]
      },
      {
        label: 'Other Option',
        controlSetRows: [
          ['dash_min', 'dash_max'],
          ['dash_name', 'dash_splitNum'],
          ['dash_expr', 'dash_suffix'],
          ['dash_style']
        ]
      },
    ]
  },
  echarts_big_number_compare: {
    label: 'echarts Big Number Compare',
    controlPanelSections: [
      {
        label: 'metrics and dismensions',
        expanded: true,
        controlSetRows: [
          ['metrics_one', 'metrics_two'],
          ['subheader', 'fontSize'],
        ]
      },
    ]
  },
  echarts_big_number: {
    label: 'Echart - Big Number',
    controlPanelSections: [
      {
        label: 'Chart Options',
        expanded: true,
        controlSetRows: [
          ['metric'],
          ['subheader', 'fontSize'],
        ]
      },
    ]
  },
  //big number
  big_number_viz: {
    label: 'Big Number',
    controlPanelSections: [
      {
        label: "Big Number",
        expanded: true,
        controlSetRows: [
          ['metric'],
          ['subheader', 'titleSize'],
          ['head_color', 'body_color'],
          ['format', 'big_number_fontSize'],
          ['icone_select'],
        ]
      },
    ]
  },

  //big number two
  big_number_two_viz: {
    label: 'Big Number Two',
    controlPanelSections: [
      {
        label: "Big Number Two",
        expanded: true,
        controlSetRows: [
          ['metric'],
          ['metrics_one', 'metrics_two'],
          ['format', 'big_number_fontSize'],
          ['fontColor'],
          ['number_description', 'progress_description'],
          ['icone_select'],
        ]
      },
    ]
  },
  //big number two
  big_number_three_viz: {
    label: 'Big Number Three',
    controlPanelSections: [
      {
        label: "Big Number Three",
        expanded: true,
        controlSetRows: [
          ['metric'],
          ['subheader', 'number_description'],
          ['format', 'big_number_fontSize'],
          ['icon_color'],
          ['icone_select'],
        ]
      },
    ]
  },
  echarts_china_map: {
    label: 'China Map',
    controlPanelSections: [
      {
        label: 'Metrics and Dimensions ',
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby_one'],
          ['min_legend'],
          ['max_legend'],
        ]
      },
    ]
  },

  china_city_map: {
    label: 'China City Map',
    controlPanelSections: [
      {
        label: 'Metrics and Dimensions ',
        expanded: true,
        controlSetRows: [
          ['metric'],
          ['groupby_one'],
          ['standard_point'],
        ]
      },
    ]
  },
  //echarts china city map migration
  echarts_china_city_map_migration: {
    label: 'China City Map Migration',
    controlPanelSections: [
      {
        label: 'Metrics and Dimensions ',
        expanded: true,
        controlSetRows: [
          ['metric'],
          ['groupby'],
          ['min_legend'],
          ['max_legend'],
        ]
      },
    ],
    controlOverrides: {
      groupby: {
        label: 'From City / To City',
        description: 'Choose a from city and a to city',
      }
    },
  },

  echarts_bubble: {
    label: 'Echart - Bubble Viz',
    controlPanelSections: [
      {
        label: 'Chart Options',
        expanded: true,
        controlSetRows: [
          ['series', 'entity'],
          ['x', 'y'],
          ['size', 'row_limit'],
        ]
      },
      {
        label: 'Chart Options',
        controlSetRows: [
          ['y_degree', 'y_format'],
          ['x_degree', 'x_format'],
          ['x_axis_label', 'y_axis_label'],
        ]
      },
      {
        label: 'Padding Options',
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
        ]
      }
    ]
  },
  echarts_quadrant: {
    label: 'Echart - Quadrant',
    controlPanelSections: [
      {
        label: 'Chart Options',
        expanded: true,
        controlSetRows: [
          ['series'],
          ['x_metric', 'y_metric'],
          ['origin_x', 'origin_y'],
          ['min_x_axis', 'max_x_axis'],
          ['min_y_axis', 'max_y_axis'],
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
          ['point_size'],
          ['first_module_infor'],
          ['first_x', 'first_y'],
          ['second_module_infor'],
          ['second_x', 'second_y'],
          ['third_module_infor'],
          ['third_x', 'third_y'],
          ['fourth_module_infor'],
          ['fourth_x', 'fourth_y'],
        ]
      },
    ]
  },

  //echarts area stack
  echarts_area_stack: {
    label: 'Echart - Area Stack View',
    controlPanelSections: [
      {
        label: 'Area Stack Options',
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: 'Left Options',
        controlSetRows: [
          ['y_metrics'],
          ['y_format', 'y_degree'],
          ['y_axis_name'],
        ]
      },
      {
        label: 'Padding Options',
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
        ]
      },
      {
        label: 'Other Options',
        controlSetRows: [
          ['is_bar_value', 'normal'],
          ['lable_color'],
        ]
      },
    ]
  },

  //echarts sankey
  echarts_sankey: {
    label: 'Echart - Sankey',
    controlPanelSections: [
      {
        label: 'Metrics Options',
        expanded: true,
        controlSetRows: [
          ['groupby'],
          ['metric'],
          ['row_limit'],
        ]
      }
    ],
    controlOverrides: {
      groupby: {
        label: 'Source / Target',
        description: 'Choose a source and a target',
      }
    },
  },


  //漏斗图
  echarts_funnel: {
    label: 'echarts_funnel',
    controlPanelSections: [
      {
        label: 'Metrics Options',
        expanded: true,
        controlSetRows: [
           ['groupby_one'],
           ['metric'],
           ['order_type'],
        
        ]
      },
    ]
  },
  echarts_radar_map: {
    label: 'echarts Radar Map View',
    controlPanelSections: [
      {
        label: 'metrics',
        expanded: true,
        controlSetRows: [
          ['groupby', 'metrics'],
          ['row_limit'],
        ]
      },
      {
        label: 'Other Options',
        controlSetRows: [
          ['circle', 'normal'],
        ],
      },
    ]
  },
  echarts_treemap: {
    label: 'Echarts Treemap',
    controlPanelSections: [
      {
        label: 'metrics and dismensions',
        expanded: true,
        controlSetRows: [
          ['groupby', 'metrics'],
          ['parent_id', 'child_id'],
          ['child_name'],
          ['visible_min', 'leaf_depth'],
        ]
      },
    ]
  },
  echarts_word_cloud: {
    label: 'echarts Word Cloud',
    controlPanelSections: [
      {
        label: 'metrics and dismensions',
        expanded: true,
        controlSetRows: [
          ['series', 'metric', 'limit'],
          ['size_from', 'size_to'],
          ['rotation'],
        ]
      },
    ]
  },
}