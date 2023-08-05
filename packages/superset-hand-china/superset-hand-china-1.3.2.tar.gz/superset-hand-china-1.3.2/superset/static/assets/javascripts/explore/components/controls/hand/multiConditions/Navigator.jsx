import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';
import { Button, Row, Col } from 'react-bootstrap';
import { t } from '../../../../../locales';

const $ = window.$ = require('jquery');

const propTypes = {
  changeNavigator: PropTypes.func,
  removeNavigator: PropTypes.func,
  navigator: PropTypes.object.isRequired,
  datasource: PropTypes.object,
  having: PropTypes.bool,
  form_data: PropTypes.object,
};

const defaultProps = {
  changeNavigator: () => { },
  removeNavigator: () => { },
  datasource: null,
};

export default class Navigator extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      navigate_type: this.props.navigator.navigate_type,
      open_type: this.props.navigator.open_type,
      slicesChoices: [],
      dashboardChoices: [],
    };
  }
  jsonToArray(json) {
    const array = [];
    for (let k in json) {
      array.push({
        id: k,
        name: json[k]
      });
    }
    return array;
  }
  componentWillMount() {
    const _this = this;
    $.get('/hand/explore/getSlices', function(data) {
      const array = _this.jsonToArray(JSON.parse(data));
      _this.setState({ slicesChoices:  array});
    });
    $.get('/hand/explore/getDashboards', function(data) {
      const array = _this.jsonToArray(JSON.parse(data));
      _this.setState({ dashboardChoices: array });
    });
  }
  changeColumn(value) {
    this.props.changeNavigator('col', value);
  }
  changeExpr(event) {
    this.props.changeNavigator('expr', event.target.value);
  }
  changeNavigateType(value) {
    this.props.changeNavigator('navigate_type', value);
    this.setState({ 'navigate_type': value });
  }
  changeOpenType(value) {
    this.props.changeNavigator('open_type', value);
    this.setState({ 'open_type': value });
  }
  changeWidth(event) {
    this.props.changeNavigator('width', event.target.value);
  }
  changeHeight(event) {
    this.props.changeNavigator('height', event.target.value);
  }
  changeSliceId(value) {
    this.props.changeNavigator('slice_id', value);
  }
  changeDashboardId(value) {
    this.props.changeNavigator('dashboard_id', value);
  }
  changeFilterFrozen(value) {
    this.props.changeNavigator('filter_frozen', value);
  }
  removeNavigator(navigator) {
    this.props.removeNavigator(navigator);
  }
  render() {
    const datasource = this.props.datasource;
    const navigator = this.props.navigator;
    let colChoices;
    if (datasource) {
      colChoices = datasource.metrics_combo.concat(datasource.gb_cols).map(c => ({ value: c[0], label: c[1] }));
    }
    return (
      <div>
        <Row className="space-1">
          <Col md={6}>
            <label className="control-label">{t('Column:')}</label>
            <Select
              multi={false}
              simpleValue
              placeholder={t('Select Column')}
              options={colChoices}
              clearable={false}
              value={navigator.col}
              onChange={this.changeColumn.bind(this)}
            />
          </Col>
          <Col md={6}>
            <label className="control-label">{t('Expression:')}</label>
            <input
              className="form-control input-sm"
              type="text"
              placeholder={t('Metric Expression')}
              value={navigator.expr}
              onChange={this.changeExpr.bind(this)}
            />
          </Col>
        </Row>
        <Row className="space-1">
          <Col md={6}>
            <label className="control-label">{t('Navigate Type:')}</label>
            <Select
              multi={false}
              simpleValue
              placeholder={t('Select Navigate Type')}
              options={['slice', 'dashboard'].map(c => ({ value: c, label: c }))}
              clearable={false}
              value={navigator.navigate_type}
              onChange={this.changeNavigateType.bind(this)}
            />
          </Col>
          <Col md={6}>
            <label className="control-label">{t('Open Type:')}</label>
            <Select
              multi={false}
              simpleValue
              placeholder={t('Select Open Type')}
              options={['modal', 'new window'].map(c => ({ value: c, label: c }))}
              clearable={false}
              value={navigator.open_type}
              onChange={this.changeOpenType.bind(this)}
            />
          </Col>
        </Row>
        { this.state.open_type === 'modal' &&
          <Row className="space-1">
            <Col md={6}>
              <label className="control-label">{t('Width:')}</label>
              <input
                className="form-control input-sm"
                type="text"
                placeholder={t('Width')}
                value={navigator.width}
                onChange={this.changeWidth.bind(this)}
              />
            </Col>
            <Col md={6}>
              <label className="control-label">{t('Height:')}</label>
              <input
                className="form-control input-sm"
                type="text"
                placeholder={t('Height')}
                value={navigator.height}
                onChange={this.changeHeight.bind(this)}
              />
            </Col>
          </Row>
        }
        <Row className="space-1">
          { this.state.navigate_type === 'slice' &&
            <Col md={6}>
              <label className="control-label">{t('Slice:')}</label>
              <Select
                multi={false}
                simpleValue
                placeholder={t('Select Slice')}
                options={this.state.slicesChoices.map(c => ({ value: c['id'], label: c['name'] }))}
                clearable={false}
                value={navigator.slice_id}
                onChange={this.changeSliceId.bind(this)}
              />
            </Col>
          }
          { this.state.navigate_type === 'dashboard' &&
            <div>
              <Col md={6}>
                <label className="control-label">{t('Dashboard:')}</label>
                <Select
                  multi={false}
                  simpleValue
                  placeholder={t('Select Dashboard')}
                  options={this.state.dashboardChoices.map(c => ({ value: c['id'], label: c['name'] }))}
                  clearable={false}
                  value={navigator.dashboard_id}
                  onChange={this.changeDashboardId.bind(this)}
                />
              </Col>
              <Col md={5}>
                <label className="control-label">{t('Is Filter Frozen:')}</label>
                <Select
                  multi={false}
                  simpleValue
                  placeholder={t('Is Filter Frozen')}
                  options={['true', 'false'].map(c => ({ value: c, label: c }))}
                  clearable={false}
                  value={navigator.filter_frozen}
                  onChange={this.changeFilterFrozen.bind(this)}
                />
              </Col>
            </div>
          }
          <Col md={1} style={{ marginTop: 25 }}>
            <Button
              id="remove-button"
              bsSize="small"
              onClick={this.removeNavigator.bind(this)}
            >
              <i className="fa fa-minus" />
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

Navigator.propTypes = propTypes;
Navigator.defaultProps = defaultProps;
