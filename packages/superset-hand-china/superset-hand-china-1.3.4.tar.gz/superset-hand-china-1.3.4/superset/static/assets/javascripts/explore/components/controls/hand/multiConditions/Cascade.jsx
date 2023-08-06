import React from 'react';
import PropTypes from 'prop-types';
import Select from 'react-select';
import { Button, Row, Col } from 'react-bootstrap';
import { t } from '../../../../../locales';

const $ = window.$ = require('jquery');

const propTypes = {
  changeCascade: PropTypes.func,
  removeCascade: PropTypes.func,
  cascade: PropTypes.object.isRequired,
  datasource: PropTypes.object,
  having: PropTypes.bool,
  form_data: PropTypes.object,
  data: PropTypes.object,
};

const defaultProps = {
  changeCascade: () => { },
  removeCascade: () => { },
  datasource: null,
};

export default class Cascade extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      level: this.props.cascade.level,
      show_parent_node: true,
    };
  }
  
  changeLevel(value) {
    this.props.changeCascade('level', value);
    this.setState({ level: value });
  }
  changeParentNode(value) {
    this.props.changeCascade('parentNode', value);
  }
  changeChildNodes(value) {
    console.info(value)
    this.props.changeCascade('childNodes', value);
  }
  removeCascade(cascade) {
    this.props.removeCascade(cascade);
  }
  render() {
    const { datasource, cascade, form_data, data } = this.props;
    let levelChoices = [], parentNodeChoices = [], childNodeChoices = [];
    form_data.groupby.forEach((g, index) => {
      levelChoices.push({ value: (index + 1), label: 'level ' + (index + 1) });
    });

    // try{
      if (this.state.level > 1) {
        parentNodeChoices = data[form_data.groupby[this.state.level-2]].map(n => ({label: n, value: n}));
      }
      childNodeChoices = data[form_data.groupby[this.state.level-1]].map(n => ({label: n, value: n}));
    // } catch(error) {
    //   console.info(error)
    // }

    return (
      <div>
        <Row className="space-1">
          <Col md={6}>
            <label className="control-label">{t('Level:')}</label>
            <Select
              multi={false}
              simpleValue
              placeholder={t('Select Level')}
              options={levelChoices}
              clearable={false}
              value={cascade.level}
              onChange={this.changeLevel.bind(this)} 
            />
          </Col>
          {this.state.level > 1 &&
            <Col md={6}>
              <label className="control-label">{t('ParentNode:')}</label>
              <Select
                multi={false}
                simpleValue
                placeholder={t('Select ParentNode')}
                options={parentNodeChoices}
                clearable={false}
                value={cascade.parentNode}
                onChange={this.changeParentNode.bind(this)}
              />
            </Col>
          }
        </Row>
        <Row className="space-1">
          <Col md={11}>
            <label className="control-label">{t('ChildNodes:')}</label>
            <Select
              multi
              simpleValue
              placeholder={t('Select ChildNodes')}
              options={childNodeChoices}
              clearable={false}
              value={cascade.childNodes}
              onChange={this.changeChildNodes.bind(this)}
            />
          </Col>
          <Col md={1} style={{ marginTop: 30 }}>
            <Button
              id="remove-button"
              bsSize="small"
              onClick={this.removeCascade.bind(this)}
            >
              <i className="fa fa-minus" />
            </Button>
          </Col>
        </Row>
      </div>
    );
  }
}

Cascade.propTypes = propTypes;
Cascade.defaultProps = defaultProps;
