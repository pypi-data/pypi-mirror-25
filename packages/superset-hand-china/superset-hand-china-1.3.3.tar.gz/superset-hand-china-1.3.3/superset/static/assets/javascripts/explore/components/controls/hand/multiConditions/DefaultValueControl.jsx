import React from 'react';
import PropTypes from 'prop-types';
import { Button, Row, Col } from 'react-bootstrap';
import { t } from '../../../../../locales';
import DefaultValue from './DefaultValue';

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

export default class DefaultValueControl extends React.Component {
  addDefaultValue() {
    const newDefaultValues = Object.assign([], this.props.value);
    newDefaultValues.push({
      field: '',
      type: 'sets',
      value: '',
      sql: '',
    });
    this.props.onChange(newDefaultValues);
  }
  changeDefaultValue(index, control, value) {
    const newDefaultValues = Object.assign([], this.props.value);
    const modifiedDefaultValue = Object.assign({}, newDefaultValues[index]);
    if (typeof control === 'string') {
      modifiedDefaultValue[control] = value;
    } else {
      control.forEach((c, i) => {
        modifiedDefaultValue[c] = value[i];
      });
    }
    newDefaultValues.splice(index, 1, modifiedDefaultValue);
    this.props.onChange(newDefaultValues);
  }
  removeDefaultValue(index) {
    this.props.onChange(this.props.value.filter((f, i) => i !== index));
  }
  render() {
    const defaultValues = this.props.value.map((defaultValue, i) => (
      <div key={i}>
        <DefaultValue
          defaultValue={defaultValue}
          datasource={this.props.datasource}
          removeDefaultValue={this.removeDefaultValue.bind(this, i)}
          changeDefaultValue={this.changeDefaultValue.bind(this, i)}
        />
      </div>
    ));
    return (
      <div>
        {defaultValues}
        <Row className="space-2">
          <Col md={2} >
            <Button
              id="add-button"
              bsSize="sm"
              onClick={this.addDefaultValue.bind(this)}
            >
              <i className="fa fa-plus" /> &nbsp; {t('Add DefaultValue')}
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

DefaultValueControl.propTypes = propTypes;
DefaultValueControl.defaultProps = defaultProps;
