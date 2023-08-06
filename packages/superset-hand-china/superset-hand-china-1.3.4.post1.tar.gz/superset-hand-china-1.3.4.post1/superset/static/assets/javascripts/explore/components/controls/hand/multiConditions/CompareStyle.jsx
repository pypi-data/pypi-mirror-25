import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';
import { Button, Row, Col } from 'react-bootstrap';
import { t } from '../../../../../locales';

const $ = window.$ = require('jquery');

const propTypes = {
  changeCompareStyle: PropTypes.func,
  removeCompareStyle: PropTypes.func,
  compareStyle: PropTypes.object.isRequired,
  datasource: PropTypes.object,
  having: PropTypes.bool,
};

const defaultProps = {
  changeCompareStyle: () => { },
  removeCompareStyle: () => { },
  datasource: null,
};

export default class CompareStyle extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      iconChoices: [
        { key: 'Null', value: '' },
        { key: 'Rise (single arrow)', value: 'fa fa-arrow-up' },
        { key: 'Down (single arrow)', value: 'fa fa-arrow-down' },
        { key: 'Rise (double arrow)', value: 'fa fa-angle-double-up' },
        { key: 'Down (double arrow)', value: 'fa fa-angle-double-down' },
        { key: 'Bar-chart', value: 'fa fa-bar-chart' },
        { key: 'Line-chart', value: 'fa fa-line-chart' },
        { key: 'Pie-chart', value: 'fa fa-pie-chart' },
        { key: 'Area-chart', value: 'fa fa-area-chart' },
      ],
    };
  }
  changeMetric1(value) {
    this.props.changeCompareStyle('metric1', value);
  }
  changeMetric2(value) {
    this.props.changeCompareStyle('metric2', value);
  }
  changeExpr(event) {
    this.props.changeCompareStyle('expr', event.target.value);
  }
  changeStyle(event) {
    this.props.changeCompareStyle('style', event.target.value);
  }
  removeCompareStyle(compareStyle) {
    this.props.removeCompareStyle(compareStyle);
  }
  renderOption(opt) {
    return (
      <div>
        <i className={opt.value} />
        <span style={{ marginLeft: '10px' }}>{opt.label}</span>
      </div>
      );
  }
  render() {
    const datasource = this.props.datasource;
    const compareStyle = this.props.compareStyle;
    let colChoices;
    if (datasource) {
      colChoices = datasource.metrics_combo.map(c => ({ value: c[0], label: c[1] }));
    }
    return (
      <div>
        <Row className="space-1">
          <Col md={6}>
            <label className="control-label">{t('metric1:')}</label>
            <Select
              multi={false}
              simpleValue
              placeholder={t('Select Metric1')}
              options={colChoices}
              clearable={false}
              value={compareStyle.metric1}
              onChange={this.changeMetric1.bind(this)}
            />
          </Col>
          <Col md={6}>
            <label className="control-label">{t('metric2:')}</label>
            <Select
              multi={false}
              simpleValue
              placeholder={t('Select Metric2')}
              options={colChoices}
              clearable={false}
              value={compareStyle.metric2}
              onChange={this.changeMetric2.bind(this)}
            />
          </Col>
        </Row>
        <Row className="space-1">
          <Col md={6}>
            <label className="control-label">{t('expression:')}</label>
            <input
              className="form-control input-sm"
              type="text"
              placeholder={t('compare expr(x, y => metric1, metric2)')}
              value={compareStyle.expr}
              onChange={this.changeExpr.bind(this)}
            />
          </Col>
          <Col md={5}>
            <label className="control-label">{t('style:')}</label>
            <input
              className="form-control input-sm"
              type="text"
              placeholder={t('Metric1 Style')}
              value={compareStyle.style}
              onChange={this.changeStyle.bind(this)}
            />
          </Col>
          <Col md={1} style={{ marginTop: 25 }}>
            <Button
              id="remove-button"
              bsSize="small"
              onClick={this.removeCompareStyle.bind(this)}
            >
              <i className="fa fa-minus" />
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

CompareStyle.propTypes = propTypes;
CompareStyle.defaultProps = defaultProps;
