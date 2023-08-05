import React from 'react';
import PropTypes from 'prop-types';
import { Button, Row, Col } from 'react-bootstrap';
import { t } from '../../../../../locales';
import FilterSetting from './FilterSetting';

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

export default class FilterSettingControl extends React.Component {
  addFilterSetting() {
    const newFilterSettings = Object.assign([], this.props.value);
    newFilterSettings.push({
      metric: '',
      width: '',
      type: '',
      range: '',
    });
    this.props.onChange(newFilterSettings);
  }
  changeFilterSetting(index, control, value) {
    const newFilterSettings = Object.assign([], this.props.value);
    const modifiedFilterSetting = Object.assign({}, newFilterSettings[index]);
    if (typeof control === 'string') {
      modifiedFilterSetting[control] = value;
    } else {
      control.forEach((c, i) => {
        modifiedFilterSetting[c] = value[i];
      });
    }
    newFilterSettings.splice(index, 1, modifiedFilterSetting);
    this.props.onChange(newFilterSettings);
  }
  removeFilterSetting(index) {
    this.props.onChange(this.props.value.filter((f, i) => i !== index));
  }
  render() {
    const filterSettings = this.props.value.map((filterSetting, i) => (
      <div key={i}>
        <FilterSetting
          filterSetting={filterSetting}
          datasource={this.props.datasource}
          removeFilterSetting={this.removeFilterSetting.bind(this, i)}
          changeFilterSetting={this.changeFilterSetting.bind(this, i)}
        />
      </div>
    ));
    return (
      <div>
        {filterSettings}
        <Row className="space-2">
          <Col md={2} >
            <Button
              id="add-button"
              bsSize="sm"
              onClick={this.addFilterSetting.bind(this)}
            >
              <i className="fa fa-plus" /> &nbsp; {t('Add FilterSetting')}
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

FilterSettingControl.propTypes = propTypes;
FilterSettingControl.defaultProps = defaultProps;
