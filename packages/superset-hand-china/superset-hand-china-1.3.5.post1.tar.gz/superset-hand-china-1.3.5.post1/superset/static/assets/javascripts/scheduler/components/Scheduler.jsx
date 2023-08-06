import React from 'react';
import { Form, Input, Button, Select, Modal } from 'antd';
import { t } from '../../locales';

const FormItem = Form.Item;
const Option = Select.Option;
const { TextArea } = Input;
const $ = window.$ = require('jquery');

class Scheduler extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      mode: null,
      expr: null
    }
    if (this.props.type === 'modify') {
      this.state = {
        mode: this.props.form_data.scheduler.mode,
        expr: this.parseExpr()
      }
    }
  }

  parseExpr() {
    const s = this.props.form_data.scheduler;
    if (s.mode === 'interval') {
      return s.interval_expr;
    } else if (s.mode === 'date') {
      return "run_date='" + s.date_run_date + "'";
    }
    // cron
    let str = '';
    if (s.cron_year != null) {
      str += "year='" + s.cron_year + "'\n&& ";
    }
    if (s.cron_month != null) {
      str += "month='" + s.cron_month + "'\n&& ";
    }
    if (s.cron_day != null) {
      str += "day='" + s.cron_day + "'\n&& ";
    }
    if (s.cron_week != null) {
      str += "week='" + s.cron_week + "'\n&& ";
    }
    if (s.cron_day_of_week != null) {
      str += "day_of_week='" + s.cron_day_of_week + "'\n&& ";
    }
    if (s.cron_hour != null) {
      str += "hour='" + s.cron_hour + "'\n&& ";
    }
    if (s.cron_minute != null) {
      str += "minute='" + s.cron_minute + "'\n&& ";
    }
    if (s.cron_second != null) {
      str += "second='" + s.cron_second + "'\n&& ";
    }
    return str.substring(0, str.length - 3);
  }

  save(e) {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        console.log('Received values of form: ', values);
        const _this = this;
        if (this.props.type === 'modify') {
          values['id'] = this.props.form_data.scheduler.id;
        }
        $.ajax({
          type: 'POST',
          url: '/hand/insertOrModifyScheduler/' + this.props.type,
          data: values,
          dataType: 'json',
          success: function (data) {
            if (data.status === 'true') {
              Modal.success({
                title: t('save success'),
                onOk() {
                  _this.props.changeDisabled(data.schedulerId);
                }
              });
            } else {
              Modal.error({
                title: t('save failed'),
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
    });
  }

  render() {
    // console.info(this.props.form_data);
    const { getFieldDecorator } = this.props.form;
    const formItemLayout = {
      labelCol: {
        xs: { span: 24 },
        sm: { span: 6 },
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 12 },
      },
    };
    const tailFormItemLayout = {
      wrapperCol: {
        xs: {
          span: 24,
          offset: 0,
        },
        sm: {
          span: 14,
          offset: 6,
        },
      },
    };
    return (
      <Form>
        <FormItem
          {...formItemLayout}
        >
          <h3>{t('Scheduler Setting')}</h3>
        </FormItem>
        <FormItem
          {...formItemLayout}
          label={t('scheduler mode')}
          hasFeedback
        >
          {getFieldDecorator('mode', {
            initialValue: this.state.mode,
            rules: [{
              required: true, message: t('Please select mode!'),
            }],
          })(
            <Select disabled={ this.props.disabled }>
              <Option value="interval">{t('interval')}</Option>
              <Option value="cron">{t('cron')}</Option>
              <Option value="date">{t('date')}</Option>
            </Select>
          )}
        </FormItem>
        <FormItem
          {...formItemLayout}
          label={t('scheduler expression')}
          hasFeedback
        >
          {getFieldDecorator('expr', {
            initialValue: this.state.expr,
            rules: [{
              required: true, message: t('Please input expression!'),
            }],
          })(
            <TextArea
               disabled={ this.props.disabled }
              placeholder={t('scheduler expression')}
              autosize={{ minRows: 4, maxRows: 8 }}
            />
          )}
        </FormItem>
        <FormItem
          {...tailFormItemLayout}
        >
          <p>{t('Note:Time use `YYYY-MM-DD hh:mm:ss` or `YYYY-MM-DD` string representation, multiple conditions use && connect')}</p>
          <a target="_blank" href="http://debugo.com/apscheduler/">{t('Scheduler Detail link')}</a>
        </FormItem>
        <FormItem
          {...tailFormItemLayout}
        >
          <Button
            disabled={ this.props.disabled }
            type="primary"
            onClick={ this.save.bind(this) }
          >
            {t('save')}
          </Button>
        </FormItem>
      </Form>
    )
  }
}

export const SchedulerForm = Form.create()(Scheduler);