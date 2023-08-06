import React from 'react';
import PropTypes from 'prop-types';
import { Button, Row, Col } from 'react-bootstrap';

import { t } from '../../../../locales';
import ControlModal from './ControlModal';

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

export default class ButtonControl extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      showModal: false,
    };
  }

  toggleModal() {
    this.setState({ showModal: !this.state.showModal });
  }

  render() {
    return (
      <div>
        <Row className="space-2">
          <Col md={4}>
            <Button
              bsSize="sm"
              onClick={this.toggleModal.bind(this)}
            >
              <i className="fa fa-plus" /> &nbsp; {t('Setting')}
            </Button>
          </Col>
        </Row>
        { this.state.showModal &&
          <ControlModal
            onHide={this.toggleModal.bind(this)}
          />
        }
      </div>
    );
  }
}

ButtonControl.propTypes = propTypes;
ButtonControl.defaultProps = defaultProps;
