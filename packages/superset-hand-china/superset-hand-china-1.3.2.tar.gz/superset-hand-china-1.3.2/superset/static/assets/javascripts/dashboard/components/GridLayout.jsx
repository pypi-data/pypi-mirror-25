import React from 'react';
import PropTypes from 'prop-types';
import { Responsive, WidthProvider } from 'react-grid-layout';
import $ from 'jquery';

// import SliceCell from './SliceCell';
import SliceCell from '../hand/SliceCell';
import { getExploreUrl } from '../../explore/exploreUtils';

require('react-grid-layout/css/styles.css');
require('react-resizable/css/styles.css');

const ResponsiveReactGridLayout = WidthProvider(Responsive);

const propTypes = {
  dashboard: PropTypes.object.isRequired,
};

class GridLayout extends React.Component {
  componentWillMount() {
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
        };
      }

      layout.push({
        i: String(sliceId),
        x: pos.col - 1,
        y: pos.row,
        w: pos.size_x,
        minW: 2,
        minH: 2,
        h: pos.size_y,
      });
    });

    this.setState({
      layout,
      slices: this.props.dashboard.slices,
    });
  }

  onResizeStop(layout, oldItem, newItem) {
    const newSlice = this.props.dashboard.getSlice(newItem.i);
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
    }));
  }

  getCsv(slice) {
    let csv_endpoint = getExploreUrl(slice.form_data, 'csv');
    const params = JSON.parse(this.getQueryString("preselect_filters"));
    var filter = {};
    for(var k in params) {
      for(var m in params[k]) {
        filter[m] = params[k][m];
      }
    }
    var filterStr = JSON.stringify(filter);
    location.href = csv_endpoint + '&extra_filters=' + filterStr;
  }

  // get url param
  getQueryString(name) {
    const reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    const r = window.location.search.substr(1).match(reg);
    if (r != null) return unescape(decodeURI(r[2]));
    return null;
  }



  render() {
    return (
      <ResponsiveReactGridLayout
        className="layout"
        layouts={{ lg: this.state.layout }}
        onResizeStop={this.onResizeStop.bind(this)}
        onDragStop={this.onDragStop.bind(this)}
        cols={{ lg: 24, md: 10, sm: 8, xs: 6, xxs: 2 }}
        rowHeight={10}
        autoSize
        margin={[20, 20]}
        useCSSTransforms
        draggableHandle=".drag"
      >
        {this.state.slices.map((slice,index) => (
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
              getCsv={this.getCsv.bind(this, slice)}
              index={index}
            />
          </div>
        ))}
      </ResponsiveReactGridLayout>
    );
  }
}

GridLayout.propTypes = propTypes;

export default GridLayout;
