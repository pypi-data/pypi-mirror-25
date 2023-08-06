// const px = require('../../javascripts/modules/superset');
const urlLib = require('url');
const utils = require('../../javascripts/modules/utils');
import moment from 'moment';
import { t } from '../../javascripts/locales';

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
          const slice = px.Slice(data, datasources[data.form_data.datasource], this);
          $(`#slice_${data.slice_id}`).find('a.refresh').click(() => {
            slice.render(true);
          });
          this.sliceObjects.push(slice);
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
    done(slice) {
      const refresh = slice.getWidgetHeader().find('.refresh');
      const data = slice.data;
      const cachedWhen = moment.utc(data.cached_dttm).fromNow();
      if (data !== undefined && data.is_cached) {
        refresh
        .addClass('danger')
        .attr(
          'title',
          t('Served from data cached %s. Click to force refresh', cachedWhen))
        .tooltip('fixTitle');
      } else {
        refresh
        .removeClass('danger')
        .attr('title', t('Click to force refresh'))
        .tooltip('fixTitle');
      }
    },
    effectiveExtraFilters(sliceId) {
      const f = [];
    //   const immuneSlices = this.metadata.filter_immune_slices || [];
      const immuneSlices = [];
      if (sliceId && immuneSlices.includes(sliceId)) {
        // The slice is immune to dashboard fiterls
        return f;
      }

      // Building a list of fields the slice is immune to filters on
      let immuneToFields = [];
      // if (
      //       sliceId &&
      //       this.metadata.filter_immune_slice_fields &&
      //       this.metadata.filter_immune_slice_fields[sliceId]) {
      //   immuneToFields = this.metadata.filter_immune_slice_fields[sliceId];
      // }
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
            slice.resize();
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
      const maxRandomDelay = Math.max(interval * 0.2, 5000);
      const refreshAll = () => {
        dash.sliceObjects.forEach((slice) => {
          const force = !dash.firstLoad;
          setTimeout(() => {
            slice.render(force);
          },
          // Randomize to prevent all widgets refreshing at the same time
          maxRandomDelay * Math.random());
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
    //   const immune = this.metadata.filter_immune_slices || [];
      const immune = [];
      this.sliceObjects.forEach((slice) => {
        if (slice.data.slice_id !== sliceId && immune.indexOf(slice.data.slice_id) === -1) {
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
            body: t('Sorry, there was an error adding slices to this dashboard: %s ', errorMsg),
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