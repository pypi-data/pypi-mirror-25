import React from 'react';
import { Table, Icon, Button, Modal } from 'antd';

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
        title: 'Do you want to delete this scheduler?',
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
        if (data) {
          Modal.success({
            title: operate + ' success',
            onOk() {
              location.href = '/hand/mySchedulers/list/1';
            }
          });
        } else {
          Modal.error({
            title: operate + ' failed',
          });
        }
      },
      error: function () {
        Modal.error({
          title: 'unknown error',
        });
      },
    });
  }

  render() {
    const columns = [{
      title: 'description',
      dataIndex: 'description',
      key: 'description',
      render: (text, record) => {
        return (<a href={'/hand/mySchedulers/modify/' + record.id}>{text}</a>);
      },
    }, {
      title: 'mode',
      dataIndex: 'mode',
      key: 'mode',
    }, {
      title: 'expression',
      dataIndex: 'expression',
      key: 'expression',
      render: (text, record) => { return this.parseExpr(record); }
    }, {
      title: 'start_date',
      dataIndex: 'start_date',
      key: 'start_date',
    }, {
      title: 'end_date',
      dataIndex: 'end_date',
      key: 'end_date',
    }, {
      title: 'is_active',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (text, record) => {
        return text ? <span style={{ color: 'green' }}>true</span> : 
        (
          <Button
            type="primary"
            style={{  backgroundColor: '#37a14a' }}
            onClick={this.operateJob.bind(this, record.id, 'active')}
          >
            active
          </Button>
        )
      }
    }, {
      title: 'is_running',
      dataIndex: 'is_running',
      key: 'is_running',
      render: (text, record) => {
        if (record.mode !== 'date'
            || (record.mode === 'date' && new Date().getTime() < new Date(record.date_run_date).getTime())
        ) {
          if (!record.is_active) {
            return (
              <div>
                <Button disabled="disabled">stop</Button>
                <Button disabled="disabled" style={{ marginLeft: '20px' }}>start</Button>
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
                  stop
                </Button>
                <Button disabled="disabled" style={{ marginLeft: '20px' }}>start</Button>
              </div>
            );
          } else {
            return (
              <div>
                <Button disabled="disabled">stop</Button>
                <Button
                  type="primary"
                  style={{ marginLeft: '20px', backgroundColor: '#00A699' }}
                  onClick={this.operateJob.bind(this, record.id, 'resume')}
                >
                  start
                </Button>
              </div>
            );
          }
        } else {
          // the date scheduler has started
          return (
            <div>
              <Button disabled="disabled">stop</Button>
              <Button disabled="disabled" style={{ marginLeft: '20px' }}>start</Button>
            </div>
          );
        }
      }
    }, {
      title: 'actions',
      dataIndex: 'actions',
      key: 'actions',
      render: (text, record) => {
        return (
          <div>
            <Button
              type="primary"
              onClick={this.modifyScheduler.bind(this, record.id)}
            >
              modify
            </Button>
            <Button
              type="danger"
              style={{ marginLeft: '20px', background: 'red', color: 'white' }}
              onClick={this.operateJob.bind(this, record.id, 'delete')}
            >
              delete
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
          add schedule
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
