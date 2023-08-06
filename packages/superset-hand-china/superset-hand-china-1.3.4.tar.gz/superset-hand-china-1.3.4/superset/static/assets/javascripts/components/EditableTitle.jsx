import React from 'react';
import PropTypes from 'prop-types';
import { Button, Modal } from 'react-bootstrap';

import TooltipWrapper from './TooltipWrapper';
import { t } from '../locales';

const propTypes = {
  title: PropTypes.string,
  canEdit: PropTypes.bool,
  showHeaderModal: PropTypes.string,
  onSaveTitle: PropTypes.func.isRequired,
};
const defaultProps = {
  title: t('Title'),
  canEdit: false,
  showHeaderModal: 'TitleHeader',
};

class EditableTitle extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      isEditing: false,
      modalShow: false,
      noEmptyShow: false,
      title: this.props.title,
      lastTitle: this.props.title,
    };
    this.handleClick = this.handleClick.bind(this);
    this.handleBlur = this.handleBlur.bind(this);
    this.handleChange = this.handleChange.bind(this);
    this.handleKeyPress = this.handleKeyPress.bind(this);
  }
  handleClick() {
    if (!this.props.canEdit) {
      return;
    }

    this.setState({
      isEditing: true,
    });
  }
  handleBlur() {
    if (!this.props.canEdit) {
      return;
    }

    this.setState({
      isEditing: false,
    });

    if (this.state.lastTitle !== this.state.title) {
      if (this.state.title === '') {
        this.setState({ noEmptyShow: true });
      } else {
        if (this.props.showHeaderModal === 'Dashboard') {
          const _this = this;
          const dashboardTitle = this.state.title;
          $.ajax({
            type: 'get',
            url: '/hand/queryDashboardData',
            dataType: 'json',
            success: function (data) {
              _this.setState({ modalShow: false });
              for (let i = 0; i < data.length; i++) {
                if (dashboardTitle === data[i].dashboard_title) {
                  _this.setState({ modalShow: true });
                }
              }
              if (_this.state.modalShow === false) {
                _this.setState({
                  lastTitle: _this.state.title,
                });
                _this.props.onSaveTitle(_this.state.title);
              }
            },
            error: function (error) {
              console.info(error);
            },
          });
        } else if (this.props.showHeaderModal === 'Slice') {
          const _this = this;
          const sliceTitle = this.state.title;
          $.ajax({
            type: 'get',
            url: '/hand/querySliceData',
            dataType: 'json',
            success: function (data) {
              _this.setState({ modalShow: false });
              for (let i = 0; i < data.length; i++) {
                if (sliceTitle === data[i].slice_name) {
                  _this.setState({ modalShow: true });
                }
              }
              if (_this.state.modalShow === false) {
                _this.setState({
                  lastTitle: _this.state.title,
                });
                _this.props.onSaveTitle(_this.state.title);
              }
            },
            error: function (error) {
              console.info(error);
            },
          });
        } else {
          this.setState({
            lastTitle: this.state.title,
          });
          this.props.onSaveTitle(this.state.title);
        }
      }
    }
  }
  handleChange(ev) {
    if (!this.props.canEdit) {
      return;
    }

    this.setState({
      title: ev.target.value,
    });
  }
  handleKeyPress(ev) {
    if (ev.key === 'Enter') {
      ev.preventDefault();

      this.handleBlur();
    }
  }
  render() {
    let showModalTitle = this.props.showHeaderModal;
    if (this.props.showHeaderModal === 'Dashboard') {
      showModalTitle = t('Dashboard Name already exists');
    } else if(this.props.showHeaderModal === 'Slice') {
      showModalTitle = t('Slice Name already exists');
    }
    return (
      <span className="editable-title">
        <TooltipWrapper
          label="title"
          tooltip={this.props.canEdit ? t('click to edit title') : t('You don\'t have the rights to alter this title.')}
        >
          <input
            required
            type={this.state.isEditing ? 'text' : 'button'}
            value={this.state.title}
            onChange={this.handleChange}
            onBlur={this.handleBlur}
            onClick={this.handleClick}
            onKeyPress={this.handleKeyPress}
          />
        </TooltipWrapper>
        <Modal show={this.state.modalShow} onHide={() => this.setState({ modalShow: false})}>
          <Modal.Header>
            <Modal.Title>{showModalTitle}</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            {`${showModalTitle}` + t('Please change it.')}
          </Modal.Body>
          <Modal.Footer>
            <Button
              onClick={() => this.setState({ modalShow: false})}
              bsStyle="primary"
            >
              {t('OK')}
            </Button>
          </Modal.Footer>
        </Modal>
        <Modal show={this.state.noEmptyShow} onHide={() => this.setState({ noEmptyShow: false})}>
          <Modal.Body>
            {t('Title can\'t be empty, Please change it.')}
          </Modal.Body>
          <Modal.Footer>
            <Button
              onClick={() => this.setState({ noEmptyShow: false})}
              bsStyle="primary"
            >
              {t('OK')}
            </Button>
          </Modal.Footer>
        </Modal>
      </span>
    );
  }
}
EditableTitle.propTypes = propTypes;
EditableTitle.defaultProps = defaultProps;

export default EditableTitle;
