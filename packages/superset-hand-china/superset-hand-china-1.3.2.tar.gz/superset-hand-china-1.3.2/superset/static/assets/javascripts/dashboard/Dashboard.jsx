import React from 'react';
import { render } from 'react-dom';
import d3 from 'd3';
import { Alert } from 'react-bootstrap';
import moment from 'moment';

import GridLayout from './components/GridLayout';
import Header from './components/Header';
import { appSetup } from '../common';
import { t } from '../locales';
import AlertsWrapper from '../components/AlertsWrapper';

// import '../../stylesheets/dashboard.css';
import '../../stylesheets/hand/dashboard.css';

const superset = require('../modules/superset');
const urlLib = require('url');
const utils = require('../modules/utils');
require('bootstrap');
require('../../stylesheets/simple-line-icons/simple-line-icons.css')

let px;

appSetup();

let filter_combination_id = null;
let filter_box_ids = [];
export function getInitialState(boostrapData) {
  const dashboard = Object.assign(
    {},
    utils.controllerInterface,
    boostrapData.dashboard_data,
    { common: boostrapData.common });
  dashboard.firstLoad = true;

  dashboard.posDict = {};
  if (dashboard.position_json) {
    dashboard.position_json.forEach((position) => {
      dashboard.posDict[position.slice_id] = position;
    });
  }
  dashboard.refreshTimer = null;
  const themes = ['macarons', 'shine', 'dark', 'vintage', 'roma', 'infographic', 'westeros',
    'wonderland', 'chalk', 'essos', 'walden', 'purple-passion'];
  const sliceResizeAble = ['true', 'false'];
  const state = Object.assign({}, boostrapData, { dashboard }, { 'themes': themes },
    { 'sliceResizeAble': sliceResizeAble });
  return state;
}

function unload() {
  const message = t('You have unsaved changes.');
  window.event.returnValue = message; // Gecko + IE
  return message; // Gecko + Webkit, Safari, Chrome etc.
}

function onBeforeUnload(hasChanged) {
  if (hasChanged) {
    window.addEventListener('beforeunload', unload);
  } else {
    window.removeEventListener('beforeunload', unload);
  }
}

function renderAlert() {
  render(
    <div className="container-fluid">
      <Alert bsStyle="warning">
        <strong>{t('You have unsaved changes.')}</strong> {t('Click the')} &nbsp;
        <i className="fa fa-save" />&nbsp;
        {t('button on the top right to save your changes.')}
      </Alert>
    </div>,
    document.getElementById('alert-container'),
  );
}

function initDashboardView(dashboard, themes, sliceResizeAble) {
  const otherSlices = [];
  dashboard.slices.forEach(s => {
    if ($.inArray(s.slice_id, filter_box_ids) === -1) {
      otherSlices.push(s);
    }
  });
  dashboard.slices = otherSlices;
  dashboard.themes = themes;
  dashboard.sliceResizeAble = sliceResizeAble;
  // console.info(dashboard)
  render(
    <div>
      <AlertsWrapper initMessages={dashboard.common.flash_messages} />
      <Header dashboard={dashboard} />
    </div>,
    document.getElementById('dashboard-header'),
  );
  // eslint-disable-next-line no-param-reassign
  dashboard.reactGridLayout = render(
    <GridLayout dashboard={dashboard} />,
    document.getElementById('grid-container'),
  );

  // Displaying widget controls on hover
  $('.react-grid-item').hover(
    function () {
      $(this).find('.chart-controls').fadeIn(300);
    },
    function () {
      $(this).find('.chart-controls').fadeOut(300);
    },
  );
  $('div.grid-container').css('visibility', 'visible');

  $('div.widget').click(function (e) {
    const $this = $(this);
    const $target = $(e.target);

    if ($target.hasClass('slice_info')) {
      $this.find('.slice_description').slideToggle(0, function () {
        $this.find('.refresh').click();
      });
    } else if ($target.hasClass('controls-toggle')) {
      $this.find('.chart-controls').toggle();
    }
  });
  px.initFavStars();
  // $('[data-toggle="tooltip"]').tooltip({ container: 'body' });
}

