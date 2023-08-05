// JS
import d3 from 'd3';
import React from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';
// import Select from 'react-select';

import MultiSelect from '@khanacademy/react-multi-select';
import { t } from '../../javascripts/locales';
import '../../stylesheets/react-select/select.less';
import { TIME_CHOICES } from '../constants';
import '../filter_box.css';

// antd
import { Radio, Checkbox, DatePicker, Button, Select } from 'antd';

const RadioGroup = Radio.Group;
const CheckboxGroup = Checkbox.Group;
const { RangePicker } = DatePicker;
const Option = Select.Option;

var moment = require('moment');

const propTypes = {
  origSelectedValues: PropTypes.object,
  instantFiltering: PropTypes.bool,
  filtersChoices: PropTypes.object,
  onChange: PropTypes.func,
  showDateFilter: PropTypes.bool,
  datasource: PropTypes.object.isRequired,
  formData: PropTypes.object.isRequired,
  is_child: PropTypes.bool.isRequired,
};

const defaultProps = {
  origSelectedValues: {},
  onChange: () => {},
  showDateFilter: false,
  instantFiltering: true,
};

class FilterBox extends React.Component {
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
  changeSlices(filter, vals) {
    if (this.props.is_child) {
      this.props.onChange(filter, vals, false, false);
    } else {
      this.props.onChange(filter, vals, false, this.props.instantFiltering);
    }
  }
  changeFilter(filter, options) {
    let vals = null;
    if (options) {
      if (Array.isArray(options)) {
        vals = options.map(opt => opt.value);
      } else {
        vals = options.value;
      }
    }
    const selectedValues = Object.assign({}, this.state.selectedValues);
    let array = [];
    if (!(vals instanceof Array) && vals !== null) {
      vals = [vals];
    }
    selectedValues[filter] = vals;
    this.setState({ selectedValues, hasChanged: true });
    // this.props.onChange(filter, vals, false, this.props.instantFiltering);
    this.changeSlices(filter, vals);
  }
  changeRadio(filter, event) {
    const selectedValues = Object.assign({}, this.state.selectedValues);
    let val = event.target.value;
    if (val !== null) {
      val = [val];
    }
    selectedValues[filter] = val;
    this.setState({ selectedValues, hasChanged: true });
    // this.props.onChange(filter, val, false, this.props.instantFiltering);
    this.changeSlices(filter, val);
  }
  changeCheckBox(filter, vals) {
    const selectedValues = Object.assign({}, this.state.selectedValues);
    selectedValues[filter] = vals;
    this.setState({ selectedValues, hasChanged: true });
    // this.props.onChange(filter, vals, false, this.props.instantFiltering);
    this.changeSlices(filter, vals);
  }
  changeSelectBox(filter, vals) {
    const selectedValues = Object.assign({}, this.state.selectedValues);
    // selectedValues[filter] = vals === null ? [] : vals;
    selectedValues[filter] = vals;
    this.setState({ selectedValues, hasChanged: true });
    // this.props.onChange(filter, vals, false, this.props.instantFiltering);
    this.changeSlices(filter, vals);
  }
  changeSingleSelect(filter, vals) {
    const selectedValues = Object.assign({}, this.state.selectedValues);
    if (!(vals instanceof Array) && vals !== undefined && vals !== null) {
      vals = [vals];
    }
    if(vals === undefined || vals === null) {
      vals = [];
    }
    // selectedValues[filter] = vals === undefined ? [] : vals;
    selectedValues[filter] = vals;
    this.setState({ selectedValues, hasChanged: true });
    // this.props.onChange(filter, vals, false, this.props.instantFiltering);
    this.changeSlices(filter, vals);
  }
  changeDate(vals) {
    const selectedValues = Object.assign({}, this.state.selectedValues);
    let time = new Date();
    let dates = ['1900-01-01', (time.getFullYear() + '-' + (time.getMonth() + 1) + '-' + time.getDate())];
    // clear date
    if (vals.length > 0) {
      dates = vals.map(val => (val.format("YYYY/MM/DD")));
    }
    selectedValues['__from'] = dates[0];
    selectedValues['__to'] = dates[1];
    this.changeSlices('__from', dates[0]);
    this.changeSlices('__to', dates[1]);
    this.setState({ selectedValues, hasChanged: true });
  }
  // select(filter, multi, width, data) {
  //   const maxes = {};
  //   maxes[filter] = d3.max(data, function (d) {
  //     return d.metric;
  //   });
  //   return (
  //     <div key={filter} className="m-b-5" 
  //       style={{ width: width==='' ? '100%' : width, float: 'left', fontSize: '12px' }}
  //     >
  //       <div style={{ marginLeft: 15 }}>
  //         {this.props.datasource.verbose_map[filter] || filter}
  //         <Select.Creatable
  //           placeholder={`Select [${filter}]`}
  //           key={filter}
  //           multi={multi}
  //           value={multi === true ? this.state.selectedValues[filter] : 
  //             ((this.state.selectedValues[filter] === undefined || this.state.selectedValues[filter] == null)
  //               ? undefined : this.state.selectedValues[filter][0]) }
  //           options={data.map((opt) => {
  //             // const perc = Math.round((opt.metric / maxes[opt.filter]) * 100);
  //             // const backgroundImage = (
  //             //  'linear-gradient(to right, lightgrey, ' +
  //             //  `lightgrey ${perc}%, rgba(0,0,0,0) ${perc}%`
  //             // );
  //             const style = {
  //               // backgroundImage,
  //               padding: '2px 5px',
  //             };
  //             return { value: opt.id, label: opt.id, style };
  //           })}
  //           onChange={this.changeFilter.bind(this, filter)}
  //         />
  //       </div>
  //     </div>
  //   );
  // }
  radio(filter, width, data) {
    return (
      <div key={filter} className="m-b-5" 
        style={{ width: width==='' ? '100%' : width, float: 'left', fontSize: 12 }}
      >
        <div style={{ marginLeft: 15 }}>
          <p>{this.props.datasource.verbose_map[filter] || filter}</p>
          <RadioGroup
            disabled={this.state.filterFrozen}
            options={data.concat({id: null, text: 'all'}).map(d => ({label: d.text, value: d.id}))}
            onChange={this.changeRadio.bind(this, filter)}
            value={(this.state.selectedValues[filter] === '' || this.state.selectedValues[filter] == null)
              ? null : this.state.selectedValues[filter][0]}
          />
        </div>
      </div>
    );
  }
  checkbox(filter, width, data) {
    return (
      <div key={filter} className="m-b-5" 
        style={{ width: width==='' ? '100%' : width, float: 'left', fontSize: '12px' }}
      >
        <div style={{ marginLeft: 15 }}>
          <p>{this.props.datasource.verbose_map[filter] || filter}</p>
          <CheckboxGroup
            disabled={this.state.filterFrozen}
            options={data.map(d => ({label: d.id, value: d.id}))}
            onChange={this.changeCheckBox.bind(this, filter)}
            defaultValue={this.state.selectedValues[filter]}
          />
        </div>
      </div>
    )
  }
  selectBox(filter, width, data) {
    return (
      <div key={filter} className="m-b-5" 
        style={{ width: width==='' ? '100%' : width, float: 'left', fontSize: '12px' }}
      >
        <div style={{ marginLeft: 15 }} id="selectBox">
          <p>{this.props.datasource.verbose_map[filter] || filter}</p>
            <MultiSelect
              disabled={this.state.filterFrozen}
              options={data.map(d => ({label: d.id, value: d.id}))}
              onSelectedChanged={this.changeSelectBox.bind(this, filter)}
              selected={this.state.selectedValues[filter] === undefined ? [] : this.state.selectedValues[filter]}
              valueRenderer={filterValueRenderer}
              selectAllLabel={`Select All [${filter}]`}
            />
        </div>
      </div>
    )
  }
  singleSelect(filter, width, data) {
    let selectValue = [];
    for (let i = 0; i < data.length; i++) {
      if(data[i].id !== null && data[i].id !== ''){
        selectValue.push(<Option key={data[i].id}>{data[i].id}</Option>);
      }
    }
    return (
      <div key={filter} className="m-b-5" 
        style={{ width: width==='' ? '100%' : width, float: 'left', fontSize: '12px' }}
      >
        <div style={{ marginLeft: 15 }}>
          {this.props.datasource.verbose_map[filter] || filter}
          <br />
          <Select
            disabled={this.state.filterFrozen}
            showSearch
            allowClear
            optionFilterProp="children"
            defaultValue={this.state.selectedValues[filter]}
            placeholder={'Please Select'}
            style={{ width: '100%' }}
            onChange={this.changeSingleSelect.bind(this, filter)}
            filterOption={(input, option) => option.props.children.toLowerCase().indexOf(input.toLowerCase()) >= 0}
          >
            {selectValue}
          </Select>
        </div>
      </div>
    );
  }

