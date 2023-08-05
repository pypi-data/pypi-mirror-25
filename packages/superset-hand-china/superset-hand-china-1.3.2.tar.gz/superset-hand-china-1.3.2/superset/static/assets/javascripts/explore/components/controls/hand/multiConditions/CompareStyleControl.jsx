import React from 'react';
import PropTypes from 'prop-types';
import { Button, Row, Col } from 'react-bootstrap';
import { t } from '../../../../../locales';
import CompareStyle from './CompareStyle';

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

export default class CompareStyleControl extends React.Component {
  addCompareStyle() {
    const newCompareStyles = Object.assign([], this.props.value);
    newCompareStyles.push({
      metric1: '',
      metric2: '',
      expr: '',
      style: '',
    });
    this.props.onChange(newCompareStyles);
  }
  changeCompareStyle(index, control, value) {
    const newCompareStyles = Object.assign([], this.props.value);
    const modifiedCompareStyle = Object.assign({}, newCompareStyles[index]);
    if (typeof control === 'string') {
      modifiedCompareStyle[control] = value;
    } else {
      control.forEach((c, i) => {
        modifiedCompareStyle[c] = value[i];
      });
    }
    newCompareStyles.splice(index, 1, modifiedCompareStyle);
    this.props.onChange(newCompareStyles);
  }
  removeCompareStyle(index) {
    this.props.onChange(this.props.value.filter((f, i) => i !== index));
  }
  render() {
    const compareStyles = this.props.value.map((compareStyle, i) => (
      <div key={i}>
        <CompareStyle
          compareStyle={compareStyle}
          datasource={this.props.datasource}
          removeCompareStyle={this.removeCompareStyle.bind(this, i)}
          changeCompareStyle={this.changeCompareStyle.bind(this, i)}
        />
      </div>
    ));
    return (
      <div>
        {compareStyles}
        <Row className="space-2">
          <Col md={2}>
            <Button
              id="add-button"
              bsSize="sm"
              onClick={this.addCompareStyle.bind(this)}
            >
              <i className="fa fa-plus" /> &nbsp; {t('Add CompareStyle')}
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

CompareStyleControl.propTypes = propTypes;
CompareStyleControl.defaultProps = defaultProps;
