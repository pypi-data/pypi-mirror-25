import React from 'react';
import PropTypes from 'prop-types';
import cx from 'classnames';

import URLShortLinkButton from './URLShortLinkButton';
import EmbedCodeButton from './EmbedCodeButton';
import DisplayQueryButton from './DisplayQueryButton';
import { t } from '../../locales';

const propTypes = {
  canDownload: PropTypes.oneOfType([PropTypes.string, PropTypes.bool]).isRequired,
  slice: PropTypes.object,
  queryEndpoint: PropTypes.string.isRequired,
  queryResponse: PropTypes.object,
  chartStatus: PropTypes.string,
};

export default function ExploreActionButtons({
    chartStatus, canDownload, slice, queryResponse, queryEndpoint, isImportExcel }) {
  const exportToExcelClasses = cx('btn btn-default btn-sm', {
    'disabled disabledButton': !canDownload,
  });
  if (slice) {
    return (
      <div className="btn-group results" role="group">
        <URLShortLinkButton slice={slice} />

        <EmbedCodeButton slice={slice} />

        <a
          href={slice.data.json_endpoint}
          className="btn btn-default btn-sm"
          title={t('Export to .json')}
          target="_blank"
          rel="noopener noreferrer"
        >
          <i className="fa fa-file-code-o" /> {t('.json')}
        </a>
        {isImportExcel &&
          <a
            href={slice.data.excel_endpoint}
            className={exportToExcelClasses}
            title={t('Export to .excel format')}
            target="_blank"
            rel="noopener noreferrer"
          >
            <i className="fa fa-file-text-o" /> {t('.excel')}
        </a>
        }

        <DisplayQueryButton
          queryResponse={queryResponse}
          queryEndpoint={queryEndpoint}
          chartStatus={chartStatus}
        />
      </div>
    );
  }
  return (
    <DisplayQueryButton queryEndpoint={queryEndpoint} />
  );
}

ExploreActionButtons.propTypes = propTypes;
