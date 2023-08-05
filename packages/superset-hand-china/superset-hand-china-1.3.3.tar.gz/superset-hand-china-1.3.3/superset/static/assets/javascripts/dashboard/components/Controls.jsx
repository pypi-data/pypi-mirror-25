import React from 'react';
import PropTypes from 'prop-types';
import { ButtonGroup } from 'react-bootstrap';

import { t } from '../../locales';
import Button from '../../components/Button';
import CssEditor from './CssEditor';
import RefreshIntervalModal from './RefreshIntervalModal';
import SaveModal from './SaveModal';
import CodeModal from './CodeModal';
import SliceAdder from './SliceAdder';

const $ = window.$ = require('jquery');

const propTypes = {
  dashboard: PropTypes.object.isRequired,
};

class Controls extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      css: props.dashboard.css || '',
      theme: props.dashboard.theme,
      refreshAble: props.dashboard.refreshAble,
      cssTemplates: [],
    };
  }
  componentWillMount() {
    $.get('/csstemplateasyncmodelview/api/read', (data) => {
      const cssTemplates = data.result.map(row => ({
        value: row.template_name,
        css: row.css,
        label: row.template_name,
      }));
      this.setState({ cssTemplates });
    });
  }
  refresh() {
    this.props.dashboard.sliceObjects.forEach((slice) => {
      slice.render(true);
    });
  }
  changeCss(css) {
    this.setState({ css });
    this.props.dashboard.onChange();
  }
  changeTheme(theme) {
    this.setState({ theme });
    this.props.dashboard.onChange();
  }
  changeRefresh(refreshAble) {
    this.setState({ refreshAble });
    this.props.dashboard.onChange();
  }
  change(opt, type) {
    if (type === 'css') {
      this.changeCss(opt);
    } else if (type === 'theme') {
      this.changeTheme(opt);
    } else if (type === 'refresh') {
      this.changeRefresh(opt);
    }
  }
  render() {
    const dashboard = this.props.dashboard;
    const emailBody = t('Checkout this dashboard: %s', window.location.href);
    const emailLink = 'mailto:?Subject=Superset%20Dashboard%20'
      + `${dashboard.dashboard_title}&Body=${emailBody}`;
    return (
      <ButtonGroup>
        <Button
          tooltip={t('Force refresh the whole dashboard')}
          onClick={this.refresh.bind(this)}
          >
          <i className="fa fa-refresh" />
        </Button>
        <SliceAdder
          dashboard={dashboard}
          triggerNode={
            <i className="fa fa-plus" />
          }
          />
        <RefreshIntervalModal
          onChange={refreshInterval => dashboard.startPeriodicRender(refreshInterval * 1000)}
          triggerNode={
            <i className="fa fa-clock-o" />
          }
          />
        <CodeModal
          codeCallback={dashboard.readFilters.bind(dashboard)}
          triggerNode={<i className="fa fa-filter" />}
          />
        <CssEditor
          dashboard={dashboard}
          triggerNode={
            <i className="fa fa-css3" />
          }
          initialCss={dashboard.css}
          templates={this.state.cssTemplates}
          onChange={this.change.bind(this)}
          theme={dashboard.theme}
          themes={dashboard.themes}
          sliceResizeAble={dashboard.sliceResizeAble}
          refreshAble={dashboard.refreshAble}
          />
        <Button
          onClick={() => { window.location = emailLink; } }
          >
          <i className="fa fa-envelope" />
        </Button>
        <Button
          disabled={!dashboard.dash_edit_perm}
          onClick={() => {
            window.location = `/dashboardmodelview/edit/${dashboard.id}`;
          } }
          tooltip={t('Edit this dashboard\'s properties')}
          >
          <i className="fa fa-edit" />
        </Button>
        <SaveModal
          dashboard={dashboard}
          css={this.state.css}
          theme={this.state.theme}
          refreshAble={this.state.refreshAble}
          triggerNode={
            <Button disabled={!dashboard.dash_save_perm}>
              <i className="fa fa-save" />
            </Button>
          }
          />
      </ButtonGroup>
    );
  }
}
Controls.propTypes = propTypes;

export default Controls;
