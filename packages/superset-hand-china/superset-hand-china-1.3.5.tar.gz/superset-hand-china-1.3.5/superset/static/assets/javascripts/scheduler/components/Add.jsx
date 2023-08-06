import React from 'react';
import { SchedulerForm } from './Scheduler';
import { ConditionForm } from './Condition';
const $ = window.$ = require('jquery');

export default class Add extends React.PureComponent  {
  constructor(props) {
    super(props);
    this.state = {
      disabled: false,
      disabled2: true,
      schedulerId: null,
    }
  }

  changeDisabled(schedulerId) {
    this.setState({
      disabled: true,
      disabled2: false,
      schedulerId: schedulerId
    });
  }

  render() {
    // console.info(this.props.form_data)
    return (
      <div style={{ width: '80%', overflow: 'hidden', marginLeft: 20 }}>
        <div style= {{ width: '50%', float: 'left' }}>
          <SchedulerForm
            disabled={this.state.disabled}
            form_data={this.props.form_data}
            changeDisabled={this.changeDisabled.bind(this)}
            type="insert"
          />
        </div>
        <div style= {{ width: '50%', float: 'left' }}>
          <ConditionForm
            form_data={this.props.form_data}
            disabled={this.state.disabled2}
            schedulerId={this.state.schedulerId}
            type="insert"
          />
        </div>
      </div>
    );
  }
}

