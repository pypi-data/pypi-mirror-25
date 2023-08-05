import React from 'react';
import PropTypes from 'prop-types';

import BoundsControl from './controls/BoundsControl';
import CheckboxControl from './controls/CheckboxControl';
import DatasourceControl from './controls/DatasourceControl';
import DateFilterControl from './controls/DateFilterControl';
import FilterControl from './controls/FilterControl';
import HiddenControl from './controls/HiddenControl';
import SelectControl from './controls/SelectControl';
import TextAreaControl from './controls/TextAreaControl';
import TextControl from './controls/TextControl';
import VizTypeControl from './controls/VizTypeControl';
import ColorSchemeControl from './controls/ColorSchemeControl';

import ButtonControl from './controls/hand/ButtonControl';
import StackControl from './controls/hand/multiConditions/StackControl';
import ColStyleControl from './controls/hand/multiConditions/ColStyleControl';
import ConditionStyleControl from './controls/hand/multiConditions/ConditionStyleControl';
import CompareStyleControl from './controls/hand/multiConditions/CompareStyleControl';
import NavigatorControl from './controls/hand/multiConditions/NavigatorControl';
import ParentNodeControl from './controls/hand/multiConditions/ParentNodeControl';
import FilterSettingControl from './controls/hand/multiConditions/FilterSettingControl';
import DefaultValueControl from './controls/hand/multiConditions/DefaultValueControl';
import DefaultValueFilterTreeControl from './controls/hand/multiConditions/DefaultValueFilterTreeControl';
import FilterCombinationControl from './controls/hand/FilterCombinationControl';
import DateValueControl from './controls/hand/DateValueControl';
import OrderSelectControl from './controls/hand/OrderSelectControl';
import IconControl from './controls/hand/IconControl';
import DatePickerControl from './controls/hand/DatePickerControl';
import CascadeControl from './controls/hand/multiConditions/CascadeControl';

const controlMap = {
  BoundsControl,
  CheckboxControl,
  DatasourceControl,
  DateFilterControl,
  FilterControl,
  HiddenControl,
  SelectControl,
  TextAreaControl,
  TextControl,
  VizTypeControl,
  ColorSchemeControl,

  ButtonControl,
  StackControl,
  ColStyleControl,
  ConditionStyleControl,
  CompareStyleControl,
  NavigatorControl,
  ParentNodeControl,
  FilterSettingControl,
  DefaultValueControl,
  DefaultValueFilterTreeControl,
  FilterCombinationControl,
  DateValueControl,
  OrderSelectControl,
  IconControl,
  DatePickerControl,
  CascadeControl,

};
const controlTypes = Object.keys(controlMap);

const propTypes = {
  actions: PropTypes.object.isRequired,
  name: PropTypes.string.isRequired,
  type: PropTypes.oneOf(controlTypes).isRequired,
  hidden: PropTypes.bool,
  label: PropTypes.string.isRequired,
  choices: PropTypes.arrayOf(PropTypes.array),
  description: PropTypes.string,
  places: PropTypes.number,
  validators: PropTypes.array,
  validationErrors: PropTypes.array,
  renderTrigger: PropTypes.bool,
  rightNode: PropTypes.node,
  value: PropTypes.oneOfType([
    PropTypes.string,
    PropTypes.number,
    PropTypes.bool,
    PropTypes.array]),
};

const defaultProps = {
  renderTrigger: false,
  validators: [],
  hidden: false,
  validationErrors: [],
};

export default class Control extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = { hovered: false };
    this.validate = this.validate.bind(this);
    this.onChange = this.onChange.bind(this);
  }
  componentDidMount() {
    this.validateAndSetValue(this.props.value, []);
  }
  onChange(value, errors) {
    this.validateAndSetValue(value, errors);
  }
  setHover(hovered) {
    this.setState({ hovered });
  }
  validateAndSetValue(value, errors) {
    let validationErrors = this.props.validationErrors;
    let currentErrors = this.validate(value);
    if (errors && errors.length > 0) {
      currentErrors = validationErrors.concat(errors);
    }
    if (validationErrors.length + currentErrors.length > 0) {
      validationErrors = currentErrors;
    }

    if (value !== this.props.value || validationErrors !== this.props.validationErrors) {
      this.props.actions.setControlValue(this.props.name, value, validationErrors);
    }
  }
  validate(value) {
    const validators = this.props.validators;
    const validationErrors = [];
    if (validators && validators.length > 0) {
      validators.forEach((f) => {
        const v = f(value);
        if (v) {
          validationErrors.push(v);
        }
      });
    }
    return validationErrors;
  }
  render() {
    const ControlType = controlMap[this.props.type];
    const divStyle = this.props.hidden ? { display: 'none' } : null;
    return (
      <div
        style={divStyle}
        onMouseEnter={this.setHover.bind(this, true)}
        onMouseLeave={this.setHover.bind(this, false)}
      >
        <ControlType
          onChange={this.onChange}
          hovered={this.state.hovered}
          {...this.props}
        />
      </div>
    );
  }
}

Control.propTypes = propTypes;
Control.defaultProps = defaultProps;
