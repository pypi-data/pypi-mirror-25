// JS
import d3 from 'd3';
import React from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';
import Select from 'react-select';
import { Button } from 'react-bootstrap';

import '../../stylesheets/react-select/select.less';
import { TIME_CHOICES } from '../constants';
require('./big_number_three.css');
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


class BigNumberThree extends React.Component {
  constructor(props) {
    super(props);
  }


  render() {
    const fd = this.props.formData;
    const dt = this.props.payload.data;
    const numberValue = format(dt.records[0][fd.metric], fd.format);
    return (
      <div className="bigNumberThree">
        <div className="widget-thumb widget-bg-color-white margin-bottom-20 bordered">
          <h4 className="widget-thumb-heading">{fd.subheader}</h4>
          <div className="widget-thumb-wrap">
            <i className={'widget-thumb-icon ' + 'fa ' + fd.icone_select} style={{ background: fd.icon_color }}></i>
            <div className="widget-thumb-body">
              <span className="widget-thumb-subtitle">{fd.number_description}</span>
              <span className="widget-thumb-body-stat" data-counter="counterup" data-value="7,644" style={{ fontSize: fd.big_number_fontSize + 'px' }}>{numberValue}</span>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

BigNumberThree.propTypes = propTypes;

function bigNumberThree(slice, payload, theme) {
  const fd = slice.formData;
  const height = slice.height();
  const width = slice.width();
  ReactDOM.render(
    <BigNumberThree
      slice={slice}
      formData={fd}
      payload={payload}
      sliceHeight={height}
      sliceWidthwidth={width}
    />,
    document.getElementById(slice.containerId),
  );
}

module.exports = bigNumberThree;
