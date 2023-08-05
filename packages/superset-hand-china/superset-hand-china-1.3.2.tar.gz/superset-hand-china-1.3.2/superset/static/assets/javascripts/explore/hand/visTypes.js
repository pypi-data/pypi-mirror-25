import { t } from '../../locales';

export const visTypes = {
  filter_box: {
    label: t('Filter Box'),
    controlPanelSections: [
      {
        label: t('Filter Options'),
        expanded: true,
        controlSetRows: [
          ['date_filter', 'instant_filtering'],
          ['groupby'],
          ['metric'],
        ],
      },
      {
        label: t('Setting Options'),
        controlSetRows: [
          ['show_modal']
        ]
      },
      {
        label: t('Base Setting'),
        controlSetRows: [
          ['filterSetting'],
        ]
      },
      {
        label: t('Set Default Value'),
        controlSetRows: [
          ['defaultValueSetting'],
        ]
      },
      {
        label: t('Set Date Value'),
        controlSetRows: [
          ['dateValueSetting'],
        ]
      },
    ],
    controlOverrides: {
      groupby: {
        label: t('Filter Controls'),
        description: (
          t('The controls you want to filter on. Note that only columns ' +
          'checked as "filterable" will show up on this list.')
        ),
        mapStateToProps: state => ({
          options: (state.datasource) ? state.datasource.columns.filter(c => c.filterable) : [],
        }),
      },
    },
  },
  filter_box_tree: {
    label: t('Filter Box Tree'),
    controlPanelSections: [
      {
        label: t('Metrics And Dimensions'),
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
        label: t('Setting Options'),
        controlSetRows: [
          ['show_modal']
        ]
      },
      {
        label: t('Set Default Value Filter Tree'),
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
    label: t('Filter Box Combination'),
    controlPanelSections: [
      {
        label: t('Filter Combination'),
        expanded: true,
        controlSetRows: [
          ['filter_combination'],
        ]
      },
    ]
  },
  // filter_box_cascade: {
  //   label: t('Filter Box Cascade'),
  //   controlPanelSections: [
  //     {
  //       label: t('Cascade Options'),
  //       expanded: true,
  //       controlSetRows: [
  //         ['groupby', 'metric'],
  //         ['width'],
  //         ['instant_filtering'],
  //       ]
  //     },
  //     {
  //       label: t('Setting Options'),
  //       expanded: true,
  //       controlSetRows: [
  //         ['show_modal']
  //       ]
  //     },
  //     {
  //       label: t('Cascade Setting'),
  //       controlSetRows: [
  //         ['cascade'],
  //       ]
  //     },
  //     {
  //       label: t('Set Default Value'),
  //       controlSetRows: [
  //         ['defaultValueSetting'],
  //       ]
  //     },
  //   ]
  // },
  ag_grid: {
    label: t('Ag-Grid'),
    controlPanelSections: [
      {
        label: t('Chart Options'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
        ]
      },
      {
        label: t('AgGrid Options'),
        expanded: true,
        controlSetRows: [
          ['order_by_cols'],
          ['row_limit'],
          ['hide_options'],
        ]
      },
      {
        label: t('Setting Options'),
        controlSetRows: [
          ['show_modal']
        ]
      },
      {
        label: t('baseStyle'),
        controlSetRows: [
          ['table_style'],
          ['col_style']
        ]
      },
      {
        label: t('condition'),
        controlSetRows: [
          ['condition_style']
        ]
      },
      {
        label: t('compare'),
        controlSetRows: [
          ['compare_style']
        ]
      },
      {
        label: t('navigator'),
        controlSetRows: [
          ['navigator']
        ]
      },
      {
        label: t('agGrid'),
        controlSetRows: [
          ['theme', 'pageSize'],
          ['frozen_left', 'frozen_right'],
          ['link_cols', 'hide_cols'],
          ['is_pivot'],
          ['parent_node']
        ]
      },
      {
        label: t('agGrid_pivot'),
        controlSetRows: [
          ['pivot_groupby'],
          ['columns'],
          ['pivot_metrics']
        ]
      }
    ]
  },
  echarts_bar_progress: {
    label: t('Echarts - Bar progress'),
    controlPanelSections: [
      {
        label: t('Metrics And Dim'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: t('Only Bottom X Options'),
        controlSetRows: [
          ['x_format', 'x_degree'],
          ['x_axis_name'],
        ]
      },
      {
        label: t('Padding Options'),
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
          ['bar_width'],
        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['enabled_bar_width'],
        ]
      },
      {
        label: t('Bar Stacks'),
        description: t('bar stacks'),
        controlSetRows: [['stacks']],
      }
    ],
    controlOverrides: {
      groupby: {
        label: t('Y_Axis'),
        description: t('One or many fields to group by'),
      },
    },
  },
  echarts_bar: {
    label: t('Echart - Bar Chart'),
    controlPanelSections: [
      {
        label: t('Chart Options'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: t('Only Left Options'),
        controlSetRows: [
          ['only_left', 'y_metrics'],
          ['y_format', 'y_degree'],
          ['y_axis_name'],
        ]
      },
      {
        label: t('Multi Y Options'),
        controlSetRows: [
          ['y_left_metrics', 'y_right_metrics'],
          ['y_left_format', 'y_right_format'],
          ['y_left_degree', 'y_right_degree'],
        ]
      },
      {
        label: t('Padding Options'),
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
          ['bar_width'],
        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['is_avg', 'is_max_min'],
          ['is_bar_value', 'enabled_bar_width'],
        ]
      },
      {
        label: t('Bar Stacks'),
        description: t('bar stacks'),
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
    label: t('echarts bar waterfall View'),
    controlPanelSections: [
      {
        label: t('metrics and dismensions'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: t('Padding'),
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
          ['y_format', 'y_degree'],
          ['y_axis_name'],
          ['bar_width'],
        ],
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['enabled_bar_width'],
        ]
      },
    ]
  },
  echarts_bar_h: {
    label: t('Echart - Bar Chart horizohtal'),
    controlPanelSections: [
      {
        label: t('Chart Options'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: t('Only Bottom Options'),
        controlSetRows: [
          ['only_bottom', 'x_metrics'],
          ['x_format', 'x_degree'],
          ['x_axis_name'],
        ]
      },
      {
        label: t('Multi X Options'),
        controlSetRows: [
          ['x_bottom_metrics', 'x_top_metrics'],
          ['x_bottom_format', 'x_top_format'],
          ['x_bottom_degree', 'x_top_degree'],
        ]
      },
      {
        label: t('Padding Options'),
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
          ['bar_width'],
        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['is_avg', 'is_max_min'],
          ['is_bar_value', 'enabled_bar_width'],
        ]
      },
      {
        label: t('Bar Stacks'),
        description: t('bar stacks'),
        controlSetRows: [['stacks']],
      },
    ]
  },
  echarts_line_bar: {
    label: t('Echart - Line Bar'),
    controlPanelSections: [
      {
        label: t('Metrics And Dimensions'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: t('Line and Bar'),
        controlSetRows: [
          ['line_choice'],
        ]
      },
      {
        label: t('Only Left Options'),
        controlSetRows: [
          ['only_left', 'y_metrics'],
          ['y_format', 'y_degree'],
          ['y_axis_name'],
        ]
      },
      {
        label: t('Muti Y Axis Options'),
        controlSetRows: [
          ['y_left_metrics', 'y_right_metrics'],
          ['y_left_format', 'y_right_format'],
          ['y_left_degree', 'y_right_degree'],
        ]
      },
      {
        label: t('Padding Options'),
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
          ['bar_width'],
        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['is_avg', 'is_max_min'],
          ['is_bar_value', 'enabled_bar_width'],
        ]
      },
      {
        label: t('Bar Stacks'),
        description: t('bar stacks'),
        controlSetRows: [['stacks']],
      },
    ],
    controlOverrides: {
      groupby: {
        label: t('Y Axis'),
        description: t('One or many fields to group by'),
      },
    },
  },
  echarts_line: {
    label: t('Echart - line View'),
    controlPanelSections: [
      {
        label: t('Chart Options'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: t('Only Left Options'),
        controlSetRows: [
          ['only_left', 'y_metrics'],
          ['y_format', 'y_degree'],
          ['y_axis_name'],
        ]
      },
      {
        label: t('Multi Y Options'),
        controlSetRows: [
          ['y_left_metrics', 'y_right_metrics'],
          ['y_left_format', 'y_right_format'],
          ['y_left_degree', 'y_right_degree'],
          ['y_left_splitLine','y_right_splitLine']
        ]
      },
      {
        label: t('Padding Options'),
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['is_avg', 'is_max_min'],
          ['is_bar_value'],
        ]
      },
    ]
  },
  echarts_pie_m: {
    label: t('Echarts Pie Metrics View'),
    controlPanelSections: [
      {
        label: t('Metrics'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['order_by_cols'],
          ['row_limit'],

        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['label_position', 'label_format'],
          ['circle_type', 'rose_type'],
        ],
      },
    ]
  },
  echarts_pie_h: {
    label: t('Echart - Echarts Pie h'),
    controlPanelSections: [
      {
        label: t('Metrics Options'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['order_by_cols'],
          ['row_limit'],

        ]
      },
      {
        label: t('Inner Circle'),
        controlSetRows: [
          ['inner_metrics'],
          ['inner_label_position', 'inner_label_format'],
          ['inner_lable_color'],
        ]
      },
      {
        label: t('Outer Circle'),
        controlSetRows: [
          ['outer_metrics'],
          ['outer_label_position', 'outer_label_format'],
        ]
      },
    ]
  },
  echarts_pie_g: {
    label: t('Echarts Pie GroupBy View'),
    controlPanelSections: [
      {
        label: t('Metrics'),
        expanded: true,
        controlSetRows: [
          ['groupby', 'metrics'],
          ['order_by_cols'],
          ['row_limit'],

        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['label_position', 'label_format'],
          ['circle_type', 'rose_type'],
          ['col_num']
        ],
      },
    ]
  },

  echarts_pie_h_g: {
    label: t('Echart - Pie Hierarchical GroupBy View'),
    controlPanelSections: [
      {
        label: t('Metrics Options'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['order_by_cols'],
          ['col_num'],
          ['row_limit'],
        ]
      },
      {
        label: t('Inner Circle'),
        controlSetRows: [
          ['inner_metrics_one'],
          ['inner_label_position', 'inner_label_format'],
          ['inner_lable_color'],
        ]
      },
      {
        label: t('Outer Circle'),
        controlSetRows: [
          ['outer_metrics_one'],
          ['outer_label_position', 'outer_label_format'],
        ]
      },
    ]
  },
  echarts_dash_board: {
    label: t('Echart - Dash Board'),
    controlPanelSections: [
      {
        label: t('Metrics Options'),
        controlSetRows: [
          ['metric'],
          ['row_limit'],
        ]
      },
      {
        label: t('Other Option'),
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
    label: t('Echarts Big Number Compare'),
    controlPanelSections: [
      {
        label: t('Metrics And Dimensions'),
        expanded: true,
        controlSetRows: [
          ['metrics_one', 'metrics_two'],
          ['subheader', 'fontSize'],
        ]
      },
    ]
  },
  echarts_big_number: {
    label: t('Echart - Big Number'),
    controlPanelSections: [
      {
        label: t('Chart Options'),
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
    label: t('Big Number'),
    controlPanelSections: [
      {
        label: t('Big Number'),
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
    label: t('Big Number Two'),
    controlPanelSections: [
      {
        label: t('Big Number Two'),
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
    label: t('Big Number Three'),
    controlPanelSections: [
      {
        label: t('Big Number Three'),
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
    label: t('China Map'),
    controlPanelSections: [
      {
        label: t('Metrics and Dimensions '),
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
    label: t('China City Map'),
    controlPanelSections: [
      {
        label: t('Metrics and Dimensions '),
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
    label: t('China City Map Migration'),
    controlPanelSections: [
      {
        label: t('Metrics and Dimensions '),
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
        label: t('From City / To City'),
        description: t('Choose a from city and a to city'),
      }
    },
  },

  echarts_bubble: {
    label: t('Echart - Bubble Viz'),
    controlPanelSections: [
      {
        label: t('Chart Options'),
        expanded: true,
        controlSetRows: [
          ['series', 'entity'],
          ['x', 'y'],
          ['size', 'row_limit'],
        ]
      },
      {
        label: t('Chart Options'),
        controlSetRows: [
          ['y_degree', 'y_format'],
          ['x_degree', 'x_format'],
          ['x_axis_label', 'y_axis_label'],
        ]
      },
      {
        label: t('Padding Options'),
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
        ]
      }
    ]
  },
  echarts_quadrant: {
    label: t('Echart - Quadrant'),
    controlPanelSections: [
      {
        label: t('Chart Options'),
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
    label: t('Echart - Area Stack View'),
    controlPanelSections: [
      {
        label: t('Area Stack Options'),
        expanded: true,
        controlSetRows: [
          ['metrics'],
          ['groupby'],
          ['order_by_cols'],
          ['row_limit'],
        ]
      },
      {
        label: t('Left Options'),
        controlSetRows: [
          ['y_metrics'],
          ['y_format', 'y_degree'],
          ['y_axis_name'],
        ]
      },
      {
        label: t('Padding Options'),
        controlSetRows: [
          ['top_padding', 'bottom_padding'],
          ['left_padding', 'right_padding'],
        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['is_bar_value', 'normal'],
          ['lable_color'],
        ]
      },
    ]
  },

  //echarts sankey
  echarts_sankey: {
    label: t('Echart - Sankey'),
    controlPanelSections: [
      {
        label: t('Metrics Options'),
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
        label: t('Source / Target'),
        description: t('Choose a source and a target'),
      }
    },
  },


  //漏斗图
  echarts_funnel: {
    label: t('echarts_funnel'),
    controlPanelSections: [
      {
        label: t('Metrics Options'),
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
    label: t('echarts Radar Map View'),
    controlPanelSections: [
      {
        label: t('metrics'),
        expanded: true,
        controlSetRows: [
          ['groupby', 'metrics'],
          ['row_limit'],
        ]
      },
      {
        label: t('Other Options'),
        controlSetRows: [
          ['circle', 'normal'],
        ],
      },
    ]
  },
  echarts_treemap: {
    label: t('Echarts Treemap'),
    controlPanelSections: [
      {
        label: t('metrics and dismensions'),
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
    label: t('echarts Word Cloud'),
    controlPanelSections: [
      {
        label: t('metrics and dismensions'),
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