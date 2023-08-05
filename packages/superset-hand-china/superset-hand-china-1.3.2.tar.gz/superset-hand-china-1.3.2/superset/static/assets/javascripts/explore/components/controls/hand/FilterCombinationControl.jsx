import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';

import { t } from '../../../../locales';
import $ from 'jquery';

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

export default class FilterCombinationControl extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      filter_boxs: [],
    };
  }

  componentWillMount() {
    const _this = this;
    $.get('/hand/getFilterBoxs', function(data) {
      const filter_boxs = JSON.parse(data);
      _this.setState({ filter_boxs: filter_boxs });
    });
  }

  changeFilterCombination(vals) {
    const optionValue = vals ? vals.map(o => o.value) : null;
    this.props.onChange(optionValue);
  }

  render() {
    return (
      <div>
        <label>{t('filter boxs:')}</label>
        <Select.Creatable
          placeholder={t('Select slices')}
          multi
          value={this.props.value}
          options={ this.state.filter_boxs.map( f => ({value: f.id, label: f.slice_name}) )}
          onChange={this.changeFilterCombination.bind(this)}
        />
      </div>
    );
  }
}

FilterCombinationControl.propTypes = propTypes;
FilterCombinationControl.defaultProps = defaultProps;
