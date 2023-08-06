import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';
import { Button, Row, Col } from 'react-bootstrap';
import { t } from '../../../../../locales';

const $ = window.$ = require('jquery');

const propTypes = {
  changeFilterSetting: PropTypes.func,
  removeFilterSetting: PropTypes.func,
  filterSetting: PropTypes.object.isRequired,
  datasource: PropTypes.object,
  having: PropTypes.bool,
};

const defaultProps = {
  changeFilterSetting: () => {},
  removeFilterSetting: () => {},
  datasource: null,
};

export default class FilterSetting extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }
  changeMetric(value) {
    this.props.changeFilterSetting('metric', value);
  }
  changeWidth(event) {
    this.props.changeFilterSetting('width', event.target.value);
  }
  changeType(value) {
    this.props.changeFilterSetting('type', value);
  }
  changeRange(value) {
    this.props.changeFilterSetting('range', value);
  }
  removeFilterSetting(filterSetting) {
    this.props.removeFilterSetting(filterSetting);
  }
  render() {
    const datasource = this.props.datasource;
    const filterSetting = this.props.filterSetting;
    let colChoices;
    if (datasource) {
      colChoices = datasource.gb_cols.map(c => ({ value: c[0], label: c[1] }));
    }
    const sqlChoices =['in','not in','==','!=','<=','>=','<','>','like'].map(b => ({value: b, label: b}));
    // const typeChoices = ['single select', 'multi select', 'radio', 'checkbox'].map(t => ({value: t, label: t}));
    const typeChoices = [
      { label: t('single select'), value: 'single select' },
      { label: t('multi select'), value: 'multi select' },
      { label: t('radio'), value: 'radio' },
      { label: t('checkbox'), value: 'checkbox' },
    ].map((xt) => ({ value: xt.value, label: xt.label }));
    return (
      <div>
        <Row className="space-1">
          <Col md={6}>
            <label className="control-label">{t('Metric:')}</label>
            <Select
              multi={false}
              simpleValue
              placeholder={t('Select Metric')}
              options={colChoices}
              clearable={false}
              value={filterSetting.metric}
              onChange={this.changeMetric.bind(this)}
            />
          </Col>
          <Col md={6}>
            <label className="control-label">{t('Width:')}</label>
            <input
              className="form-control input-sm"
              type="text"
              placeholder={t('Filter Width')}
              value={filterSetting.width}
              onChange={this.changeWidth.bind(this)}
            />
          </Col>
          <Col md={6}>
            <label className="control-label">{t('Type:')}</label>
            <Select
              multi={false}
              simpleValue
              placeholder={t('Select Filter Type')}
              options={typeChoices}
              clearable={false}
              value={filterSetting.type}
              onChange={this.changeType.bind(this)}
            />
          </Col>
          { filterSetting.type =='single select' && <Col md={4}>
            <label className="control-label">Range:</label>
            <Select
              multi={false}
              simpleValue
              placeholder="Select Filter Range"
              options={sqlChoices}
              clearable={false}
              value={(filterSetting.range === undefined ||
                filterSetting.range === '') ? 'in' : filterSetting.range}
              onChange={this.changeRange.bind(this)}
            />
          </Col>}
          <Col md={1} style={{ marginTop: 25 }}>
            <Button
              id="remove-button"
              bsSize="small"
              onClick={this.removeFilterSetting.bind(this)}
            >
              <i className="fa fa-minus" />
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

FilterSetting.propTypes = propTypes;
FilterSetting.defaultProps = defaultProps;
