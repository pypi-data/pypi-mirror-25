import React from 'react';
import PropTypes from 'prop-types';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Button, Row, Col } from 'react-bootstrap';

import { t } from '../../../../../locales';
import Cascade from './Cascade';
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

class CascadeControl extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      data: null
    }
  }

  componentWillMount() {
    this.query();
  }

  query() {
    const {datasource, groupby} = this.props.form_data;
    const _this = this;
    $.ajax({
      async: false,
      type: "post",
      url: "/hand/queryCascadeData",
      dataType: "json",
      data: {
        datasource: datasource,
        groupby: groupby.join(','),
      },
      success: function (result) {
        _this.setState({ data: result });
      },
      error: function (err) {
        _this.setState({ data: null });
      }
    });
  }


  addCascade() {
    const newCascades = Object.assign([], this.props.value);
    newCascades.push({
      level: 1,
      parentNode: '',
      childNodes: '',
    });
    this.props.onChange(newCascades);
  }
  changeCascade(index, control, value) {
    const newCascades = Object.assign([], this.props.value);
    const modifiedCascade = Object.assign({}, newCascades[index]);
    if (typeof control === 'string') {
      modifiedCascade[control] = value;
    } else {
      control.forEach((c, i) => {
        modifiedCascade[c] = value[i];
      });
    }
    newCascades.splice(index, 1, modifiedCascade);
    this.props.onChange(newCascades);
  }
  removeCascade(index) {
    this.props.onChange(this.props.value.filter((f, i) => i !== index));
  }
  render() {
    const cascades = this.props.value.map((cascade, i) => (
      <div key={i}>
        <Cascade
          cascade={cascade}
          form_data={this.props.form_data}
          datasource={this.props.datasource}
          data={this.state.data}
          removeCascade={this.removeCascade.bind(this, i)}
          changeCascade={this.changeCascade.bind(this, i)}
        />
      </div>
    ));
    return (
      <div>
        {cascades}
        <Row className="space-2">
          <Col md={2}>
            <Button
              id="add-button"
              bsSize="sm"
              onClick={this.addCascade.bind(this)}
            >
              <i className="fa fa-plus" /> &nbsp; {t('Add Cascade')}
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

CascadeControl.propTypes = propTypes;

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

export { CascadeControl };

export default connect(mapStateToProps, mapDispatchToProps)(CascadeControl);

