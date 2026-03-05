// @specre 01KJXW7T67VPX2HZKKWN70MM4E
import PropTypes from 'prop-types';
import { h } from 'preact';

import { DateTime } from '../../../shared/components/dateTime';

export const ListingDate = ({ bumpedAt, updatedAt }) => {
  return (
    <DateTime
      className="dashboard-listing-date"
      dateTime={bumpedAt ? bumpedAt.toString() : updatedAt.toString()}
    />
  );
};

ListingDate.propTypes = {
  bumpedAt: PropTypes.instanceOf(Date).isRequired,
  updatedAt: PropTypes.instanceOf(Date).isRequired,
};
