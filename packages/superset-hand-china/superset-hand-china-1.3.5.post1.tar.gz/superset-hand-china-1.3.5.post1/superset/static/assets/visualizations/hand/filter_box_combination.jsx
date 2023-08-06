// JS
import d3 from 'd3';
import React from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';

// antd
import { Button } from 'antd';

import $ from 'jquery';
import { t } from '../../javascripts/locales';
import {getInitialState, dashboardContainer} from './util.js';

import '../filter_box.css';

const superset = require('../../javascripts/modules/superset');

const propTypes = {
  origSelectedValues: PropTypes.object,
  onChange: PropTypes.func,
  datasource: PropTypes.object.isRequired,
  formData: PropTypes.object.isRequired,
  payload: PropTypes.object.isRequired,
};

const defaultProps = {
  origSelectedValues: {},
  onChange: () => {},
};

let slices = null;
let sliceCombination = null;
class FilterBoxCombination extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedValues: props.origSelectedValues,
      hasChanged: false,
    };
  }
  componentWillMount() {
    if (this.props.formData.filter_combination.length === 0) {
      slices = [];
    } else {
      const filteIds = this.props.formData.filter_combination.join(",");
      $.ajax({
        url: '/hand/getSliceData?sliceIds=' + filteIds,
        async: false,
        success: function(data) {
          slices = JSON.parse(data);
        }
      });
    }
  }
  loadByExplore() {
    let href = window.location.href;
    const link = href.substr(href.indexOf('/superset/') + 10, 10);
    if (link.startsWith('explore')) {
      return true;
    }
    return false;
  }
  componentDidMount() {
    // load by explore
    if (this.loadByExplore()) {
      let state = getInitialState(slices);
      let px = superset(state);
      const dashboard = dashboardContainer(state.dashboard, state.datasources, state.user_id, px);
      dashboard.init();
    }
  }
  clickApply() {
    this.props.onChange(Object.keys(this.state.selectedValues)[0], [], true, true);
    this.setState({ hasChanged: false });
  }
  render() {
    // load for explore
    const slicesDiv = [];
    if (this.loadByExplore()) {
      this.props.formData.filter_combination.forEach(f => {
        slicesDiv.push(
          <div id={"con_" + f} key={"key_" + f}></div>
        )
      });
    }
    return (
      <div>
        {slicesDiv}
        <div>
          <Button
            style={{ marginLeft: 15, width: 65, height:25 ,marginTop: 20, float:'left' }}
            type="primary"
            icon="search"
            size="small"
            onClick={this.clickApply.bind(this)}
          >
            {t('Query')}
          </Button>
        </div>
      </div>
    );
  }
}
FilterBoxCombination.propTypes = propTypes;
FilterBoxCombination.defaultProps = defaultProps;

function filterBoxCombination(slice, payload) {
  const d3token = d3.select(slice.selector);
  d3token.selectAll('*').remove();

  const fd = slice.formData;
  ReactDOM.render(
    <FilterBoxCombination
      onChange={slice.addFilter}
      datasource={slice.datasource}
      origSelectedValues={slice.getFilters() || {}}
      formData={fd}
      payload={payload}
      
    />,
    document.getElementById(slice.containerId),
  );
}

module.exports = filterBoxCombination;
