import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';

// antd
import { DatePicker } from 'antd';
const { RangePicker } = DatePicker;
var moment = require('moment');


const propTypes = {
  name: PropTypes.string,
  onChange: PropTypes.func,
  value: PropTypes.array,
  datasource: PropTypes.object,
};

const defaultProps = {
  onChange: () => {},
  value: [],
};

export default class DateValueControl extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      dates: this.props.value,
    };
  }

  changeDate(vals) {
    // console.info(vals)
    let time = new Date();
    let dates = ['1900-01-01', (time.getFullYear() + '-' + (time.getMonth() + 1) + '-' + time.getDate())];
    // clear date
    if (vals.length > 0) {
      dates = vals.map(val => (val.format("YYYY/MM/DD")));
    }
    this.setState({ dates: dates });
    this.props.onChange(dates);
  }

  render() {
    let dates = [this.state.dates[0], this.state.dates[1]];
    if (this.state.dates[0] === undefined && this.state.dates[1] === undefined) {
      let time = new Date();
      dates = ['1900-01-01', (time.getFullYear() + '-' + (time.getMonth() + 1) + '-' + time.getDate())];
    }
    return (
      <div key='date' className="m-b-5" 
        style={{ float: 'left', fontSize: 12 }}
      >
        <RangePicker
          size="default"
          allowClear
          value={[moment(dates[0]), moment(dates[1])]}
          onChange={this.changeDate.bind(this)}
        />
      </div>
    );
  }
}

DateValueControl.propTypes = propTypes;
DateValueControl.defaultProps = defaultProps;
