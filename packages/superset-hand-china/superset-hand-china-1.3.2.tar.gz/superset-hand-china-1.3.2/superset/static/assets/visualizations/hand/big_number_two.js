// JS
import d3 from 'd3';
import React from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';
import Select from 'react-select';
import { Button } from 'react-bootstrap';

import '../../stylesheets/react-select/select.less';
import { TIME_CHOICES } from '../constants';
require('./big_number_two.css');
require('./font-awesome.min.css');


// antd
import { Radio, Checkbox, DatePicker } from 'antd';
const RadioGroup = Radio.Group;
const CheckboxGroup = Checkbox.Group;
const { RangePicker } = DatePicker;
var moment = require('moment');

const propTypes = {
  formData: PropTypes.object.isRequired,
  payload: PropTypes.object.isRequired,
}

const format = function (value, format) {
  if (format === undefined || format === '') {
    return value;
  }
  const expr = format.substring(format.indexOf('{') + 1, format.indexOf('}'));
  return format.substring(0, format.indexOf('{')) + eval(expr) + format.substring(format.indexOf('}') + 1);
}


class BigNumberTwo extends React.Component {
  constructor(props) {
    super(props);
  }


  render() {
    const fd = this.props.formData;
    const dt = this.props.payload.data;
    const numberValue = format(dt.records[0][fd.metric], fd.format);
    const percentage = ((dt.records[0][fd.metrics_one] / dt.records[0][fd.metrics_two])*100).toFixed(2) + '%';
    return (
      <div className="dashboard-stat2">
        <div className="display1">
          <div className="number1">
            <h3 className="font-green-sharp1">
              <span data-counter="counterup1" data-value="7800" style={{ color: fd.fontColor, fontSize: fd.big_number_fontSize + 'px' }}>{numberValue}</span>
            </h3>
            <small>{fd.number_description}</small>
          </div>
          <div className="icon1">
            <i className={'fa ' + fd.icone_select}></i>
          </div>
        </div>
        <div className="progress-info1">
          <div className="progress1">
            <span style={{width: percentage,backgroundColor: fd.fontColor,}} className="progress-bar1 progress-bar-success1">
            </span>
          </div>
          <div className="status1">
            <div className="status-title1"> {fd.progress_description} </div>
            <div className="status-number1"> {percentage} </div>
          </div>
        </div>
      </div>
    );
  }
}

BigNumberTwo.propTypes = propTypes;

function bigNumberTwo(slice, payload, theme) {
  const fd = slice.formData;
  const height = slice.height();
  const width = slice.width();
  ReactDOM.render(
    <BigNumberTwo
      slice={slice}
      formData={fd}
      payload={payload}
      sliceHeight={height}
      sliceWidthwidth={width}
    />,
    document.getElementById(slice.containerId),
  );
}

module.exports = bigNumberTwo;
