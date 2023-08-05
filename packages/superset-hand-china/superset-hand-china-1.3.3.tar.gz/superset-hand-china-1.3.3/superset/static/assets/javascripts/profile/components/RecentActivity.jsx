import React from 'react';
import PropTypes from 'prop-types';
import moment from 'moment';

import { t } from '../../locales';
import TableLoader from './TableLoader';

const propTypes = {
  user: PropTypes.object,
};

export default class RecentActivity extends React.PureComponent {
  render() {
    const mutator = function (data) {
      return data.map(row => {
        const data = {};
        data[t('action')] = row.action;
        data[t('item')] = <a href={row.item_url}>{row.item_title}</a>;
        data[t('time')] = moment.utc(row.time).fromNow();
        data[t('_time')] = row.time;
        return data;
      });
    };
    return (
      <div>
        <TableLoader
          className="table table-condensed"
          mutator={mutator}
          sortable
          dataEndpoint={`/superset/recent_activity/${this.props.user.userId}/`}
        />
      </div>
    );
  }
}
RecentActivity.propTypes = propTypes;
