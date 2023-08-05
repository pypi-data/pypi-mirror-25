import React from 'react';
import { Table, Icon, Button, Modal } from 'antd';

import { t } from '../../locales';

const $ = window.$ = require('jquery');

const propTypes = {
  form_data: React.PropTypes.object.isRequired,
};

export default class List extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
    };
  }

  parseExpr(s) {
    if (s.mode === 'interval') {
      return s.interval_expr;
    } else if (s.mode === 'date') {
      return "run_date='" + s.date_run_date + "'";
    }
    // cron
    let str = '';
    if (s.cron_year != null) {
      str += "year='" + s.cron_year + "',";
    }
    if (s.cron_month != null) {
      str += "month='" + s.cron_month + "',";
    }
    if (s.cron_day != null) {
      str += "day='" + s.cron_day + "',";
    }
    if (s.cron_week != null) {
      str += "week='" + s.cron_week + "',";
    }
    if (s.cron_day_of_week != null) {
      str += "day_of_week='" + s.cron_day_of_week + "',";
    }
    if (s.cron_hour != null) {
      str += "hour='" + s.cron_hour + "',";
    }
    if (s.cron_minute != null) {
      str += "minute='" + s.cron_minute + "',";
    }
    if (s.cron_second != null) {
      str += "second='" + s.cron_second + "',";
    }
    return str.substring(0, str.length - 1);
  }

  addScheduler() {
    location.href = '/hand/mySchedulers/add/1';
  }

  modifyScheduler(id) {
    location.href = '/hand/mySchedulers/modify/' + id;
  }

  operateJob(id, operate) {
    if (operate === 'delete') {
      const _this = this;
      Modal.confirm({
        title: t('Do you want to delete this scheduler?'),
        onOk() {
          _this.operate(id, operate);
        },
        onCancel() {
          return;
        },
      });
    } else {
      this.operate(id, operate);
    }
    
  }

  operate(id, operate) {
    $.ajax({
      type: 'get',
      url: '/hand/job/' + operate + '/' + id,
      dataType: 'json',
      success: function (data) {
        let operate1;
        if(operate === 'active'){
          operate1 = t('active');
        } else if(operate === 'delete'){
          operate1 = t('delete');
        } else if(operate === 'resume'){
          operate1 = t('resume');
        } else if(operate === 'pause'){
          operate1 = t('pause');
        }
        if (data) {
          Modal.success({
            title: operate1 + t(' success'),
            onOk() {
              location.href = '/hand/mySchedulers/list/1';
            }
          });
        } else {
          Modal.error({
            title: operate1 + t(' failed'),
          });
        }
      },
      error: function () {
        Modal.error({
          title: t('unknown error'),
        });
      },
    });
  }

  render() {
    const columns = [{
      title: t('description'),
      dataIndex: 'description',
      key: 'description',
      render: (text, record) => {
        return (<a href={'/hand/mySchedulers/modify/' + record.id}>{text}</a>);
      },
    }, {
      title: t('mode'),
      dataIndex: 'mode',
      key: 'mode',
    }, {
      title: t('expression'),
      dataIndex: 'expression',
      key: 'expression',
      render: (text, record) => { return this.parseExpr(record); }
    }, {
      title: t('start_date'),
      dataIndex: 'start_date',
      key: 'start_date',
    }, {
      title: t('end_date'),
      dataIndex: 'end_date',
      key: 'end_date',
    }, {
      title: t('is_active'),
      dataIndex: 'is_active',
      key: 'is_active',
      render: (text, record) => {
        return text ? <span style={{ color: 'green' }}>{t('true')}</span> : 
        (
          <Button
            type="primary"
            style={{  backgroundColor: '#37a14a' }}
            onClick={this.operateJob.bind(this, record.id, 'active')}
          >
            {t('active')}
          </Button>
        )
      }
    }, {
      title: t('is_running'),
      dataIndex: 'is_running',
      key: 'is_running',
      render: (text, record) => {
        if (record.mode !== 'date'
            || (record.mode === 'date' && new Date().getTime() < new Date(record.date_run_date).getTime())
        ) {
          if (!record.is_active) {
            return (
              <div>
                <Button disabled="disabled">{t('stop')}</Button>
                <Button disabled="disabled" style={{ marginLeft: '20px' }}>{t('start')}</Button>
              </div>
            );
          }
          if (text) {
            return (
              <div>
                <Button
                  type="danger"
                  style={{ background: 'red', color: 'white' }}
                  onClick={this.operateJob.bind(this, record.id, 'pause')}
                >
                  {t('stop')}
                </Button>
                <Button disabled="disabled" style={{ marginLeft: '20px' }}>{t('start')}</Button>
              </div>
            );
          } else {
            return (
              <div>
                <Button disabled="disabled">{t('stop')}</Button>
                <Button
                  type="primary"
                  style={{ marginLeft: '20px', backgroundColor: '#00A699' }}
                  onClick={this.operateJob.bind(this, record.id, 'resume')}
                >
                  {t('start')}
                </Button>
              </div>
            );
          }
        } else {
          // the date scheduler has started
          return (
            <div>
              <Button disabled="disabled">{t('stop')}</Button>
              <Button disabled="disabled" style={{ marginLeft: '20px' }}>{t('start')}</Button>
            </div>
          );
        }
      }
    }, {
      title: t('actions'),
      dataIndex: 'actions',
      key: 'actions',
      render: (text, record) => {
        return (
          <div>
            <Button
              type="primary"
              onClick={this.modifyScheduler.bind(this, record.id)}
            >
              {t('modify')}
            </Button>
            <Button
              type="danger"
              style={{ marginLeft: '20px', background: 'red', color: 'white' }}
              onClick={this.operateJob.bind(this, record.id, 'delete')}
            >
              {t('delete')}
            </Button>
          </div>
        );
      }
    }];

    return (
      <div style={{ width: '98%' }}>
        <Button
          type="primary"
          style={{ marginLeft: 20, marginBottom: 10, backgroundColor: '#00A699' }}
          onClick={this.addScheduler.bind(this)}
        >
          {t('add schedule')}
        </Button>
        <Table
          style={{ marginLeft: 20 }}
          size='small'
          columns={columns}
          dataSource={this.props.form_data.schedulers}
        />
      </div>
    );
  }
}

List.propTypes = propTypes;
