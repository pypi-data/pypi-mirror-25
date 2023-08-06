/* eslint camelcase: 0 */
import React from 'react';
import PropTypes from 'prop-types';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import Select from 'react-select';

import { t } from '../../../../locales';
import * as actions from '../../../actions/exploreActions';
import { getFormDataFromControls } from '../../../stores/store';
import ControlHeader from '../../ControlHeader';
const $ = window.$ = require('jquery');

const propTypes = {
  name: PropTypes.string,
  onChange: PropTypes.func,
  value: PropTypes.array,
  datasource: PropTypes.object,
  form_data: PropTypes.object
};
let opt = [];

class OrderSelectControl extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      value: this.props.form_data.order_type,
    }

  }
  changeOrderControl(vals) {
    this.props.onChange(vals);
    this.setState({ value: vals });
  }
  query(g) {
    let query = [];
    let groupby_one = this.props.form_data.groupby_one;
    let datasource = this.props.form_data.datasource;
    if (g !== '') {
      groupby_one = g;
    }
    $.ajax({
      //要用post方式 
      async: false,
      type: "post",
      //方法所在页面和方法名
      url: "/hand/queryForFunnel",
      dataType: "json",
      data: {
        datasource: datasource,
        groupby: groupby_one,
      },
      success: function (msg) {
        //返回的数据用data.d获取内容
        return query = msg
      },
      error: function (err) {
        return query.results = [];
      }
    })
    let que = query.results;
    if (que != undefined) {
      // let que = query.split(",");
      // $.unique(que);
      for (let i = 0; i < que.length; i++) {
        const key = que[i];
        const option = {
          label: que[i],
          value: que[i],
        };
        opt.push(option);
      }
    }

  }
  componentWillMount() {
    const g = '';
    this.query(g);
  }

  componentWillReceiveProps(nextProps) {
    let query = [];
    let groupby_one = this.props.form_data.groupby_one;
    let datasource = this.props.form_data.datasource;
    if (nextProps.form_data.groupby_one !== this.props.form_data.groupby_one) {
      groupby_one = nextProps.form_data.groupby_one;
      opt = [];
      // this.clearValue();
      this.changeOrderControl([]);
      this.query(groupby_one);
    }
    if (nextProps.form_data.datasource !== this.props.form_data.datasource) {
      datasource = nextProps.form_data.datasource;
      groupby_one = nextProps.form_data.groupby_one;
      opt = [];
      // this.clearValue();
      this.changeOrderControl([]);
      if (groupby_one) {
        const g = '';
        this.query(g);
      }
    }

  }
  render() {

    return (
      <div>
        {this.props.showHeader &&
          <ControlHeader
            {...this.props}
          />
        }
        <Select
          className="test"
          multi={true}
          placeholder={t('Select')}
          options={opt}
          value={this.state.value}
          onChange={this.changeOrderControl.bind(this)}
        />
      </div>
    );
  }
}

OrderSelectControl.propTypes = propTypes;


function mapStateToProps({ explore }) {
  const form_data = getFormDataFromControls(explore.controls);
  return {
    alert: explore.controlPanelAlert,
    isDatasourceMetaLoading: explore.isDatasourceMetaLoading,
    controls: explore.controls,
    exploreState: explore,
    datasource_type: explore.datasource_type,
    form_data
  };
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(actions, dispatch),
  };
}

export { OrderSelectControl };
export default connect(mapStateToProps, mapDispatchToProps)(OrderSelectControl);
