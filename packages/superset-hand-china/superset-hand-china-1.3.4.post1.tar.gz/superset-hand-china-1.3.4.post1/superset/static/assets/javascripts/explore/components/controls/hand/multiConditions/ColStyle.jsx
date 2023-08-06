import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';
import { Button, Row, Col } from 'react-bootstrap';
import { t } from '../../../../../locales';

const $ = window.$ = require('jquery');

const propTypes = {
  changeColStyle: PropTypes.func,
  removeColStyle: PropTypes.func,
  colStyle: PropTypes.object.isRequired,
  datasource: PropTypes.object,
  having: PropTypes.bool,
};

const defaultProps = {
  changeColStyle: () => {},
  removeColStyle: () => {},
  datasource: null,
};

export default class ColStyle extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }
  changeCol(value) {
    this.props.changeColStyle('col', value);
  }
  changeStyle(event) {
    this.props.changeColStyle('style', event.target.value);
  }
  removeColStyle(colStyle) {
    this.props.removeColStyle(colStyle);
  }
  render() {
    const datasource = this.props.datasource;
    const colStyle = this.props.colStyle;
    let colChoices;
    if (datasource) {
      colChoices = datasource.gb_cols.concat(datasource.metrics_combo).map(c => ({ value: c[0], label: c[1] }));
    }
    return (
      <div>
        <Row className="space-1">
          <Col md={6}>
            <label className="control-label">{t('Columns:')}</label>
            <Select
              multi={false}
              simpleValue
              placeholder={t('Select Column')}
              options={colChoices}
              clearable={false}
              value={colStyle.col}
              onChange={this.changeCol.bind(this)}
            />
          </Col>
          <Col md={5}>
            <label className="control-label">{t('Style:')}</label>
            <input
              className="form-control input-sm"
              type="text"
              placeholder={t('Column Style')}
              value={colStyle.style}
              onChange={this.changeStyle.bind(this)}
            />
          </Col>
          <Col md={1} style={{ marginTop: 25 }}>
            <Button
              id="remove-button"
              bsSize="small"
              onClick={this.removeColStyle.bind(this)}
            >
              <i className="fa fa-minus" />
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

ColStyle.propTypes = propTypes;
ColStyle.defaultProps = defaultProps;
