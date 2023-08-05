import React from 'react';
import PropTypes from 'prop-types'
import { slugify } from '../../../../modules/utils';
import ControlHeader from '../../ControlHeader';
var moment = require('moment');

import { DatePicker } from 'antd';
const { MonthPicker, RangePicker } = DatePicker;

const propTypes = {
  name: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number, PropTypes.array]),
  label: PropTypes.string,
  description: PropTypes.string,
  onChange: PropTypes.func,
};

const defaultProps = {
  value: '',
  label: null,
  description: null,
  onChange: () => {},
};

export default class DatePickerControl extends React.Component {
  constructor(props) {
    super(props);
    let date = null;
    // date = this.props.value ? this.props.value : this.props.defaultValue;
    date = this.props.date;
    this.state = {
      selectedValue: date,
    };
  }

  changeDate(options) {
    let val = null;
    if (options !== null) {
      val = options.format("YYYY-MM-DD");
      
    } else {
      val = options;
    }
    this.props.onChange(val);
    this.setState({
      selectedValue: val
    });
   
  }

  render() {
    const momentValue = this.state.selectedValue === null ? null : moment(this.state.selectedValue);
  
    return (
      <div  id={`formControlsSelect-${slugify(this.props.label)}`}>
        <ControlHeader
          {...this.props}
        />
        <DatePicker
          style={{width: "100%"}}
          className="datePicker"
          selected={momentValue}
          onChange={ this.changeDate.bind(this) }
          format="YYYY-MM-DD"
          showMonthDropdown 
          showYearDropdown
          isClearable={true}
        />
      </div>
    );
  }
}

DatePickerControl.propTypes = propTypes;
DatePickerControl.defaultProps = defaultProps;