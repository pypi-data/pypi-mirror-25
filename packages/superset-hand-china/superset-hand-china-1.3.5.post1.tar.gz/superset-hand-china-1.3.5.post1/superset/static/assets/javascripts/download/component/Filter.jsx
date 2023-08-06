import React from 'react';
import { render } from 'react-dom';
import PropTypes from 'prop-types';
import { Button } from 'react-bootstrap';
import { Select } from 'antd';

import { t } from '../../locales';

const Option = Select.Option;

const propTypes = {
  dashboard: PropTypes.object.isRequired,
  slice_id: PropTypes.number.isRequired,
  groupby: PropTypes.array.isRequired,
  metrics: PropTypes.array.isRequired,
  changeGroupby: PropTypes.func.isRequired,
  changeMetrics: PropTypes.func.isRequired,
}

export default class Filter extends React.Component {
  constructor(props) {
    super(props);
  }

  changeGroupby(vals) {
    this.props.changeGroupby(this.props.slice_id, vals);
  }

  changeMetrics(vals) {
    this.props.changeMetrics(this.props.slice_id, vals);
  }

  render() {
    let groupby = [];
    let metrics = [];
    // get current tab slice's all columns
    this.props.dashboard.getSliceObjects().forEach(s => {
      if (s.formData.slice_id === this.props.slice_id) {
        groupby = s.datasource.gb_cols;
        metrics = s.datasource.metrics_combo;
      }
    });
    const groupbyChoices = groupby.map(col => <Option key={col[0]}>{col[1]}</Option>);
    const metricChoices = metrics.map(col => <Option key={col[0]}>{col[1]}</Option>);

    return (
      <div style={{ marginTop: 15, marginBottom: 10 }}>
        <div>
          <label style={{ width: 70 }}>{t('groupby:')}</label>
          <Select
            mode="multiple"
            style={{ width: '80%' }}
            placeholder={t('Select groupby')}
            allowClear
            value={this.props.groupby}
            onChange={this.changeGroupby.bind(this)}
          >
            {groupbyChoices}
          </Select>
        </div>
        <div>
          <label style={{ marginTop: 15, width: 70 }}>{t('metrics:')}</label>
          <Select
            mode="multiple"
            style={{ width: '80%' }}
            placeholder={t('Select metrics')}
            allowClear
            value={this.props.metrics}
            onChange={this.changeMetrics.bind(this)}
          >
            {metricChoices}
          </Select>
        </div>
      </div>
    )
  }
}

Filter.propTypes = propTypes;