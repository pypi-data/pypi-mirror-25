import React from 'react';
import PropTypes from 'prop-types';
import { bindActionCreators } from 'redux';
import { connect } from 'react-redux';
import { Button, Row, Col } from 'react-bootstrap';
import { t } from '../../../../../locales';
import ParentNode from './ParentNode';
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

class ParentNodeControl extends React.Component {
  addParentNode() {
    const newParentNodes = Object.assign([], this.props.value);
    newParentNodes.push({
      parentName: '',
      children: '',
      show_items: '',
    });
    this.props.onChange(newParentNodes);
  }
  changeParentNode(index, control, value) {
    const newParentNodes = Object.assign([], this.props.value);
    const modifiedParentNode = Object.assign({}, newParentNodes[index]);
    if (typeof control === 'string') {
      modifiedParentNode[control] = value;
    } else {
      control.forEach((c, i) => {
        modifiedParentNode[c] = value[i];
      });
    }
    newParentNodes.splice(index, 1, modifiedParentNode);
    this.props.onChange(newParentNodes);
  }
  removeParentNode(index) {
    this.props.onChange(this.props.value.filter((f, i) => i !== index));
  }
  render() {
    // console.info(this.props.form_data)
    const parentNodes = this.props.value.map((parentNode, i) => (
      <div key={i}>
        <ParentNode
          parentNode={parentNode}
          datasource={this.props.datasource}
          removeParentNode={this.removeParentNode.bind(this, i)}
          changeParentNode={this.changeParentNode.bind(this, i)}
        />
      </div>
    ));
    return (
      <div>
        <div><hr style={{ borderTop: '1px solid rgb(85, 85, 85)' }}/></div>
        { this.props.form_data.is_pivot === 'false' &&
          <div>
            {parentNodes}
            <Row className="space-2">
              <Col md={2}>
                <Button
                  id="add-button"
                  bsSize="sm"
                  onClick={this.addParentNode.bind(this)}
                >
                  <i className="fa fa-plus" /> &nbsp; {t('Add ParentNode')}
                </Button>
              </Col>
            </Row>
          </div>
        }
      </div>
    );
  }
}


ParentNodeControl.propTypes = propTypes;

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

export { ParentNodeControl };

export default connect(mapStateToProps, mapDispatchToProps)(ParentNodeControl);
