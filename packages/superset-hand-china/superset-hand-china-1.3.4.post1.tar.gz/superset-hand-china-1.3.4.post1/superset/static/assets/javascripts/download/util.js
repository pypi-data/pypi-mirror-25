const urlLib = require('url');
const utils = require('../modules/utils');
import moment from 'moment';

export function getInitialState(boostrapData) {
  const dashboard = Object.assign({}, utils.controllerInterface, boostrapData.dashboard_data);
  dashboard.firstLoad = true;

  dashboard.posDict = {};
  if (dashboard.position_json) {
    dashboard.position_json.forEach((position) => {
      dashboard.posDict[position.slice_id] = position;
    });
  }
  dashboard.refreshTimer = null;
  const state = Object.assign({}, boostrapData, { dashboard });
  return state;
}

export function dashboardContainer(dashboard, datasources, userid, px) {
  return Object.assign({}, dashboard, {
    type: 'dashboard',
    filters: {},
    curUserId: userid,
    init() {
      this.sliceObjects = [];
      dashboard.slices.forEach((data) => {
        if (data.error) {
          const html = `<div class="alert alert-danger">${data.error}</div>`;
          $(`#slice_${data.slice_id}`).find('.token').html(html);
        } else {
          const slice = px.Slice(data, datasources[data.form_data.datasource], this, dashboard.theme);
          $(`#slice_${data.slice_id}`).find('a.refresh').click(() => {
            slice.render(true);
          });
          this.sliceObjects.push(slice);
        }
      });
      this.loadPreSelectFilters();
      this.startPeriodicRender(0);
    },
    loadPreSelectFilters() {
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
    },
    setFilter(sliceId, col, vals, refresh) {
      this.addFilter(sliceId, col, vals, false, refresh);
    },
    effectiveExtraFilters(sliceId) {
      const f = [];
      const immuneSlices = [];
      if (sliceId && immuneSlices.includes(sliceId)) {
        return f;
      }
      let immuneToFields = [];
      for (const filteringSliceId in this.filters) {
        for (const field in this.filters[filteringSliceId]) {
          if (!immuneToFields.includes(field)) {
            f.push({
              col: field,
              op: 'in',
              val: this.filters[filteringSliceId][field],
            });
          }
        }
      }
      return f;
    },
    addFilter(sliceId, col, vals, merge = true, refresh = true) {
      if (!(sliceId in this.filters)) {
        this.filters[sliceId] = {};
      }
      if (!(col in this.filters[sliceId]) || !merge) {
        this.filters[sliceId][col] = vals;
      } else if (this.filters[sliceId][col] instanceof Array) {
        this.filters[sliceId][col] = d3.merge([this.filters[sliceId][col], vals]);
      } else {
        this.filters[sliceId][col] = d3.merge([[this.filters[sliceId][col]], vals])[0] || '';
      }
      if (refresh) {
        this.refreshExcept(sliceId);
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
    startPeriodicRender(interval) {
      const dash = this;
      const maxRandomDelay = Math.max(interval * 0.2, 5000);
      dash.sliceObjects.forEach((slice) => {
        if (slice.formData.viz_type === 'filter_box' || slice.formData.viz_type === 'filter_box_tree') {
          slice.render(true);
        }
      });
    },
    refreshExcept(sliceId) {
    //   const immune = this.metadata.filter_immune_slices || [];
      const immune = [];
      // console.info(this.sliceObjects);
    },
    getSliceObjects() {
      return this.sliceObjects;
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
  });
}