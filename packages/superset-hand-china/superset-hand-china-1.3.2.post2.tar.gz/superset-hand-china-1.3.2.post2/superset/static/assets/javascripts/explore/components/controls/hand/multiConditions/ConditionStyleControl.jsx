import React from 'react';
import PropTypes from 'prop-types';
import { Button, Row, Col } from 'react-bootstrap';
import { t } from '../../../../../locales';
import ConditionStyle from './ConditionStyle';

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

export default class ConditionStyleControl extends React.Component {
  addConditionStyle() {
    const newConditionStyles = Object.assign([], this.props.value);
    newConditionStyles.push({
      metric: '',
      expr: '',
      style: '',
      icon: '',
    });
    this.props.onChange(newConditionStyles);
  }
  changeConditionStyle(index, control, value) {
    const newConditionStyles = Object.assign([], this.props.value);
    const modifiedConditionStyle = Object.assign({}, newConditionStyles[index]);
    if (typeof control === 'string') {
      modifiedConditionStyle[control] = value;
    } else {
      control.forEach((c, i) => {
        modifiedConditionStyle[c] = value[i];
      });
    }
    newConditionStyles.splice(index, 1, modifiedConditionStyle);
    this.props.onChange(newConditionStyles);
  }
  removeConditionStyle(index) {
    this.props.onChange(this.props.value.filter((f, i) => i !== index));
  }
  render() {
    const conditionStyles = this.props.value.map((conditionStyle, i) => (
      <div key={i}>
        <ConditionStyle
          conditionStyle={conditionStyle}
          datasource={this.props.datasource}
          removeConditionStyle={this.removeConditionStyle.bind(this, i)}
          changeConditionStyle={this.changeConditionStyle.bind(this, i)}
        />
      </div>
    ));
    return (
      <div>
        {conditionStyles}
        <Row className="space-2">
          <Col md={2}>
            <Button
              id="add-button"
              bsSize="sm"
              onClick={this.addConditionStyle.bind(this)}
            >
              <i className="fa fa-plus" /> &nbsp; {t('Add ConditionStyle')}
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

ConditionStyleControl.propTypes = propTypes;
ConditionStyleControl.defaultProps = defaultProps;
