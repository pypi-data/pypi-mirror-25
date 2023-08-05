// JS
import d3 from 'd3';
import React from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';
import Select from 'react-select';
import { Button } from 'react-bootstrap';

import '../../stylesheets/react-select/select.less';
import { TIME_CHOICES } from '../constants';
require('./big_number.css');
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


class BigNumber extends React.Component {
  constructor(props) {
    super(props);
  }


  render() {
    const fd = this.props.formData;
    const dt = this.props.payload.data;
    const numberValue = format(dt.records[0][fd.metric], fd.format);
    return (
      <div className="dashboard-stat" style={{ backgroundColor: fd.body_color }}>
        <a className="more" href="javascript:;" style={{ backgroundColor: fd.head_color, fontSize: fd.titleSize + 'px' }}> {fd.subheader}
          <i className="m-icon-swapright m-icon-white"></i>
        </a>
        <div className="visual">
          <i className={'fa ' + fd.icone_select}></i>
        </div>
        <div className="details">
          <div className="number" style={{ fontSize: fd.big_number_fontSize + 'px' }}>
            <span data-counter="counterup" data-value="1349">{numberValue}</span>
          </div>
        </div>
      </div>
    );
  }
}

BigNumber.propTypes = propTypes;

function bigNumber(slice, payload,theme) {
  const fd = slice.formData;
  const height = slice.height();
  const width = slice.width();
  ReactDOM.render(
    <BigNumber
      slice={slice}
      formData={fd}
      payload={payload}
      sliceHeight={height}
      sliceWidthwidth={width}
    />,
    document.getElementById(slice.containerId),
  );
}

module.exports = bigNumber;
