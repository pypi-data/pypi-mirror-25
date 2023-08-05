// JS
import d3 from 'd3';
import React from 'react';
import PropTypes from 'prop-types';
import ReactDOM from 'react-dom';

// antd
import { Select, Button } from 'antd';
import { t } from '../../javascripts/locales';
import '../filter_box.css';

const propTypes = {
  origSelectedValues: PropTypes.object,
  instantFiltering: PropTypes.bool,
  onChange: PropTypes.func,
  datasource: PropTypes.object.isRequired,
  formData: PropTypes.object.isRequired,
  payload: PropTypes.object.isRequired,
  is_child: PropTypes.bool.isRequired,
};

const defaultProps = {
  origSelectedValues: {},
  onChange: () => { },
  showDateFilter: false,
  instantFiltering: true,
};

let data = [];

// data[0] = ['仙侠', '二次元'];
// data[1] = {
//   '仙侠': ['龙之宫', '黑X白', '黄庭立道', '魔法使之夜'],
//   '二次元': ['诡道荒行', '让钞票在飞'],
// };
// data[2] = {
//   '龙之宫': ['1', '2', '3'],
//   '黑X白': ['4', '5', '6'],
//   '黄庭立道': ['10', '20', '50', '60'],
//   '魔法使之夜': ['11', '22', '33'],
//   '诡道荒行': ['6', '7', '8'],
//   '让钞票在飞': ['1', '2'],
// }


class FilterBoxCascade extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      selectedValues: props.origSelectedValues,
      hasChanged: false,
      filterFrozen: false,
      options: [],
      values: [], 
    };
  }

  componentWillMount() {
    // console.info(this.props.formData)
    // init data
    this.props.formData.groupby.forEach((g, index) => {
      data[index] = index === 0 ? [] : {};  
    })
    this.props.formData.cascade.forEach(c => {
      if (c.level === 1) {
        data[c.level - 1] = c.childNodes.split(',');
      } else {
        data[c.level - 1][c.parentNode] = c.childNodes.split(',');
      }
    });
    console.info(data)

    // init options and values(prompt or default)
    const options = [], values = [];
    let promptValue = null;
    for (let i = 0; i < this.props.formData.groupby.length; i++) {
      try {
        promptValue = this.props.origSelectedValues[this.props.formData.groupby[i]][0];
      } catch (error) {
        console.info(error)
      }
      if (i === 0) {
        options[i] = data[i];
      } else if (i === 1) {
        options[i] = data[i][values[i-1]] || data[i][data[i-1][0]];
      } else {
        options[i] = data[i][data[i-1][values[i-1]]] || data[i][data[i-1][Object.keys(data[i-1])[0]][0]];
      }
      values[i] = promptValue || options[i][0];
    }
    this.setState({
      options: options,
      values: values,
    });
  }

  clickApply() {
    this.props.onChange(null, [], true, true);
    this.setState({ hasChanged: false });
  }

  handleChange(index, value) {
    // console.info(index, value);
    const v = this.state.values;
    // set self value
    v[index] = value; 
    this.setState({ values: v});

    // change child options
    for (let i = index + 1; i < this.props.formData.groupby.length; i++) {
      const o = this.state.options;
      if (i === index + 1) {
        o[i] = data[i][value];
      } else {
        o[i] = data[i][o[i-1][0]];
      }
      this.setState({ options: o })
    }

    // change child value
    for (let i = index + 1; i < this.props.formData.groupby.length; i++) {
      const v = this.state.values;
      v[i] = data[i][v[i-1]][0];
      this.setState({ values: v});
    }

    this.setState({ hasChanged: true });

    // change prompt(all values)
    for (let i = 0; i < this.props.formData.groupby.length; i++) {
      if (this.props.is_child) {
        this.props.onChange(this.props.formData.groupby[i], [this.state.values[i]], false, false);
      } else {
        this.props.onChange(this.props.formData.groupby[i], [this.state.values[i]], false, this.props.instantFiltering);
      }
    }
  }

  render() {
    // console.info(this.state.values)
    // console.info(this.state.options)
    const fd = this.props.formData;
    const selects = [];
    for (let i = 0; i < fd.groupby.length; i++) {
      let choiceOptions = this.state.options[i].map(k => <Option key={k}>{k}</Option>);
      selects.push(
        <div className="m-b-5" 
          style={{ width: fd.width==='' ? '100%' : fd.width, float: 'left', fontSize: '12px' }}
        >
          <div style={{ marginLeft: 15 }}>
            {fd.groupby[i]}
            <br />
            <Select
              style={{ width: '100%' }}
              value={this.state.values[i]}
              onChange={this.handleChange.bind(this, i)}
            >
              {choiceOptions}
            </Select>
          </div>
        </div>
      )
    }

    return (
      <div>
        {selects}
        {!this.props.instantFiltering && !this.props.is_child &&
          <div>
            <Button
              disabled={!this.state.hasChanged}
              style={{ marginLeft: 15, width: 65, height: 25, marginTop:20, float:'left'}}
              type="primary"
              icon="search"
              size="small"
              onClick={this.clickApply.bind(this)}
            >
              {t('Query')}
            </Button>
          </div>
        }
      </div>
    );
  }
}

FilterBoxCascade.propTypes = propTypes;
FilterBoxCascade.defaultProps = defaultProps;

function filterBoxCascade(slice, payload) {
  const d3token = d3.select(slice.selector);
  d3token.selectAll('*').remove();

  const fd = slice.formData;
  const is_child = fd.is_child ? true : false;
  // console.info(is_child)
  ReactDOM.render(
    <FilterBoxCascade
      onChange={slice.addFilter}
      datasource={slice.datasource}
      origSelectedValues={slice.getFilters() || {}}
      instantFiltering={fd.instant_filtering}
      formData={fd}
      payload={payload}
      is_child={is_child}
    />,
    document.getElementById(slice.containerId),
  );
}

module.exports = filterBoxCascade;
