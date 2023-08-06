import React from 'react';
import PropTypes from 'prop-types';
import { Button, Row, Col } from 'react-bootstrap';
import { t } from '../../../../../locales';
import Stack from './Stack';

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

export default class StackControl extends React.Component {
  addStack() {
    const newStacks = Object.assign([], this.props.value);
    newStacks.push({
      name: '',
      metrics: '',
    });
    this.props.onChange(newStacks);
  }
  changeStack(index, control, value) {
    const newStacks = Object.assign([], this.props.value);
    const modifiedStack = Object.assign({}, newStacks[index]);
    if (typeof control === 'string') {
      modifiedStack[control] = value;
    } else {
      control.forEach((c, i) => {
        modifiedStack[c] = value[i];
      });
    }
    newStacks.splice(index, 1, modifiedStack);
    this.props.onChange(newStacks);
  }
  removeStack(index) {
    this.props.onChange(this.props.value.filter((f, i) => i !== index));
  }
  render() {
    const stacks = this.props.value.map((stack, i) => (
      <div key={i}>
        <Stack
          stack={stack}
          datasource={this.props.datasource}
          removeStack={this.removeStack.bind(this, i)}
          changeStack={this.changeStack.bind(this, i)}
        />
      </div>
    ));
    return (
      <div>
        {stacks}
        <Row className="space-2">
          <Col md={2}>
            <Button
              id="add-button"
              bsSize="sm"
              onClick={this.addStack.bind(this)}
            >
              <i className="fa fa-plus" /> &nbsp; {t('Add Stack')}
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

StackControl.propTypes = propTypes;
StackControl.defaultProps = defaultProps;
