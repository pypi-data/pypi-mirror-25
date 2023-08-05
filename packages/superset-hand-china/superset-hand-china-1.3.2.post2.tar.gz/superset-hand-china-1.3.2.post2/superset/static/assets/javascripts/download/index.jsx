import React from 'react';
import { render } from 'react-dom';
import Download from './component/Download';
import { getInitialState, dashboardContainer } from './util.js';

const superset = require('../modules/superset');
const $ = window.$ = require('jquery');
const jQuery = window.jQuery = $; // eslint-disable-line
require('bootstrap');

let px;

const appContainer = document.getElementById('app');
const bootstrapData = JSON.parse(appContainer.getAttribute('data-bootstrap'));
const state = getInitialState(bootstrapData);
px = superset(state);

// get filter_combination_id
let filter_combination_id = null;
let filter_box_ids = [];
state.dashboard.slices.forEach(s => {
  if (s.form_data.viz_type === 'filter_box_combination') {
    filter_combination_id = s.slice_id;
    filter_box_ids = s.form_data.filter_combination;
  }
});

let dashboard = null;
if (filter_combination_id !== null && filter_box_ids.length !== 0) {
  $.ajax({
    url: '/hand/getSliceData?sliceIds=' + filter_box_ids.join(','),
    async: false,
    success: function(data) {
      const slices = JSON.parse(data);
      const state2 = getInitialState(slices);
      let mergeState = state;
      mergeState.dashboard.slices = state.dashboard.slices.concat(state2.dashboard.slices);
      mergeState.datasources = $.extend(state.datasources, state2.datasources);
      // console.info(mergeState)
      dashboard = dashboardContainer(mergeState.dashboard, mergeState.datasources, state.user_id, px);
      // console.info(sliceCombination)
      dashboard.init();
    }
  });
} else {
  dashboard = dashboardContainer(state.dashboard, state.datasources, state.user_id, px);
  dashboard.init();
}

// get url param
function getQueryString(name) {
  const reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
  const r = window.location.search.substr(1).match(reg);
  if (r != null) return unescape(r[2]);
  return null;
}

function hideTitle() {
  // hide header and title
  if (getQueryString('isTitle') === 'false') {
    $('#alert-container').hide();
    $('#dashboard-header .pull-left').hide();
  }
  if (getQueryString('isControl') === 'false') {
    $('#dashboard-header .pull-right').hide();
  }
}
hideTitle();

render(
    <Download dashboard={dashboard} />,
    appContainer
);
