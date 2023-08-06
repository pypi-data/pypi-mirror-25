import React from 'react';
import { render } from 'react-dom';

import List from './components/List';
import Add from './components/Add';
import Modify from './components/Modify';
import { MailForm } from './components/Mail';

const $ = window.$ = require('jquery');
const jQuery = window.jQuery = $; // eslint-disable-line
require('bootstrap');

const appContainer = document.getElementById('app');
const bootstrapData = JSON.parse(appContainer.getAttribute('data-bootstrap'));

const state = Object.assign({},
  {
    type: bootstrapData.type,
    schedulers: bootstrapData.schedulers,
    dashboards: bootstrapData.dashboards,
    scheduler: bootstrapData.scheduler,
    condition: bootstrapData.condition,
    slices: bootstrapData.slices,
    mailPage: bootstrapData.mailPage,
    mail: bootstrapData.mail,
  }
);

if (state.type === 'list') {
  render(
    <List form_data={state} />,
    appContainer
  );
} else if (state.type === 'add') {
  render(
    <Add form_data={state} />,
    appContainer
  );
} else if (state.type === 'modify') {
  render(
    <Modify form_data={state} />,
    appContainer
  );
} else if (state.mailPage === 'true') {
  render(
    <MailForm form_data={state} />,
    appContainer
  );
}
