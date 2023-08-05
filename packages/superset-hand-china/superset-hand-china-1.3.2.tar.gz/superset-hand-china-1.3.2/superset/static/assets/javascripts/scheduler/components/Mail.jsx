import React from 'react';
import { Form, Input, InputNumber, Button, Modal, Message } from 'antd';
import { t } from '../../locales';

const FormItem = Form.Item;
const $ = window.$ = require('jquery');

class Mail extends React.Component  {

  constructor(props) {
    super(props);
    this.state = {
      visible: false,
    }
  }

  modify(e) {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        console.log('Received values of form: ', values);
        let operate = 'add';
        if (this.props.form_data.mail !== null) {
          operate = 'modify';
          values['id'] = this.props.form_data.mail.id;
        }
        $.ajax({
          type: 'POST',
          url: '/hand/email/' + operate,
          data: values,
          dataType: 'json',
          success: function (data) {
            let operate1;
            if(operate === 'show'){
              operate1 = t('show');
            } else if(operate === 'add'){
              operate1 = t('add');
            } else if(operate === 'modify'){
              operate1 = t('modify');
            }
            if (data.status === 'true') {
              Modal.success({
                title: operate1 + t(' success'),
                onOk() {
                  if (operate === 'add') {
                    location.href = '/hand/email/show';
                  }
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
                title: t('unknow eror'),
              });
          },
        });
      }
    });
  }

  testConn(e) {
    e.preventDefault();
    this.props.form.validateFields((err, values) => {
      if (!err) {
        console.log('Received values of form: ', values);
        if (this.props.form_data.mail !== null) {
          values['password'] = this.props.form_data.mail.password;
        }
        $.ajax({
          type: 'POST',
          url: '/hand/testMail',
          data: values,
          dataType: 'json',
          success: function (data) {
            if (data) {
              Modal.success({
                title: t('connect success'),
              });
            } else {
              Modal.error({
                title: t('connect failed'),
                content: t('caused by') + data,
              });
            }
          },
          error: function (xhr, error) {
            Modal.error({
              title: t('connect failed'),
              content: t('caused by') + xhr.responseText,
            });
          },
        });
      }
    });
  }

  showModal(e) {
    this.setState({
      visible: true
    });
  }

  handleOk(e) {
    const password = $('#password').val();
    const _this = this;
    if (password.length < 6) {
      Message.warn(t('Password length must be greater than 6 characters '));
      return;
    }
    $.ajax({
      type: 'POST',
        url: '/hand/resetMailPassword',
        data: {
          id: this.props.form_data.mail.id,
          password: password
        },
        dataType: 'json',
        success: function (data) {
          if (data) {
            Message.success(t('reset password success'));
            setTimeout(function() {
              location.reload();
            }, 500);
          } else {
            Message.error(t('reset password failed'));
          }
        },
        error: function () {
          Message.error(t('unknown error'));
        },
    });
  }

  handleCancel() {
    this.setState({
      visible: false
    });
  }

  render() {
    // console.info(this.props.form_data);
    const mail = this.props.form_data.mail;
    const { getFieldDecorator } = this.props.form;
    const formItemLayout = {
      labelCol: {
        xs: { span: 24 },
        sm: { span: 6 },
      },
      wrapperCol: {
        xs: { span: 24 },
        sm: { span: 14 },
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
      <div>
        <Form style={{ width: '50%' }}>
          <FormItem
            {...formItemLayout}
            label={t('smtp_server')}
            hasFeedback
          >
            {getFieldDecorator('smtp_server', {
              initialValue: mail === null ? null : mail.smtp_server,
              rules: [{
                required: true, message: t('Please input smtp server!'),
              }],
            })(
              <Input />
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label={t('port')}
            hasFeedback
          >
            {getFieldDecorator('port', {
              initialValue: mail === null ? 25 : mail.port,
              rules: [{
                required: true, message: t('Please input port!'),
              }],
            })(
              <InputNumber min={1} />
            )}
          </FormItem>
          <FormItem
            {...formItemLayout}
            label={t('email')}
            hasFeedback
          >
            {getFieldDecorator('email', {
              initialValue: mail === null ? null : mail.email,
              rules: [{
                type: 'email', message: t('The input is not valid E-mail!'),
              }, {
                required: true, message: t('Please input E-mail!'),
              }],
            })(
              <Input />
            )}
          </FormItem>
          { mail === null &&
            <FormItem
              {...formItemLayout}
              label={t('Password')}
              hasFeedback
            >
              {getFieldDecorator('password', {
                initialValue: null,
                rules: [{
                  required: true, message: t('Please input your password!'),
                }, {
                  validator: this.checkConfirm,
                }],
              })(
                <Input type="password" />
              )}
            </FormItem>
          }
          <FormItem
            {...tailFormItemLayout}
          >
            <Button style={{ backgroundColor: '#00A699' }} type="primary" onClick={ this.testConn.bind(this) }>{t('Test Connection')}</Button>
            <Button style={{ marginLeft: 15, backgroundColor: '#00A699' }} type="primary" onClick={ this.modify.bind(this) }>{t('Save')}</Button>
            {  mail !== null &&
              <Button style={{ marginLeft: 15, backgroundColor: '#00A699' }} type="primary" onClick={ this.showModal.bind(this) }>{t('resetPassword')}</Button>
            }
          </FormItem>
        </Form>
        <Modal
          title={t('Basic Modal')}
          visible={this.state.visible}
          onOk={this.handleOk.bind(this)}
          onCancel={this.handleCancel.bind(this)}
          footer={[
            <Button key="back" size="large" onClick={this.handleCancel.bind(this)}>{t('Cancel')}</Button>,
            <Button key="submit" type="primary" size="large" onClick={this.handleOk.bind(this)}>
              {t('Submit')}
            </Button>,
          ]}
        >
          <label>{t('Password:')}</label>
          <Input  id="password" type="password" />
        </Modal>
      </div>
    );
  }
}

export const MailForm = Form.create()(Mail);
