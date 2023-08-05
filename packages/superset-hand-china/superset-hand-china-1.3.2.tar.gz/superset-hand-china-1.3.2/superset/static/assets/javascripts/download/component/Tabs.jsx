import React from 'react';
import { render } from 'react-dom';
import PropTypes from 'prop-types';
import { Table, Tabs, Button, Modal } from 'antd';

import { t } from '../../locales';

const TabPane = Tabs.TabPane;
const $ = window.$ = require('jquery');

const propTypes = {
  activeKey: PropTypes.string.isRequired,
  changeActiveKey: PropTypes.func.isRequired,
  sliceId: PropTypes.number.isRequired,
  viewQuery: PropTypes.func.isRequired,
  columns: PropTypes.array.isRequired,
  data: PropTypes.array.isRequired,
}

export default class Tables extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      history_columns: [{
        title: t('sql'),
        dataIndex: 'sql',
        key: 'sql',
        width: '60%',
        render: (name, record) => {
          return (
            <p onClick={this.viewSql.bind(this, name)} style={{ cursor: 'pointer' }}>
              {name.substr(0, 80) + '{...}'}
            </p>
          );
        }
      }, {
        title: t('query_time'),
        dataIndex: 'query_time',
        key: 'query_time',
        width: '20%',
      }, {
        title: t('action'),
        dataIndex: 'action',
        key: 'action',
        width: '20%',
        render: (name, record) => {
          return (
            <div>
              <Button
                type="primary"
                onClick={this.viewQuery.bind(this, record)}
              >
                {t('View')}
              </Button>
              <Button
                style={{ marginLeft: 15 }}
                type="primary"
                onClick={this.download.bind(this, record)}
              >
                {t('Download')}
              </Button>
            </div>
          );
        }
      }],
      history_data: [],
    }
  }

  viewSql(sql) {
    Modal.info({
      width: 800,
      title: 'SQL',
      content: (
        <div>
          {sql}
        </div>
      ),
    });
  }

  viewQuery(query) {
    this.props.viewQuery(query.query_json_url, query.columns);
  }

  download(query) {
    location.href = query.export_json_url + '&csv=true';
  }

  changeActiveKey(key) {
    const _this = this;
    if (key === '2') {
      $.get('/hand/getDownloadQueryHistory/' + this.props.sliceId, function(data) {
        _this.setState({history_data: JSON.parse(data)});
      });
    }
    this.props.changeActiveKey(key);
  }

  render() {
    const tableWidth = 200 * this.props.columns.length;
    return (
      <div style={{ margin: '0 0 10 15', clear: 'both', background: '#eee', padding: 10 }}>
        <Tabs
          activeKey={this.props.activeKey}
          type="card"
          onChange={this.changeActiveKey.bind(this)}
        >
          <TabPane tab={t('Result')} key="1">
            <div style={{ width: '100%', height: 220, overflow: 'auto' }}>
              <div style={{ width: tableWidth < window.screen.availWidth ? '100%' : tableWidth }}>
                <Table
                  size="small"
                  pagination={false}
                  columns={this.props.columns}
                  dataSource={this.props.data}
                />
              </div>
            </div>
          </TabPane>
          <TabPane tab={t('Result History')} key="2">
            <Table
              scroll={{ y: 200 }}
              size="small"
              pagination={{ pageSize: 5}}
              columns={this.state.history_columns}
              dataSource={this.state.history_data}
            />
          </TabPane>
        </Tabs>
      </div>
    )
  }
}

Tables.propTypes = propTypes;