export function dashboardContainer(dashboard, datasources, userid) {
  return Object.assign({}, dashboard, {
    type: 'dashboard',
    filters: {},
    curUserId: userid,
    init() {
      this.sliceObjects = [];
      this.filterBoxData = [];
      dashboard.slices.forEach((data) => {
        if (data.error) {
          const html = `<div class="alert alert-danger">${data.error}</div>`;
          $(`#slice_${data.slice_id}`).find('.token').html(html);
        } else {
          const slice = px.Slice(data, datasources[data.form_data.datasource], this, dashboard.theme);
          $(`#slice_${data.slice_id}`).find('a.refresh').click(() => {
            if (data.slice_id === filter_combination_id) {
              slice.render(true, dashboard.theme);
              this.sliceObjects.forEach((s) => {
                if ($.inArray(s.formData.slice_id, filter_box_ids) !== -1) {
                  setTimeout(() => { s.render(true); }, 500);
                }
              });
            } else {
              slice.render(true);
            }
          });
          this.sliceObjects.push(slice);
        }
        // get prompt default value
        if (data.form_data.viz_type === 'filter_box' || data.form_data.viz_type === 'filter_box_tree'
           || data.form_data.viz_type === 'filter_box_cascade') {
          this.filterBoxData.push({
            sliceId: data.slice_id,
            formData: data.form_data,
          });
        }
      });
      this.loadPreSelectFilters();
      this.startPeriodicRender(0);
      this.bindResizeToWindowResize();
    },
    onChange() {
      onBeforeUnload(true);
      renderAlert();
    },
    onSave() {
      onBeforeUnload(false);
      $('#alert-container').html('');
    },
    loadPreSelectFilters() {
      // set prompt default value
      if (px.getParam('preselect_filters') === '' && this.filterBoxData.length > 0) {
        const thisObj = this;
        this.filterBoxData.forEach(f => {
          const fd = f.formData;
          const d = {};
          if (fd.defaultValueSetting !== undefined) {
            fd.defaultValueSetting.forEach(m => {
              // get default value from sets
              if (m.type === 'sets') {
                d[m.field] = m.value.split(',');
                this.setDefaultValue(d, f.sliceId);
              } else if (m.type === 'sql') {
                // get default value from sql query
                let value = '';
                $.ajax({
                  async: false,
                  url: '/hand/prompt/query',
                  type: 'POST',
                  data: { sql: m.sql },
                  dataType: 'json',
                  success: function (data) {
                    if (data.length > 0) {
                      for (let i = 0; i < data.length; i++) {
                        for (const k in data[i]) {
                          value += data[i][k] + ',';
                        }
                      }
                      value = value.substr(0, value.length - 1);
                      d[m.field] = value.split(',');
                      thisObj.setDefaultValue(d, f.sliceId);
                    }
                  },
                  error: function (xhr, error) {
                    alert(xhr.responseText);
                  },
                });
              }
            });
          }
          if (fd.defaultValueFilterTreeSetting !== undefined && fd.filter_name !== undefined && fd.filter_name !== '') {
            const field = fd.filter_name.split('-')[1];
            fd.defaultValueFilterTreeSetting.forEach(m => {
              // get default value from sets
              if (m.type === 'sets') {
                d[field] = m.value.split(',');
                this.setDefaultValue(d, f.sliceId);
              } else if (m.type === 'sql') {
                // get default value from sql query
                let value = '';
                $.ajax({
                  async: false,
                  url: '/hand/prompt/query',
                  type: 'POST',
                  data: { sql: m.sql },
                  dataType: 'json',
                  success: function (data) {
                    if (data.length > 0) {
                      for (let i = 0; i < data.length; i++) {
                        for (const k in data[i]) {
                          value += data[i][k] + ',';
                        }
                      }
                      value = value.substr(0, value.length - 1);
                      d[field] = value.split(',');
                      thisObj.setDefaultValue(d, f.sliceId);
                    }
                  },
                  error: function (xhr, error) {
                    alert(xhr.responseText);
                  },
                });
              }
            });
          }
          if (fd.date_filter) {
            // date filter
            d['__from'] = fd.dateValueSetting[0];
            d['__to'] = fd.dateValueSetting[1];
            thisObj.setDefaultValue(d, f.sliceId);
          }
        });
      } else {
        try {
          const filters = JSON.parse(px.getParam('preselect_filters') || '{}');
          for (const sliceId in filters) {
            for (const col in filters[sliceId]) {
              this.setFilter(sliceId, col, filters[sliceId][col], false, false);
            }
          }
        } catch (e) {
          // console.error(e);
        }
      }
    },
    setDefaultValue(d, sliceId) {
      // console.info(d);
      if (d !== undefined && d !== '') {
        for (const col in d) {
          this.setFilter(sliceId, col, d[col], false);
        }
      }
    },
    setFilter(sliceId, col, vals, refresh) {
      this.addFilter(sliceId, col, vals, false, refresh);
    },
    done(slice) {
      const refresh = slice.getWidgetHeader().find('.refresh');
      const data = slice.data;
      const cachedWhen = moment.utc(data.cached_dttm).fromNow();
      if (data !== undefined && data.is_cached) {
        refresh
          .addClass('danger')
          .attr(
          'title',
          t('Served from data cached %s . Click to force refresh.', cachedWhen))
        // .tooltip('fixTitle');
      } else {
        refresh
        .removeClass('danger')
        .attr('title', t('Click to force refresh'))
        // .tooltip('fixTitle');
      }
    },
    effectiveExtraFilters(sliceId) {
      const f = [];
      const immuneSlices = this.metadata.filter_immune_slices || [];
      if (sliceId && immuneSlices.includes(sliceId)) {
        // The slice is immune to dashboard fiterls
        return f;
      }

      // Building a list of fields the slice is immune to filters on
      let immuneToFields = [];
      if (
        sliceId &&
        this.metadata.filter_immune_slice_fields &&
        this.metadata.filter_immune_slice_fields[sliceId]) {
        immuneToFields = this.metadata.filter_immune_slice_fields[sliceId];
      }
      for (const filteringSliceId in this.filters) {
        if (filteringSliceId === sliceId.toString()) {
          // Filters applied by the slice don't apply to itself
          continue;
        }
        for (const field in this.filters[filteringSliceId]) {
          if (!immuneToFields.includes(field)) {
            f.push({
              col: field,
              op: 'in',
              val: this.filters[filteringSliceId][field],
              filteringSliceId: filteringSliceId,
            });
          }
        }
      }
      return f;
    },
    addFilter(sliceId, col, vals, merge = true, refresh = true) {
      if (this.getSlice(sliceId).formData.viz_type === 'filter_box_combination') {
        if (refresh) {
          this.refreshExcept(sliceId);
        }
      } else {
        const slice = this.getSlice(sliceId);
        if (slice && 
            (col === '__from' || col === '__to' ||
              slice.formData.groupby.indexOf(col) !== -1 ||
              slice.formData.viz_type === 'filter_box_cascade' ||
              (slice.formData.viz_type === 'filter_box_tree' && slice.formData.filter_name.split('-')[1] === col)
            )
          ) {
          if (!(sliceId in this.filters)) {
            this.filters[sliceId] = {};
          }
          if (!(col in this.filters[sliceId]) || !merge) {
            this.filters[sliceId][col] = vals;

            // d3.merge pass in array of arrays while some value form filter components
            // from and to filter box require string to be process and return
          } else if (this.filters[sliceId][col] instanceof Array) {
            this.filters[sliceId][col] = d3.merge([this.filters[sliceId][col], vals]);
          } else {
            this.filters[sliceId][col] = d3.merge([[this.filters[sliceId][col]], vals])[0] || '';
          }
          if (refresh) {
            this.refreshExcept(sliceId);
          }
        }
      }
      this.updateFilterParamsInUrl();
    },
    readFilters() {
      // Returns a list of human readable active filters
      return JSON.stringify(this.filters, null, '  ');
    },
    updateFilterParamsInUrl() {
      const urlObj = urlLib.parse(location.href, true);
      urlObj.query = urlObj.query || {};
      urlObj.query.preselect_filters = this.readFilters();
      urlObj.search = null;
      history.pushState(urlObj.query, window.title, urlLib.format(urlObj));
    },
    bindResizeToWindowResize() {
      let resizeTimer;
      const dash = this;
      $(window).on('resize', () => {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => {
          dash.sliceObjects.forEach((slice) => {
            if (dash.refreshAble === 'true') {
              slice.resize();
            }
            // slice.resize();
          });
        }, 500);
      });
    },
    stopPeriodicRender() {
      if (this.refreshTimer) {
        clearTimeout(this.refreshTimer);
        this.refreshTimer = null;
      }
    },
    startPeriodicRender(interval) {
      this.stopPeriodicRender();
      const dash = this;
      const immune = this.metadata.timed_refresh_immune_slices || [];
      const maxRandomDelay = Math.max(interval * 0.2, 5000);
      const refreshAll = () => {
        dash.sliceObjects.forEach((slice) => {
          const force = !dash.firstLoad;
          // slice.render(force);
          if ($.inArray(slice.formData.slice_id, filter_box_ids) !== -1) {
            setTimeout(() => { slice.render(force); }, 500);
          } else {
            slice.render(force);
          }
          // setTimeout(() => {
          //   slice.render(force);
          // },
          // // Randomize to prevent all widgets refreshing at the same time
          // maxRandomDelay * Math.random());
        });
        dash.firstLoad = false;
      };

      const fetchAndRender = function () {
        refreshAll();
        if (interval > 0) {
          dash.refreshTimer = setTimeout(function () {
            fetchAndRender();
          }, interval);
        }
      };
      fetchAndRender();
    },
    refreshExcept(sliceId) {
      const immune = this.metadata.filter_immune_slices || [];
      this.sliceObjects.forEach((slice) => {
        if (slice.data.slice_id !== sliceId && immune.indexOf(slice.data.slice_id) === -1
          && slice.formData.viz_type !== 'filter_box' && slice.formData.viz_type !== 'filter_box_tree'
          && slice.formData.viz_type !== 'filter_box_cascade'
          && slice.formData.viz_type !== 'filter_box_combination') {
          // if(slice.data.slice_id !== filter_combination_id) {
          slice.render();
          const sliceSeletor = $(`#${slice.data.slice_id}-cell`);
          sliceSeletor.addClass('slice-cell-highlight');
          setTimeout(function () {
            sliceSeletor.removeClass('slice-cell-highlight');
          }, 1200);
        }
      });
    },
    clearFilters(sliceId) {
      delete this.filters[sliceId];
      this.refreshExcept(sliceId);
      this.updateFilterParamsInUrl();
    },
    removeFilter(sliceId, col, vals) {
      if (sliceId in this.filters) {
        if (col in this.filters[sliceId]) {
          const a = [];
          this.filters[sliceId][col].forEach(function (v) {
            if (vals.indexOf(v) < 0) {
              a.push(v);
            }
          });
          this.filters[sliceId][col] = a;
        }
      }
      this.refreshExcept(sliceId);
      this.updateFilterParamsInUrl();
    },
    getSlice(sliceId) {
      const id = parseInt(sliceId, 10);
      let i = 0;
      let slice = null;
      while (i < this.sliceObjects.length) {
        // when the slice is found, assign to slice and break;
        if (this.sliceObjects[i].data.slice_id === id) {
          slice = this.sliceObjects[i];
          break;
        }
        i++;
      }
      return slice;
    },
    getAjaxErrorMsg(error) {
      const respJSON = error.responseJSON;
      console.log(respJSON)
      return (respJSON && respJSON.message) ? respJSON.message :
        error.responseText;
    },
    addSlicesToDashboard(sliceIds) {
      const getAjaxErrorMsg = this.getAjaxErrorMsg;
      $.ajax({
        type: 'POST',
        url: `/superset/add_slices/${dashboard.id}/`,
        data: {
          data: JSON.stringify({ slice_ids: sliceIds }),
        },
        success() {
          // Refresh page to allow for slices to re-render
          window.location.reload();
        },
        error(error) {
          const errorMsg = getAjaxErrorMsg(error);
          utils.showModal({
            title: t('Error'),
            body: t('Sorry, there was an error adding slices to this dashboard: %s', errorMsg),
          });
        },
      });
    },
    updateDashboardTitle(title) {
      this.dashboard_title = title;
      this.onChange();
    },
  });
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

