import React from 'react';
import PropTypes from 'prop-types';
import { Alert } from 'react-bootstrap';

import QueryTable from './QueryTable';
import { t } from '../../locales';

const propTypes = {
  queries: PropTypes.array.isRequired,
  actions: PropTypes.object.isRequired,
};

const QueryHistory = (props) => {
  if (props.queries.length > 0) {
    return (
      <QueryTable
        columns={[
          t('state'), t('started'), t('duration'), t('progress'),
          t('rows'), t('sql'), t('output'), t('actions'),
        ]}
        queries={props.queries}
        actions={props.actions}
      />
    );
  }
  return (
    <Alert bsStyle="info">
      {t('No query history yet...')}
    </Alert>
  );
};
QueryHistory.propTypes = propTypes;

export default QueryHistory;
