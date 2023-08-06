import React from 'react';
import PropTypes from 'prop-types';
import { Button, Row, Col } from 'react-bootstrap';
import { t } from '../../../../../locales';
import DefaultValueFilterTree from './DefaultValueFilterTree';

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

export default class DefaultValueFilterTreeControl extends React.Component {
  addDefaultValueFilterTree() {
    const newDefaultValues = Object.assign([], this.props.value);
    newDefaultValues.push({
      // field: '',
      type: 'sets',
      value: '',
      sql: '',
    });
    this.props.onChange(newDefaultValues);
  }
  changeDefaultValueFilterTree(index, control, value) {
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
  removeDefaultValueFilterTree(index) {
    this.props.onChange(this.props.value.filter((f, i) => i !== index));
  }
  render() {
    const defaultValues = this.props.value.map((defaultValue, i) => (
      <div key={i}>
        <DefaultValueFilterTree
          defaultValueFilterTree={defaultValue}
          datasource={this.props.datasource}
          removeDefaultValueFilterTree={this.removeDefaultValueFilterTree.bind(this, i)}
          changeDefaultValueFilterTree={this.changeDefaultValueFilterTree.bind(this, i)}
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
              onClick={this.addDefaultValueFilterTree.bind(this)}
            >
              <i className="fa fa-plus" /> &nbsp; {t('Add DefaultValue')}
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

DefaultValueFilterTreeControl.propTypes = propTypes;
DefaultValueFilterTreeControl.defaultProps = defaultProps;
