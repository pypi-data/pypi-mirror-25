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

class IconSelectControl extends React.Component {
  constructor(props) {
    super(props);
    let selectIcon = []
    for (let i = 0; i < this.props.form_data.icon_multi_select.length; i++) {
      selectIcon.push(this.props.form_data.icon_multi_select[i].value)
    }
    this.state = {
      value: selectIcon,
    }

  }
  changeIconControl(vals) {
    this.props.onChange(vals);
    this.setState({ value: vals });
  }
  query() {
    let query = [];
    let groupby_one = this.props.form_data.groupby_one;
    let datasource = this.props.form_data.datasource;
    // $.ajax({
    //   //要用post方式 
    //   async: false,
    //   type: "post",
    //   //方法所在页面和方法名
    //   url: "/hand/queryForFunnel",
    //   dataType: "json",
    //   data: {
    //     datasource: datasource,
    //     groupby: groupby_one
    //   },
    //   success: function (msg) {
    //     //返回的数据用data.d获取内容
    //     return query = msg
    //   },
    //   error: function (err) {
    //     return query = [];
    //   }
    // })
    query = "/static/assets/images/pictorial_bar/滴滴.png,/static/assets/images/pictorial_bar/京东.png,/static/assets/images/pictorial_bar/酒店.png";
    if (query.length != 0) {
      let que = query.split(",");
      $.unique(que);
      for (let i = 0; i < que.length; i++) {
        const key = que[i];
        let img = new Image();
        img.src = key;
        let pathArray = (que[i] + "").split("/");
        let description = pathArray[pathArray.length - 1].split(".")[0];
        const option = {
          label: <div style={{}}><img style={{ with: (30 * img.width) / img.height, height: 30 }} src={que[i]}></img><div style={{ float: 'right', textalign: 'center', paddingTop: 5 }}>{description}</div></div>,
          value: que[i],
        };
        opt.push(option);
      }
    }
  }
  componentWillMount() {
    this.query();
  }

  componentWillReceiveProps(nextProps) {
    let query = [];
    let groupby_one = this.props.form_data.groupby_one;
    let datasource = this.props.form_data.datasource;
    if (nextProps.form_data.groupby_one !== this.props.form_data.groupby_one) {
      groupby_one = nextProps.form_data.groupby_one;
      opt = [];
      // this.clearValue();
      this.changeIconControl([]);
      this.query();
    }
    if (nextProps.form_data.datasource !== this.props.form_data.datasource) {
      datasource = nextProps.form_data.datasource;
      groupby_one = nextProps.form_data.groupby_one;
      opt = [];
      // this.clearValue();
      this.changeIconControl([]);
      if (groupby_one) {
        this.query();
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
          className="iconSelect"
          multi={true}
          placeholder={t('Select')}
          options={opt}
          value={this.state.value}
          onChange={this.changeIconControl.bind(this)}
        />
      </div>
    );
  }
}

IconSelectControl.propTypes = propTypes;


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

export { IconSelectControl };
export default connect(mapStateToProps, mapDispatchToProps)(IconSelectControl);
