import React from 'react';
import PropTypes from 'prop-types';
import { Button, Row, Col } from 'react-bootstrap';
import { t } from '../../../../../locales';
import ColStyle from './ColStyle';

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

export default class ColStyleControl extends React.Component {
  addColStyle() {
    const newColStyles = Object.assign([], this.props.value);
    newColStyles.push({
      col: '',
      style: '',
    });
    this.props.onChange(newColStyles);
  }
  changeColStyle(index, control, value) {
    const newColStyles = Object.assign([], this.props.value);
    const modifiedColStyle = Object.assign({}, newColStyles[index]);
    if (typeof control === 'string') {
      modifiedColStyle[control] = value;
    } else {
      control.forEach((c, i) => {
        modifiedColStyle[c] = value[i];
      });
    }
    newColStyles.splice(index, 1, modifiedColStyle);
    this.props.onChange(newColStyles);
  }
  removeColStyle(index) {
    this.props.onChange(this.props.value.filter((f, i) => i !== index));
  }
  render() {
    const colStyles = this.props.value.map((colStyle, i) => (
      <div key={i}>
        <ColStyle
          colStyle={colStyle}
          datasource={this.props.datasource}
          removeColStyle={this.removeColStyle.bind(this, i)}
          changeColStyle={this.changeColStyle.bind(this, i)}
        />
      </div>
    ));
    return (
      <div>
        <div><hr style={{ borderTop: '1px solid rgb(85, 85, 85)' }}/></div>
        {colStyles}
        <Row className="space-2">
          <Col md={2} >
            <Button
              id="add-button"
              bsSize="sm"
              onClick={this.addColStyle.bind(this)}
            >
              <i className="fa fa-plus" /> &nbsp; {t('Add ColStyle')}
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

ColStyleControl.propTypes = propTypes;
ColStyleControl.defaultProps = defaultProps;
