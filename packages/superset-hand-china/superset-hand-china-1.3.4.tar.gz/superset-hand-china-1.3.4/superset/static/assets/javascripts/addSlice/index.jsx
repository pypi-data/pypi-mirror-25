import React from 'react';
import ReactDOM from 'react-dom';
import { appSetup } from '../common';
import AddSliceContainer from './AddSliceContainer';

appSetup();

const addSliceContainer = document.getElementById('app');
const bootstrapData = JSON.parse(addSliceContainer.getAttribute('data-bootstrap'));

ReactDOM.render(
  <AddSliceContainer datasources={bootstrapData.datasources} />,
  addSliceContainer,
);
