/* eslint camelcase: 0 */
import React from 'react';
import PropTypes from 'prop-types';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Alert } from 'react-bootstrap';
import { sectionsToRender } from '../../../stores/visTypes';
import ControlPanelSection from '../../ControlPanelSection';
import ControlRow from '../../ControlRow';
import Control from '../../Control';
import controls from '../../../stores/controls';
import * as actions from '../../../actions/exploreActions';
import { getFormDataFromControls } from '../../../stores/store';

import { Modal } from 'react-bootstrap';
const $ = window.$ = require('jquery');

const propTypes = {
  onHide: React.PropTypes.func.isRequired,
  actions: PropTypes.object.isRequired,
  alert: PropTypes.string,
  datasource_type: PropTypes.string.isRequired,
  exploreState: PropTypes.object.isRequired,
  controls: PropTypes.object.isRequired,
  form_data: PropTypes.object.isRequired,
  isDatasourceMetaLoading: PropTypes.bool.isRequired,
};

class ControlModal extends React.Component {
  constructor(props) {
    super(props);
    this.removeAlert = this.removeAlert.bind(this);
    this.getControlData = this.getControlData.bind(this);
    this.state = {
      menu: 'baseStyle'
    }
    if (this.props.form_data.viz_type === 'filter_box') {
      this.state.menu = 'baseSetting';
    } else if (this.props.form_data.viz_type === 'filter_box_tree') {
      this.state.menu = 'setDefaultValueFilterTree';
    } else if (this.props.form_data.viz_type === 'filter_box_cascade') {
      this.state.menu = 'cascadeSetting';
    }
  }
  getControlData(controlName) {
    const mapF = controls[controlName].mapStateToProps;
    if (mapF) {
      return Object.assign({}, this.props.controls[controlName], mapF(this.props.exploreState));
    }
    return this.props.controls[controlName];
  }
  sectionsToRender() {
    return sectionsToRender(this.props.form_data.viz_type, this.props.datasource_type);
  }
  removeAlert() {
    this.props.actions.removeControlPanelAlert();
  }
  toggleMenu(menu, event) {
    // toggle style
    $('li a').attr('class', '');
    $('li a').attr('style', '');
    $(event.target).attr('class', 'active');
    $(event.target).css('background', '#ccc');
    // set menu state
    this.setState({ menu: menu });
  }
  render() {
    return (
      <Modal
        show
        onHide={this.props.onHide}
        bsStyle="large"
      >
        <Modal.Header closeButton>
          <Modal.Title>
            <div>
              {this.props.form_data.viz_type === 'ag_grid' &&
                <ul className="nav navbar-nav" style={{ fontSize: '14px' }}>
                  <li onClick={this.toggleMenu.bind(this, 'baseStyle')}>
                    <a className="active" style={{ background: "#ccc" }}>baseStyle</a>
                  </li>
                  <li onClick={this.toggleMenu.bind(this, 'condition')}><a>condition</a></li>
                  <li onClick={this.toggleMenu.bind(this, 'compare')}><a>compare</a></li>
                  <li onClick={this.toggleMenu.bind(this, 'navigator')}><a>navigator</a></li>
                  <li onClick={this.toggleMenu.bind(this, 'agGrid')}><a>agGrid</a></li>
                </ul>
              }
              {this.props.form_data.viz_type === 'filter_box' &&
                <ul className="nav navbar-nav" style={{ fontSize: '14px' }}>
                  <li onClick={this.toggleMenu.bind(this, 'baseSetting')}>
                    <a className="active" style={{ background: "#ccc" }}>baseSetting</a>
                  </li>
                  <li onClick={this.toggleMenu.bind(this, 'setDefaultValue')}><a>setDefaultValue</a></li>
                  <li onClick={this.toggleMenu.bind(this, 'setDateValue')}><a>setDateValue</a></li>
                </ul>
              }
              {this.props.form_data.viz_type === 'filter_box_tree' &&
                <ul className="nav navbar-nav" style={{ fontSize: '14px' }}>
                  <li onClick={this.toggleMenu.bind(this, 'setDefaultValueFilterTree')}>
                    <a className="active" style={{ background: "#ccc" }}>setDefaultValue</a>
                  </li>
                </ul>
              }
              {this.props.form_data.viz_type === 'filter_box_cascade' &&
                <ul className="nav navbar-nav" style={{ fontSize: '14px' }}>
                  <li onClick={this.toggleMenu.bind(this, 'cascadeSetting')}>
                    <a className="active" style={{ background: "#ccc" }}>cascadeSetting</a>
                  </li>
                  <li onClick={this.toggleMenu.bind(this, 'setDefaultValue')}><a>setDefaultValue</a></li>
                </ul>
              }
            </div>
          </Modal.Title>
        </Modal.Header>
        <Modal.Body style={{ minHeight: '300px' }}>
          {this.sectionsToRender().map((section, k) => (
            <div key={`panel-${k}`}>
              {section.controlSetRows.map((controlSets, i) => (
                ( this.state.menu === section.label || 
                  (this.state.menu === 'agGrid' && this.props.form_data.is_pivot === 'true' && section.label === 'agGrid_pivot')) &&
                <ControlRow
                  key={`controlsetrow-${i}`}
                  controls={controlSets.map(controlName => (
                    <Control
                      name={controlName}
                      key={`control-${controlName}`}
                      value={this.props.form_data[controlName]}
                      validationErrors={this.props.controls[controlName].validationErrors}
                      actions={this.props.actions}
                      {...this.getControlData(controlName)}
                    />
                  ))}
                />
                )
              )}
            </div>
          ))}
        </Modal.Body>
        <Modal.Footer>
        </Modal.Footer>
      </Modal>
    );
  }
}

ControlModal.propTypes = propTypes;

function mapStateToProps({ explore }) {
  const form_data = getFormDataFromControls(explore.controls);
  return {
    alert: explore.controlPanelAlert,
    isDatasourceMetaLoading: explore.isDatasourceMetaLoading,
    controls: explore.controls,
    exploreState: explore,
    datasource_type: explore.datasource_type,
    form_data
  };
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(actions, dispatch),
  };
}

export { ControlModal };

export default connect(mapStateToProps, mapDispatchToProps)(ControlModal);
