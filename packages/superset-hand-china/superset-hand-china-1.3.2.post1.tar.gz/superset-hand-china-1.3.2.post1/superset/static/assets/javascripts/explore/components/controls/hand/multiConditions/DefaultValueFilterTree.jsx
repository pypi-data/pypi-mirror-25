import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';
import { Button, Row, Col } from 'react-bootstrap';

const $ = window.$ = require('jquery');

const propTypes = {
  changeDefaultValueFilterTree: PropTypes.func,
  removeDefaultValueFilterTree: PropTypes.func,
  defaultValueFilterTree: PropTypes.object.isRequired,
  datasource: PropTypes.object,
  having: PropTypes.bool,
};

const defaultProps = {
  changeDefaultValueFilterTree: () => {},
  removeDefaultValueFilterTree: () => {},
  datasource: null,
};

export default class DefaultValueFilterTree extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }
  // changeChilaId(value) {
  //   this.props.changeDefaultValueFilterTree('field', value);
  // }
  changeType(value) {
    this.props.changeDefaultValueFilterTree('type', value);
  }
  changeValue(event) {
    this.props.changeDefaultValueFilterTree('value', event.target.value);
  }
  changeSql(event) {
    this.props.changeDefaultValueFilterTree('sql', event.target.value);
  }
  removeDefaultValueFilterTree(defaultValueFilterTree) {
    this.props.removeDefaultValueFilterTree(defaultValueFilterTree);
  }
  render() {
    // const datasource = this.props.datasource;
    const defaultValueFilterTree = this.props.defaultValueFilterTree;
    // let colChoices;
    // if (datasource) {
    //   colChoices = datasource.gb_cols.map(c => ({ value: c[0], label: c[1] }));
    // }
    const typeChoices = ['sets', 'sql'].map(t => ({value: t, label: t}));
    return (
      <div>
        <Row className="space-1">
          {/* <Col md={6}>
            <label className="control-label">Chila Id:</label>
            <Select
              multi={false}
              simpleValue
              placeholder="Select Chila Id"
              options={colChoices}
              clearable={false}
              value={defaultValueFilterTree.field}
              onChange={this.changeChilaId.bind(this)}
            />
          </Col> */}
          <Col md={12}>
            <label className="control-label">Type:</label>
            <Select
              multi={false}
              simpleValue
              placeholder="Select Type"
              options={typeChoices}
              clearable={false}
              value={defaultValueFilterTree.type}
              onChange={this.changeType.bind(this)}
            />
          </Col>
          { defaultValueFilterTree.type === 'sets' &&
            <Col md={11}>
              <label className="control-label">Set value by sets:</label>
              <textarea
                className="form-control input-sm"
                placeholder="Collection, separated by commas, such as A,B,C"
                value={defaultValueFilterTree.value}
                onChange={this.changeValue.bind(this)}
              />
            </Col>
          }
          { defaultValueFilterTree.type === 'sql' &&
            <Col md={11}>
              <label className="control-label">Set value by sql:</label>
              <textarea
                className="form-control input-sm"
                placeholder="sql"
                value={defaultValueFilterTree.sql}
                onChange={this.changeSql.bind(this)}
              />
            </Col>
          }
          <Col md={1} style={{ marginTop: 25 }}>
            <Button
              id="remove-button"
              bsSize="small"
              onClick={this.removeDefaultValueFilterTree.bind(this)}
            >
              <i className="fa fa-minus" />
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

DefaultValueFilterTree.propTypes = propTypes;
DefaultValueFilterTree.defaultProps = defaultProps;
