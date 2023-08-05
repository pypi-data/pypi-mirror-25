import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';

import { t } from '../../locales';
import TableLoader from './TableLoader';

const propTypes = {
  user: PropTypes.object.isRequired,
};

class CreatedContent extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      dashboardsLoading: true,
      slicesLoading: true,
      dashboards: [],
      slices: [],
    };
  }
  renderSliceTable() {
    const mutator = data => data.map(slice => {
      const data = {};
      data[t('slice')] = <a href={slice.url}>{slice.title}</a>;
      data[t('favorited')] = moment.utc(slice.dttm).fromNow();
      data[t('_favorited')] = slice.dttm;
      return data;
    });
    return (
      <TableLoader
        dataEndpoint={`/superset/created_slices/${this.props.user.userId}/`}
        className="table table-condensed"
        columns={[t('slice'), t('favorited')]}
        mutator={mutator}
        noDataText={t('No slices')}
        sortable
      />
    );
  }
  renderDashboardTable() {
    const mutator = data => data.map(dash => {
      const data = {};
      data[t('dashboard')] = <a href={dash.url}>{dash.title}</a>;
      data[t('favorited')] = moment.utc(dash.dttm).fromNow();
      data[t('_favorited')] = dash.dttm;
      return data;
    });
    return (
      <TableLoader
        className="table table-condensed"
        mutator={mutator}
        dataEndpoint={`/superset/created_dashboards/${this.props.user.userId}/`}
        noDataText={t('No dashboards')}
        columns={[t('dashboard'), t('favorited')]}
        sortable
      />
    );
  }
  render() {
    return (
      <div>
        <h3>{t('Dashboards')}</h3>
        {this.renderDashboardTable()}
        <hr />
        <h3>{t('Slices')}</h3>
        {this.renderSliceTable()}
      </div>
    );
  }
}
CreatedContent.propTypes = propTypes;

export default CreatedContent;
