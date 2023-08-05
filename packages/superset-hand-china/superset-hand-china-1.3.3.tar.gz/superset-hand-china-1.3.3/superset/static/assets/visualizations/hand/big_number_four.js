// JS
import d3 from 'd3';
import React from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';
import Select from 'react-select';
import { Button } from 'react-bootstrap';

import '../../stylesheets/react-select/select.less';
import { TIME_CHOICES } from '../constants';
require('./big_number_four.css');

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


class BigNumberFour extends React.Component {
  constructor(props) {
    super(props);
  }


  render() {
    const fd = this.props.formData;
    const dt = this.props.payload.data;
    const numberValue = format(dt.records[0][fd.metric], fd.format);
    const labelContent = fd.label_content;
    let divPaddingTop = (this.props.sliceHeight - 25) / 2;
    let topPadding = fd.label_top_padding;
    if(labelContent != undefined && labelContent != ''){
      divPaddingTop = (this.props.sliceHeight - 75) / 2;
    }
    if(topPadding === undefined || topPadding === ''){
      topPadding = (Number(fd.big_number_four_fontSize) + Number(fd.label_size) - 60) / 2 < 0 ? 0:(Number(fd.big_number_four_fontSize) + Number(fd.label_size) - 60) / 2;
    }
    return (
      <div className="dashboard-stat1" style={{ backgroundColor: fd.background_color }}>
        <div className="details1">
          <div className="number1" style={{paddingTop: divPaddingTop}}>
            <div style={{fontSize: fd.big_number_four_fontSize + 'px', color: fd.font_color, fontWeight: fd.font_weight*100}}>
              {numberValue}
            </div>
            <div style={{paddingTop: topPadding, display:'block', fontSize: fd.label_size + 'px', color: fd.label_color, fontWeight: fd.label_weight*100 }}>
              {labelContent}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

BigNumberFour.propTypes = propTypes;

function bigNumberFour(slice, payload, theme) {
  const fd = slice.formData;
  const height = slice.height();
  const width = slice.width();
  ReactDOM.render(
    <BigNumberFour
      slice={slice}
      formData={fd}
      payload={payload}
      sliceHeight={height}
      sliceWidthwidth={width}
    />,
    document.getElementById(slice.containerId),
  );
}

module.exports = bigNumberFour;
