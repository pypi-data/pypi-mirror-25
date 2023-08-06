import React from 'react';
import PropTypes from 'prop-types';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Button, Row, Col } from 'react-bootstrap';
import { t } from '../../../../../locales';
import Navigator from './Navigator';
import * as actions from '../../../../actions/exploreActions';
import { getFormDataFromControls } from '../../../../stores/store';

const propTypes = {
  name: PropTypes.string,
  onChange: PropTypes.func,
  value: PropTypes.array,
  datasource: PropTypes.object,
  form_data: PropTypes.object,
};

const defaultProps = {
  onChange: () => {},
  value: [],
};

class NavigatorControl extends React.Component {
  addNavigator() {
    const newNavigators = Object.assign([], this.props.value);
    newNavigators.push({
      col: '',
      expr: '',
      navigate_type: 'slice',
      open_type: 'new window',
      width: '',
      height: '',
      slice_id: null,
      dashboard_id: null,
      filter_frozen: 'false',
    });
    this.props.onChange(newNavigators);
  }
  changeNavigator(index, control, value) {
    const newNavigators = Object.assign([], this.props.value);
    const modifiedNavigator = Object.assign({}, newNavigators[index]);
    if (typeof control === 'string') {
      modifiedNavigator[control] = value;
    } else {
      control.forEach((c, i) => {
        modifiedNavigator[c] = value[i];
      });
    }
    newNavigators.splice(index, 1, modifiedNavigator);
    this.props.onChange(newNavigators);
  }
  removeNavigator(index) {
    this.props.onChange(this.props.value.filter((f, i) => i !== index));
  }
  render() {
    const navigators = this.props.value.map((navigator, i) => (
      <div key={i}>
        <Navigator
          navigator={navigator}
          form_data={this.props.form_data}
          datasource={this.props.datasource}
          removeNavigator={this.removeNavigator.bind(this, i)}
          changeNavigator={this.changeNavigator.bind(this, i)}
        />
      </div>
    ));
    return (
      <div>
        {navigators}
        <Row className="space-2">
          <Col md={2}>
            <Button
              id="add-button"
              bsSize="sm"
              onClick={this.addNavigator.bind(this)}
            >
              <i className="fa fa-plus" /> &nbsp; {t('Add Navigator')}
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

NavigatorControl.propTypes = propTypes;

function mapStateToProps({ explore }) {
  const form_data = getFormDataFromControls(explore.controls);
  return {
    form_data
  };
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(actions, dispatch),
  };
}

export { NavigatorControl };

export default connect(mapStateToProps, mapDispatchToProps)(NavigatorControl);

