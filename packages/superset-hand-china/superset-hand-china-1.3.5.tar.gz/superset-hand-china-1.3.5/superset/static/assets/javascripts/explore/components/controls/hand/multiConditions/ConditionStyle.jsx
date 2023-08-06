import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';
import { Button, Row, Col } from 'react-bootstrap';
import { t } from '../../../../../locales';

const $ = window.$ = require('jquery');

const propTypes = {
  changeConditionStyle: PropTypes.func,
  removeConditionStyle: PropTypes.func,
  conditionStyle: PropTypes.object.isRequired,
  datasource: PropTypes.object,
  having: PropTypes.bool,
};

const defaultProps = {
  changeConditionStyle: () => { },
  removeConditionStyle: () => { },
  datasource: null,
};

export default class ConditionStyle extends React.Component {
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
  changeMetric(value) {
    this.props.changeConditionStyle('metric', value);
  }
  changeExpr(event) {
    this.props.changeConditionStyle('expr', event.target.value);
  }
  changeStyle(event) {
    this.props.changeConditionStyle('style', event.target.value);
  }
  changeIcon(value) {
    this.props.changeConditionStyle('icon', value);
  }
  removeConditionStyle(conditionStyle) {
    this.props.removeConditionStyle(conditionStyle);
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
    const conditionStyle = this.props.conditionStyle;
    let colChoices;
    if (datasource) {
      colChoices = datasource.metrics_combo.map(c => ({ value: c[0], label: c[1] }));
    }
    return (
      <div>
        <Row className="space-1">
          <Col md={6}>
            <label className="control-label">{t('metric:')}</label>
            <Select
              multi={false}
              simpleValue
              placeholder={t('Select Metric')}
              options={colChoices}
              clearable={false}
              value={conditionStyle.metric}
              onChange={this.changeMetric.bind(this)}
            />
          </Col>
          <Col md={6}>
            <label className="control-label">{t('expression:')}</label>
            <input
              className="form-control input-sm"
              type="text"
              placeholder={t('Metric Expression')}
              value={conditionStyle.expr}
              onChange={this.changeExpr.bind(this)}
            />
          </Col>
        </Row>
        <Row className="space-1">
          <Col md={6}>
            <label className="control-label">{t('style:')}</label>
            <input
              className="form-control input-sm"
              type="text"
              placeholder={t('Metric Style')}
              value={conditionStyle.style}
              onChange={this.changeStyle.bind(this)}
            />
          </Col>
          <Col md={5}>
            <label className="control-label">{t('icon:')}</label>
            <Select
              multi={false}
              simpleValue
              placeholder={t('Select Icon')}
              options={this.state.iconChoices.map((o) => ({ label: o.key, value: o.value }))}
              optionRenderer={this.renderOption.bind(this)}
              clearable={false}
              value={conditionStyle.icon}
              onChange={this.changeIcon.bind(this)}
            />
          </Col>
          <Col md={1} style={{ marginTop: 25 }}>
            <Button
              id="remove-button"
              bsSize="small"
              onClick={this.removeConditionStyle.bind(this)}
            >
              <i className="fa fa-minus" />
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

ConditionStyle.propTypes = propTypes;
ConditionStyle.defaultProps = defaultProps;
