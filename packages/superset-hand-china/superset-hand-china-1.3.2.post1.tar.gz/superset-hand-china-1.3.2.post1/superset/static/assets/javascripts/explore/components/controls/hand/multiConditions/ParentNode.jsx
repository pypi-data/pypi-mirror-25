import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';
import { Button, Row, Col } from 'react-bootstrap';

const $ = window.$ = require('jquery');

const propTypes = {
  changeParentNode: PropTypes.func,
  removeParentNode: PropTypes.func,
  parentNode: PropTypes.object.isRequired,
  datasource: PropTypes.object,
  having: PropTypes.bool,
};

const defaultProps = {
  changeParentNode: () => {},
  removeParentNode: () => {},
  datasource: null,
};

export default class ParentNode extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }
  changeParentName(event) {
    this.props.changeParentNode('parentName', event.target.value);
    
  }
  changeChildren(value) {
    this.props.changeParentNode('children', value);
  }
  changeShowItems(value) {
    this.props.changeParentNode('show_items', value);
  }
  removeParentNode(parentNode) {
    this.props.removeParentNode(parentNode);
  }
  render() {
    const datasource = this.props.datasource;
    const parentNode = this.props.parentNode;
    let colChoices;
    if (datasource) {
      colChoices = datasource.gb_cols.concat(datasource.metrics_combo).map(c => ({ value: c[0], label: c[1] }));
    }
    return (
      <div>
        <Row className="space-1">
          <Col md={11}>
            <label className="control-label">Parent_Name:</label>
            <input
              className="form-control input-sm"
              type="text"
              placeholder="Column Style"
              value={parentNode.parentName}
              onChange={this.changeParentName.bind(this)}
            />
          </Col>
          <Col md={1} style={{ marginTop: 25 }}>
            <Button
              id="remove-button"
              bsSize="small"
              onClick={this.removeParentNode.bind(this)}
              >
              <i className="fa fa-minus" />
            </Button>
          </Col>
        </Row>
        <Row className="space-1">
          <Col md={6}>
            <label className="control-label">children:</label>
            <Select
              multi
              simpleValue
              placeholder="Select Children"
              options={colChoices}
              clearable={false}
              value={parentNode.children}
              onChange={this.changeChildren.bind(this)}
            />
          </Col>
          <Col md={6}>
            <label className="control-label">Show_Items:</label>
            <Select
              multi
              simpleValue
              placeholder="Select Items"
              options={colChoices}
              clearable={false}
              value={parentNode.show_items}
              onChange={this.changeShowItems.bind(this)}
            />
          </Col>
        </Row>
      </div>
    );
  }
}

ParentNode.propTypes = propTypes;
ParentNode.defaultProps = defaultProps;
