// JS
import d3 from 'd3';
import React from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';

import { t } from '../../javascripts/locales';
// antd
import { TreeSelect, Button } from 'antd';
import '../filter_box.css';

const propTypes = {
  origSelectedValues: PropTypes.object,
  instantFiltering: PropTypes.bool,
  onChange: PropTypes.func,
  datasource: PropTypes.object.isRequired,
  formData: PropTypes.object.isRequired,
  payload: PropTypes.object.isRequired,
  is_child: PropTypes.bool.isRequired,
};

const defaultProps = {
  origSelectedValues: {},
  onChange: () => {},
  showDateFilter: false,
  instantFiltering: true,
};

class FilterBoxTree extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedValues: props.origSelectedValues,
      hasChanged: false,
      filterFrozen: false,
    };
  }
  componentWillMount() {
    const reg = new RegExp('(^|&)frozenFilter=([^&]*)(&|$)', 'i');
    const r = window.location.search.substr(1).match(reg);
    if (r != null && unescape(r[2]) === 'true') {
      this.setState({ filterFrozen: true} );
    }
  }
  clickApply() {
    this.props.onChange(Object.keys(this.state.selectedValues)[0], [], true, true);
    this.setState({ hasChanged: false });
  }
  getData(fd, dt) {
    const datas = [];
    dt.forEach(d => {
      const cid = d[fd.child_id];
      const value = d[fd.child_name] + '__++' + cid + '__++';
      const pid = d[fd.parent_id];
      const label = d[fd.child_name];
      datas.push({cid: cid, value: value, pid: pid, label: label});
    });
    const treeData = this.getTreeData('0', datas);
    return treeData;
  }

  // let array to parent-children data
  getTreeData(value, datas) {
    if (value !== '0') {
      var children = [];
      for (var i = 0; i < datas.length; i++) {
        var d = datas[i];
        d.value = d.value.toString();
        d.cid = d.cid.toString();
        if(d.pid === null || d.pid === ''){
          d.pid = '0';
        } else {
          d.pid = d.pid.toString();
        }
        if (d.pid === value) {
          var node = {cid: d.cid, value: d.value, pid: d.pid, label: d.label};
          node.children = this.getTreeData(d.cid, datas);
          children.push(node);
        }
      }
      return children;
    }
    // pid == 0
    var nodes = [];
    for (var i = 0; i < datas.length; i++) {
      var d = datas[i];
      d.value = d.value.toString();
      d.cid = d.cid.toString();
      if(d.pid === null || d.pid === ''){
        d.pid = '0';
      } else {
        d.pid = d.pid.toString();
      }
      // d.pid = d.pid.toString();
      if (d.pid === '0') {
        var node = {cid: d.cid, value: d.value,pid: d.pid, label: d.label};
        node.children = this.getTreeData(d.cid, datas);
        nodes.push(node);
      }
    }
    return nodes;
  }
  onChange(filter, vals) {
    const selectedValues = Object.assign({}, this.state.selectedValues);
    if (!Array.isArray(vals)) {
      vals = vals === undefined ? [] : [vals];
    }
    selectedValues[filter] = vals;
    this.setState({ selectedValues, hasChanged: true });
    const valsIds = [];
    for(let i = 0; i < vals.length; i++){
      const valsId = vals[i].split('__++')[1];
      valsIds.push(valsId);
    }
    if (this.props.is_child) {
      this.props.onChange(filter, valsIds, false, false);
    } else {
      this.props.onChange(filter, valsIds, false, this.props.instantFiltering);
    }
  }
  render() {
    const fd = this.props.formData;
    const dt = this.props.payload.data.records;
    const treeData = this.getData(fd, dt);
    const name = fd.filter_name.split('-')[0];
    const field = fd.filter_name.split('-')[1];
    const selectVals = [];
    let marginTopSize = 0;
    if(fd.filter_name.length != 0){
        marginTopSize = 20;
    }
    if(Array.isArray(this.state.selectedValues[field]) && this.state.selectedValues[field] !== undefined){
      for(let m = 0; m < this.state.selectedValues[field].length; m++){
        selectVals.push(this.state.selectedValues[field][m]);
        dt.forEach(d => {
          if(this.state.selectedValues[field][m] === d[fd.child_id]){
            const value = d[fd.child_name] + '__++' + d[fd.child_id] + '__++';
            selectVals.push(value);
          }
        });
      }
    }
    return (
      <div>
        <div key={field} className="m-b-5" 
          style={{  width: fd.width === '' ? '100%' : fd.width, float: 'left', fontSize: 12 }}
        >
          <div style={{ marginLeft: 15 }}>
            <p>{name}</p>
            <TreeSelect
              disabled={this.state.filterFrozen}
              showSearch
              style={{ width: '100%' }}
              value={selectVals}
              multiple={fd.multi}
              treeCheckable={fd.multi}
              allowClear
              dropdownStyle={{ maxHeight: 400, overflow: 'auto' }}
              treeData={treeData}
              placeholder={t('Please Select')}
              treeDefaultExpandAll
              onChange={this.onChange.bind(this, field)}
            />
          </div>
        </div>
        {!this.props.instantFiltering && !this.props.is_child &&
          <div>
            <Button
              style={{ marginLeft: 15, width: 65, height:25, marginTop:marginTopSize, float:'left'}}
              type="primary"
              icon="search"
              size="small"
              onClick={this.clickApply.bind(this)}
              disabled={!this.state.hasChanged}
            >
              {t('Query')}
            </Button>
          </div>
        }
      </div>
    );
  }
}
FilterBoxTree.propTypes = propTypes;
FilterBoxTree.defaultProps = defaultProps;

function filterBoxTree(slice, payload) {
  const d3token = d3.select(slice.selector);
  d3token.selectAll('*').remove();

  const fd = slice.formData;
  const is_child = fd.is_child ? true : false;
  // console.info(is_child)
  ReactDOM.render(
    <FilterBoxTree
      onChange={slice.addFilter}
      datasource={slice.datasource}
      origSelectedValues={slice.getFilters() || {}}
      instantFiltering={fd.instant_filtering}
      formData={fd}
      payload={payload}
      is_child={is_child}
    />,
    document.getElementById(slice.containerId),
  );
}

module.exports = filterBoxTree;
