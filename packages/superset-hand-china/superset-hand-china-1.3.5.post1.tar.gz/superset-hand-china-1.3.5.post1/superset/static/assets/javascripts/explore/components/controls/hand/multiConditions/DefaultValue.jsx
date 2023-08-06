import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';
import { Button, Row, Col } from 'react-bootstrap';
import { t } from '../../../../../locales';

const $ = window.$ = require('jquery');

const propTypes = {
  changeDefaultValue: PropTypes.func,
  removeDefaultValue: PropTypes.func,
  defaultValue: PropTypes.object.isRequired,
  datasource: PropTypes.object,
  having: PropTypes.bool,
};

const defaultProps = {
  changeDefaultValue: () => {},
  removeDefaultValue: () => {},
  datasource: null,
};

export default class DefaultValue extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }
  changeField(value) {
    this.props.changeDefaultValue('field', value);
  }
  changeType(value) {
    this.props.changeDefaultValue('type', value);
  }
  changeValue(event) {
    this.props.changeDefaultValue('value', event.target.value);
  }
  changeSql(event) {
    this.props.changeDefaultValue('sql', event.target.value);
  }
  removeDefaultValue(defaultValue) {
    this.props.removeDefaultValue(defaultValue);
  }
  render() {
    const datasource = this.props.datasource;
    const defaultValue = this.props.defaultValue;
    let colChoices;
    if (datasource) {
      colChoices = datasource.gb_cols.map(c => ({ value: c[0], label: c[1] }));
    }
    // const typeChoices = ['sets', 'sql'].map(t => ({value: t, label: t}));
    const typeChoices = [
      { label: t('Select the default value from the collection'), value: 'sets' },
      { label: t('Query the default collection from the sql statement'), value: 'sql' },
    ].map((xt) => ({ value: xt.value, label: xt.label }));
    return (
      <div>
        <Row className="space-1">
          <Col md={6}>
            <label className="control-label">{t('Field:')}</label>
            <Select
              multi={false}
              simpleValue
              placeholder={t('Select Field')}
              options={colChoices}
              clearable={false}
              value={defaultValue.field}
              onChange={this.changeField.bind(this)}
            />
          </Col>
          <Col md={6}>
            <label className="control-label">{t('Type:')}</label>
            <Select
              multi={false}
              simpleValue
              placeholder={t('Select Type')}
              options={typeChoices}
              clearable={false}
              value={defaultValue.type}
              onChange={this.changeType.bind(this)}
            />
          </Col>
          { defaultValue.type === 'sets' &&
            <Col md={11}>
              <label className="control-label">{t('Set value by sets:')}</label>
              <textarea
                className="form-control input-sm"
                placeholder={t('Collection, separated by commas, such as A,B,C')}
                value={defaultValue.value}
                onChange={this.changeValue.bind(this)}
              />
            </Col>
          }
          { defaultValue.type === 'sql' &&
            <Col md={11}>
              <label className="control-label">{t('Set value by sql:')}</label>
              <textarea
                className="form-control input-sm"
                placeholder={t('sql')}
                value={defaultValue.sql}
                onChange={this.changeSql.bind(this)}
              />
            </Col>
          }
          <Col md={1} style={{ marginTop: 25 }}>
            <Button
              id="remove-button"
              bsSize="small"
              onClick={this.removeDefaultValue.bind(this)}
            >
              <i className="fa fa-minus" />
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

DefaultValue.propTypes = propTypes;
DefaultValue.defaultProps = defaultProps;