$(document).ready(() => {
  // Getting bootstrapped data from the DOM
  utils.initJQueryAjax();
  const dashboardData = $('.dashboard').data('bootstrap');
  const state = getInitialState(dashboardData);
  px = superset(state);

  // get filter_combination_id
  state.dashboard.slices.forEach(s => {
    if (s.form_data.viz_type === 'filter_box_combination') {
      filter_combination_id = s.slice_id;
      filter_box_ids = s.form_data.filter_combination;
    }
  });

  if (filter_combination_id !== null && filter_box_ids.length !== 0) {
    $.ajax({
      url: '/hand/getSliceData?sliceIds=' + filter_box_ids.join(','),
      async: false,
      success: function (data) {
        const slices = JSON.parse(data);
        const state2 = getInitialState(slices);
        let mergeState = state;
        mergeState.dashboard.slices = state.dashboard.slices.concat(state2.dashboard.slices);
        mergeState.datasources = $.extend(state.datasources, state2.datasources);
        // console.info(mergeState)
        const sliceCombination = dashboardContainer(mergeState.dashboard, mergeState.datasources, state.user_id);
        // console.info(sliceCombination)
        initDashboardView(sliceCombination, state.themes, state.sliceResizeAble);
        // console.info(sliceCombination)
        sliceCombination.init();
        hideTitle();
      }
    });
  } else {
    const dashboard = dashboardContainer(state.dashboard, state.datasources, state.user_id);
    initDashboardView(dashboard, state.themes, state.sliceResizeAble);
    dashboard.init();
    hideTitle();
  }

});
