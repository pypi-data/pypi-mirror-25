import React from 'react';
import { Form, Input, Button, Select, Modal } from 'antd';
const FormItem = Form.Item;
const Option = Select.Option;
const { TextArea } = Input;
const $ = window.$ = require('jquery');

class Condition extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      sliceOptions: null,
      metricOptions: null,
      title: null,
      dashboardId: null,
      sliceId: null,
      metric: null,
      expr: null,
      sendSliceId: null,
      receiveAddress: null,
    }
    if (this.props.type === 'modify') {
      // init sliceOptions and metricOptions
      let sliceOptions, metricOptions;
      this.props.form_data.dashboards.forEach(d => {
        if (d.id === this.props.form_data.condition.dashboard_id) {
          sliceOptions = d.slices.map(s => <Option key={s.id}>{s.name}</Option>);
        }
      });
      this.props.form_data.slices.forEach(s => {
        if (s.id === this.props.form_data.condition.slice_id) {
          metricOptions = s.metrics.map(m => <Option key={m}>{m}</Option>);
        }
      });
      this.state = {
        sliceOptions: sliceOptions,
        metricOptions: metricOptions,
        title: this.props.form_data.condition.description,
        dashboardId: this.props.form_data.condition.dashboard_id.toString(),
        sliceId: this.props.form_data.condition.slice_id.toString(),
        metric: this.props.form_data.condition.metric,
        expr: this.props.form_data.condition.expr,
        sendSliceId: this.props.form_data.condition.send_slice_id.toString(),
        receiveAddress: this.props.form_data.condition.receive_address,
      }
    }
  }

  changeDashboard(id) {
    this.props.form_data.dashboards.forEach(d => {
      if (d.id.toString() === id) {
        this.setState({
          sliceOptions: d.slices.map(s => <Option key={s.id}>{s.name}</Option>)
        });
        this.props.form.setFieldsValue({slice_id: null, metric: null, send_slice_id: null});
      }
    });
  }

  changeSlice(id) {
    this.props.form_data.slices.forEach(s => {
      if (s.id.toString() === id) {
        this.setState({
          metricOptions: s.metrics.map(m => <Option key={m}>{m}</Option>)
        });
        this.props.form.setFieldsValue({metric: null});
      }
    });
  }

  save(e) {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        console.log('Received values of form: ', values);
        if (this.props.type === 'insert') {
          values['scheduler_id'] = this.props.schedulerId;
        } else {
          values['id'] = this.props.form_data.condition.id;
        }
        $.ajax({
          type: 'POST',
          url: '/hand/insertOrModifyCondition/' + this.props.type,
          data: values,
          dataType: 'json',
          success: function (data) {
            if (data.status === 'true') {
              Modal.success({
                title: 'save success',
                onOk() {
                  location.href = '/hand/mySchedulers/list/1';
                }
              });
              
            } else {
              Modal.error({
                title: 'save failed',
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
    });
  }

  render() {
    // console.info(this.props.form_data);
    const { getFieldDecorator } = this.props.form;
    const dashboardOptions = this.props.form_data.dashboards.map(d => <Option key={d.id}>{d.name}</Option>);
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
          <h3>Condition Setting</h3>
        </FormItem>
        <FormItem
          {...formItemLayout}
          label="title"
          hasFeedback
        >
          {getFieldDecorator('description', {
            initialValue: this.state.title,
            rules: [{
              required: true, message: 'Please input title!',
            }],
          })(
            <Input placeholder="please input title" disabled={ this.props.disabled }/>
          )}
        </FormItem>
        <FormItem
          {...formItemLayout}
          label="dashboard"
          hasFeedback
        >
          {getFieldDecorator('dashboard_id', {
            initialValue: this.state.dashboardId,
            rules: [{
              required: true, message: 'Please select dashboard!',
            }],
          })(
            <Select onChange={ this.changeDashboard.bind(this) } disabled={ this.props.disabled }>
              {dashboardOptions}
            </Select>
          )}
        </FormItem>
        <FormItem
          {...formItemLayout}
          label="slice"
          hasFeedback
        >
          {getFieldDecorator('slice_id', {
            initialValue: this.state.sliceId,
            rules: [{
              required: true, message: 'Please select slice!',
            }],
          })(
            <Select onChange={ this.changeSlice.bind(this) } disabled={ this.props.disabled }>
              {this.state.sliceOptions}
            </Select>
          )}
        </FormItem>
        <FormItem
          {...formItemLayout}
          label="metric"
          hasFeedback
        >
          {getFieldDecorator('metric', {
            initialValue: this.state.metric,
            rules: [{
              required: true, message: 'Please select metric!',
            }],
          })(
            <Select disabled={ this.props.disabled }>
              {this.state.metricOptions}
            </Select>
          )}
        </FormItem>
        <FormItem
          {...formItemLayout}
          label="condition"
          hasFeedback
        >
          {getFieldDecorator('expr', {
            initialValue: this.state.expr,
            rules: [{
              required: true, message: 'Please input expression!',
            }],
          })(
            <Input placeholder="use x to replace metric"  disabled={ this.props.disabled } />
          )}
        </FormItem>
        <FormItem
          {...formItemLayout}
          label="send slice"
          hasFeedback
        >
          {getFieldDecorator('send_slice_id', {
            initialValue: this.state.sendSliceId,
            rules: [{
              required: true, message: 'Please select send slice!',
            }],
          })(
            <Select disabled={ this.props.disabled }>
              {this.state.sliceOptions}
            </Select>
          )}
        </FormItem>
        <FormItem
          {...formItemLayout}
          label="receive address"
          hasFeedback
        >
          {getFieldDecorator('receive_address', {
            initialValue: this.state.receiveAddress,
            rules: [{
              required: true, message: 'Please input receive address!',
            }],
          })(
            <TextArea
              disabled={ this.props.disabled }
              placeholder="email address, separated by a comma"
              autosize={{ minRows: 4, maxRows: 8 }} />
          )}
        </FormItem>
        <FormItem
          {...tailFormItemLayout}
        >
          <Button
            type="primary"
            disabled={ this.props.disabled }
            onClick={ this.save.bind(this) }
          >
            save
          </Button>
        </FormItem>
      </Form>
    )
  }
}

export const ConditionForm = Form.create()(Condition);