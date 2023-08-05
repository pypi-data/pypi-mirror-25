import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';
import { Button, Row, Col } from 'react-bootstrap';
import { t } from '../../../../../locales';

const $ = window.$ = require('jquery');

const propTypes = {
  changeStack: PropTypes.func,
  removeStack: PropTypes.func,
  stack: PropTypes.object.isRequired,
  datasource: PropTypes.object,
  having: PropTypes.bool,
};

const defaultProps = {
  changeStack: () => {},
  removeStack: () => {},
  datasource: null,
};

export default class Stack extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }
  changeName(event) {
    this.props.changeStack('name', event.target.value);
  }
  changeMetrics(value) {
    this.props.changeStack('metrics', value);
  }
  removeStack(stack) {
    this.props.removeStack(stack);
  }
  render() {
    const datasource = this.props.datasource;
    const stack = this.props.stack;
    let colChoices;
    if (datasource) {
      colChoices = datasource.metrics_combo.map(c => ({ value: c[0], label: c[1] }));
    }
    return (
      <div>
        <Row className="space-1">
          <Col md={4}>
            <input
              style={{width: '100%', height: '28px'}}
              type="text"
              placeholder={t('Bar Name')}
              value={stack.name}
              onChange={this.changeName.bind(this)}
            />
          </Col>
          <Col md={6}>
            <Select
              multi
              simpleValue
              placeholder={t('Select Metrics')}
              options={colChoices}
              clearable={false}
              value={stack.metrics}
              onChange={this.changeMetrics.bind(this)}
            />
          </Col>
          <Col md={2}>
            <Button
              id="remove-button"
              bsSize="small"
              onClick={this.removeStack.bind(this)}
            >
              <i className="fa fa-minus" />
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

Stack.propTypes = propTypes;
Stack.defaultProps = defaultProps;