  render() {
    let dateFilter;
    if (this.props.showDateFilter) {
      let dates = [this.state.selectedValues['__from'], this.state.selectedValues['__to']];
      if (this.state.selectedValues['__from'] === undefined && this.state.selectedValues['__to'] === undefined) {
        let time = new Date();
        dates = ['1900-01-01', (time.getFullYear() + '-' + (time.getMonth() + 1) + '-' + time.getDate())];
      }
      dateFilter = (
        <div key='date' className="m-b-5" 
          style={{ float: 'left', fontSize: 12 }}
        >
          <div style={{ marginLeft: 15 }}>
            <p>{this.props.formData.granularity_sqla === null ? "date filter" : this.props.formData.granularity_sqla}</p>
            <RangePicker
              size="default"
              allowClear
              value={[moment(dates[0]), moment(dates[1])]}
              onChange={this.changeDate.bind(this)}
            />
          </div>
        </div>
      );
      // dateFilter = ['__from', '__to'].map((field) => {
      //   const val = this.state.selectedValues[field];
      //   const choices = TIME_CHOICES.slice();
      //   if (!choices.includes(val)) {
      //     choices.push(val);
      //   }
      //   const options = choices.map(s => ({ value: s, label: s }));
      //   return (
      //     <div className="m-b-5" key={field}>
      //       {field.replace('__', '')}
      //       <Select.Creatable
      //         options={options}
      //         value={this.state.selectedValues[field]}
      //         onChange={this.changeFilter.bind(this, field)}
      //       />
      //     </div>
      //   );
      // });
    }

    // filters
    const filters = Object.keys(this.props.filtersChoices).map((filter) => {
      const data = this.props.filtersChoices[filter];
      for (let i = 0; i < this.props.formData.filterSetting.length; i++) {
        const f = this.props.formData.filterSetting[i];
        if (f.metric === filter) {
          if (f.type === 'single select') {
            return this.singleSelect(filter, f.width, data);
            // return this.select(filter, false, f.width, data);
          } else if (f.type === 'multi select') {
            return this.selectBox(filter, f.width, data);
            // return this.select(filter, true, f.width, data);
          } else if (f.type === 'radio') {
            return this.radio(filter, f.width, data);
          } else {
            // checkbox
            return this.checkbox(filter, f.width, data);
          }
        }
      }
      // has no setting, default multi select
      return this.selectBox(filter, '100%', data);
      // return this.select(filter, true, '100%', data);
      
    });
    
    return (
      <div>
        {dateFilter}
        {filters}
        {!this.props.instantFiltering && !this.props.is_child &&
          <div>
            <Button
              style={{ marginLeft: 15, width: 65, height: 25, marginTop: 20, float:'left'}}
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
FilterBox.propTypes = propTypes;
FilterBox.defaultProps = defaultProps;

function filterBox(slice, payload) {
  const d3token = d3.select(slice.selector);
  d3token.selectAll('*').remove();

  // filter box should ignore the dashboard's filters
  // const url = slice.jsonEndpoint({ extraFilters: false });
  const fd = slice.formData;
  const is_child = fd.is_child ? true : false;
  const filtersChoices = {};
  // Making sure the ordering of the fields matches the setting in the
  // dropdown as it may have been shuffled while serialized to json
  fd.groupby.forEach((f) => {
    filtersChoices[f] = payload.data[f];
  });
  ReactDOM.render(
    <FilterBox
      filtersChoices={filtersChoices}
      onChange={slice.addFilter}
      showDateFilter={fd.date_filter}
      datasource={slice.datasource}
      origSelectedValues={slice.getFilters() || {}}
      instantFiltering={fd.instant_filtering}
      formData={fd}
      is_child={is_child}
    />,
    document.getElementById(slice.containerId),
  );
}

function filterValueRenderer(selected, options) {
  if (selected.length === 0) {
    return t('Please Select');
  }
  return selected.join(', ');
}

module.exports = filterBox;
