import React from 'react';
import PropTypes from 'prop-types';
import { Responsive, WidthProvider } from 'react-grid-layout';
import $ from 'jquery';

// import SliceCell from './SliceCell';
import SliceCell from '../hand/SliceCell';
import { getExploreUrl } from '../../explore/exploreUtils';
var ReactGridLayout = require('react-grid-layout');
require('react-grid-layout/css/styles.css');
require('react-resizable/css/styles.css');

ReactGridLayout = WidthProvider(ReactGridLayout);

const propTypes = {
  dashboard: PropTypes.object.isRequired,
};

class GridLayout extends React.Component {
  componentWillMount() {
    this.initializationState();
  }

  initializationState() {
    const layout = [];

    this.props.dashboard.slices.forEach((slice, index) => {
      const sliceId = slice.slice_id;
      let pos = this.props.dashboard.posDict[sliceId];
      if (!pos) {
        pos = {
          col: (index * 8 + 1) % 24,
          row: Math.floor((index) / 3) * 14,
          size_x: 8,
          size_y: 14,
          proportion: 14 / document.body.clientWidth,
        };
        this.props.dashboard.posDict[sliceId] = pos;
      }
      if (pos.proportion + "" === "-1") {
        pos = {
          col: (index * 8 + 1) % 24,
          row: Math.floor((index) / 3) * 14,
          size_x: 8,
          size_y: 14,
          proportion: 14 / document.body.clientWidth,
        };
        this.props.dashboard.posDict[sliceId].col = pos.col;
        this.props.dashboard.posDict[sliceId].row = pos.row;
        this.props.dashboard.posDict[sliceId].size_x = pos.size_x;
        this.props.dashboard.posDict[sliceId].proportion = pos.proportion;
      }
      if (!pos.proportion) {
        layout.push({
          i: String(sliceId),
          x: pos.col - 1,
          y: pos.row,
          w: pos.size_x,
          minW: 3,
          minH: 3,
          h: pos.size_y,
          proportion: pos.size_y / document.body.clientWidth,
        });
        this.props.dashboard.posDict[sliceId].col = pos.col;
        this.props.dashboard.posDict[sliceId].row = pos.row;
        this.props.dashboard.posDict[sliceId].size_x = pos.size_x;
        this.props.dashboard.posDict[sliceId].proportion = pos.size_y / document.body.clientWidth;
      } else {
        layout.push({
          i: String(sliceId),
          x: pos.col - 1,
          y: pos.row,
          w: pos.size_x,
          minW: 3,
          minH: 3,
          h: document.body.clientWidth * pos.proportion,
          proportion: pos.proportion,
        });
      }
    });

    this.setState({
      layout,
      slices: this.props.dashboard.slices,
    });
  }

  onResizeStop(layout, oldItem, newItem) {
    const newSlice = this.props.dashboard.getSlice(newItem.i);
    for (let j = 0; j < layout.length; j++) {
      layout[j]['proportion'] = layout[j].h / document.body.clientWidth;
      this.props.dashboard.posDict[layout[j].i].col = layout[j].x + 1;
      this.props.dashboard.posDict[layout[j].i].row = layout[j].y;
      this.props.dashboard.posDict[layout[j].i].size_x = layout[j].w;
      this.props.dashboard.posDict[layout[j].i].proportion = layout[j].h / document.body.clientWidth;
    }

    if (oldItem.w !== newItem.w || oldItem.h !== newItem.h) {
      // refresh combination's children filter

      if (newSlice.formData.viz_type === 'filter_box_combination') {
        this.setState({ layout }, () => {
          newSlice.resize();
          newSlice.formData.filter_combination.forEach(sliceId => {
            const childSlice = this.props.dashboard.getSlice(sliceId);
            childSlice.resize();
          });
        });
      } else {
        this.setState({ layout }, () => newSlice.resize());
      }
    }
    this.props.dashboard.onChange();
  }

  onDragStop(layout) {
    for (let j = 0; j < layout.length; j++) {
      layout[j]['proportion'] = layout[j].h / document.body.clientWidth;
      this.props.dashboard.posDict[layout[j].i].col = layout[j].x + 1;
      this.props.dashboard.posDict[layout[j].i].row = layout[j].y;
      this.props.dashboard.posDict[layout[j].i].size_x = layout[j].w;
      this.props.dashboard.posDict[layout[j].i].proportion = layout[j].h / document.body.clientWidth;
    }
    this.setState({ layout });
    this.props.dashboard.onChange();
  }

  removeSlice(sliceId) {
    // $('[data-toggle=tooltip]').tooltip('hide');
    this.setState({
      layout: this.state.layout.filter(function (reactPos) {
        return reactPos.i !== String(sliceId);
      }),
      slices: this.state.slices.filter(function (slice) {
        return slice.slice_id !== sliceId;
      }),
    });
    this.props.dashboard.onChange();
  }

  serialize() {
    return this.state.layout.map(reactPos => ({
      slice_id: reactPos.i,
      col: reactPos.x + 1,
      row: reactPos.y,
      size_x: reactPos.w,
      size_y: reactPos.h,
      proportion: reactPos.proportion,
    }));
  }

  getExcel(slice) {
    let excel_endpoint = getExploreUrl(slice.form_data, 'excel');
    const params = JSON.parse(this.getQueryString("preselect_filters"));
    var filter = {};
    for (var k in params) {
      for (var m in params[k]) {
        filter[m] = params[k][m];
      }
    }
    var filterStr = JSON.stringify(filter);
    location.href = excel_endpoint + '&extra_filters=' + filterStr;
  }

  // get url param
  getQueryString(name) {
    const reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    const r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(decodeURI(r[2]));
    return null;
  }

  componentWillReceiveProps(nextProps) {
    this.initializationState();
  }

  render() {
    return (
      <ReactGridLayout
        className="layout"
        layout={this.state.layout}
        onResizeStop={this.onResizeStop.bind(this)}
        onDragStop={this.onDragStop.bind(this)}
        cols={24}
        rowHeight={10}
        autoSize
        margin={[20, 20]}
        useCSSTransforms
        draggableHandle=".drag"
      >
        {this.state.slices.map((slice, index) => (
          <div
            id={'slice_' + slice.slice_id}
            key={slice.slice_id}
            data-slice-id={slice.slice_id}
            className={`widget ${slice.form_data.viz_type}`}
          >
            <SliceCell
              slice={slice}
              removeSlice={this.removeSlice.bind(this, slice.slice_id)}
              expandedSlices={this.props.dashboard.metadata.expanded_slices}
              getExcel={this.getExcel.bind(this, slice)}
              index={index}
            />
          </div>
        ))}
      </ReactGridLayout>
    );
  }
}

GridLayout.propTypes = propTypes;

export default GridLayout;
