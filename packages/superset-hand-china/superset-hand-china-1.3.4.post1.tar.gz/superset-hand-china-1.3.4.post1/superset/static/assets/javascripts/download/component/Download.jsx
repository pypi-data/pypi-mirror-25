import React from 'react';
import { render } from 'react-dom';
import PropTypes from 'prop-types';
import Filter from './Filter';
import { t } from '../../locales';
import Tables from './Tabs';
import { Radio, Button } from 'antd';

const RadioButton = Radio.Button;
const RadioGroup = Radio.Group;
const $ = window.$ = require('jquery');

const propTypes = {
  dashboard: PropTypes.object.isRequired,
}

let filters = {};
export default class Download extends React.Component {
  constructor(porps) {
    super(porps);
    this.state = {
      sliceId: 0,
      groupby: [],
      metrcis: [],
      columns: [],
      data: [],
      activeKey: '1',
    }; 
  }

  componentWillMount() {
    // init sliceId
    for(let i = 0; i < this.props.dashboard.slices.length; i ++ ) {
      const slice = this.props.dashboard.slices[i];
      if (slice.form_data.viz_type !== 'filter_box'
          && slice.form_data.viz_type !== 'filter_box_tree'
          && slice.form_data.viz_type !== 'filter_box_combination') {
        this.props.dashboard.getSliceObjects().forEach(s => {
          if (s.formData.slice_id === slice.slice_id) {
            this.setState({
              sliceId: slice.slice_id,
              groupby: s.data.form_data.groupby,
              metrics: s.data.form_data.metrics,
            });
          }
        });
        break;
      }
    }

    // init filters
    this.props.dashboard.slices.forEach(s => {
      filters[s.slice_id] = {};
    });
  }

  onChange(e) {
    this.props.dashboard.getSliceObjects().forEach(s => {
      if (s.formData.slice_id === e.target.value) {
        this.setState({
          sliceId: e.target.value,
          groupby: s.data.form_data.groupby,
          metrics: s.data.form_data.metrics,
          activeKey: '1',
        });
      }
    });
  }

  changeGroupby(slice_id, vals) {
    filters[slice_id]['groupby'] = vals;
    this.setState({ groupby: vals });
  }

  changeMetrics(slice_id, vals) {
    // console.info(slice_id, vals);
    filters[slice_id]['metrics'] = vals;
    this.setState({ metrics: vals });
  }

  getSliceFilterUrl(row_limit) {
    let url;
    // get current tab slice
    this.props.dashboard.getSliceObjects().forEach(s => {
      if (s.formData.slice_id === this.state.sliceId) {
        if (filters[this.state.sliceId] !== undefined) {
          // set new groupby and metric
          const newGroupby = filters[this.state.sliceId]['groupby'] !== undefined ? filters[this.state.sliceId]['groupby'] : [];
          const newMetrics = filters[this.state.sliceId]['metrics'] !== undefined ? filters[this.state.sliceId]['metrics'] : [];
          // console.info(newGroupby, newMetrics);
          s.formData.groupby = newGroupby.length > 0 ? newGroupby : s.data.form_data.groupby;
          s.formData.metrcis = newMetrics.length > 0 ? newMetrics : s.data.form_data.metrcis;
          s.formData.row_limit = row_limit === null ? s.data.form_data.row_limit : row_limit;
          // set orderby
          const newOrder = [];
          s.data.form_data.order_by_cols.forEach(order => {
            const field = order.substring(2, order.indexOf(',') - 1);
            if(s.formData.groupby.indexOf(field) !== -1) {
              // groupby contain this order field
              newOrder.push(order);
            }
          });
          s.formData.order_by_cols = newOrder;
        }
        url = s.jsonEndpoint(s.formData);
      }
    });
    return url;
  }

  download() {
    location.href = this.getSliceFilterUrl(null) + '&excel=true';
  }

  queryResult() {
    const _this = this;
    const columns = this.state.groupby.concat(this.state.metrics);
    const query_json_url = this.getSliceFilterUrl(100) + '&json=true';
    const export_json_url = this.getSliceFilterUrl(null) + '&json=true';
    $.ajax({
      type: 'get',
      url: query_json_url, 
      success: function(result) {
        // get query result
        _this.setState({
          columns: columns.map(c => ({'title': c, 'dataIndex': c, 'key': c})),
          data: result.data.records.slice(0, 100),
          activeKey: '1',
        });
      
        // add to query history
        $.ajax({
          type: 'post',
          url: '/hand/addQueryHistory',
          data: {
            slice_id: _this.state.sliceId,
            query_json_url: query_json_url,
            export_json_url: export_json_url,
            sql: result.query,
            columns: columns.join(',')
          },
          success: function(data) {
            console.info(data);
          },
          error: function(xhr, error) {
            alert(xhr.responseText);
          }
        });
      },
      error: function(xhr, error) {
        alert(xhr.responseText);
      }
    });
  }

  viewQuery(query_json_url, columns) {
    const _this = this;
    $.get(query_json_url, function(result) {
      _this.setState({
        columns: columns.split(',').map(c => ({'title': c, 'dataIndex': c, 'key': c})),
        data: result.data.records.slice(0, 100),
        activeKey: '1',
      });
    });
  }

  changeActiveKey(key) {
    this.setState({ activeKey: key });
  }

  render() {
    // console.info(this.props.dashboard);
    const radioOptions = [];
    this.props.dashboard.slices.forEach((slice, index) => {
      if (slice.form_data.viz_type !== 'filter_box'
          && slice.form_data.viz_type !== 'filter_box_tree'
          && slice.form_data.viz_type !== 'filter_box_combination') {
        radioOptions.push(
          <RadioButton value={slice.slice_id}>{slice.slice_name}</RadioButton>
        )
      }
    });

    const slicesDiv = [];
    this.props.dashboard.slices.forEach(s => {
      slicesDiv.push(
        <div id={"con_" + s.slice_id} key={"key_" + s.slice_id}></div>
      )
    });

    return (
      <div style={{ padding: '10 30 0 30' }}>
        <div style={{ padding: '20 0 10 15', background: '#eee', marginLeft: 15 }}>
          <div>
            <label style={{ width: 70 }}>{t('Slices:')}</label>
            <RadioGroup
              defaultValue={this.state.sliceId}
              onChange={this.onChange.bind(this)}
            >
              {radioOptions}
            </RadioGroup>
          </div>
          <Filter
            slice_id={this.state.sliceId}
            dashboard={this.props.dashboard}
            groupby={this.state.groupby}
            metrics={this.state.metrics}
            changeGroupby={this.changeGroupby.bind(this)}
            changeMetrics={this.changeMetrics.bind(this)}
          />
        </div>
        <div style={{ marginTop: 15 }}>
          {slicesDiv}
        </div>
        <Button
          style={{ margin: '10 0 10 15', float: 'right' }}
          type="primary"
          onClick={this.download.bind(this)}
        >
          {t('Download')}
        </Button>
        <Button
          style={{ margin: '10 0 10 15', float: 'right' }}
          type="primary"
          onClick={this.queryResult.bind(this)}
        >
          {t('Query Result')}
        </Button>
        <Tables
          activeKey={this.state.activeKey}
          changeActiveKey={this.changeActiveKey.bind(this)}
          sliceId={this.state.sliceId}
          viewQuery={this.viewQuery.bind(this)}
          columns={this.state.columns}
          data={this.state.data}
        />
    </div>
    );
  }
}

Download.propTypes = propTypes;
