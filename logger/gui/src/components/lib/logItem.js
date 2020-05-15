import React from 'react';
import PropTypes from 'prop-types';
import Moment from 'react-moment';

const LogItem = props => (
  <table className="table table-striped">
    <thead>
      <tr>
        <th scope="col">App</th>
        <th scope="col">Level</th>
        <th scope="col">Timestamp</th>
        <th scope="col">Message</th>
      </tr>
    </thead>
    <tbody>
      {props.hits.map(hit => (
        <tr className={ hit._source.appname } key={ hit._id }>
          <td>{ hit._source.appname }</td>
          <td>{ hit._source.severity }</td>
          <td><Moment date={ hit._source.timestamp } /></td>
          <td>{ hit._source.msg }</td>
        </tr>
      ))}
    </tbody>
  </table>
);

LogItem.propTypes = {
  hits: PropTypes.arrayOf(PropTypes.shape({
    _index: PropTypes.string,
    _type: PropTypes.string,
    _id: PropTypes.string,
    _score: PropTypes.number,
    _source: PropTypes.shape({
      severity: PropTypes.string,
      msg: PropTypes.string,
      appname: PropTypes.string,
      timestamp: PropTypes.string
    }),
    sort: PropTypes.arrayOf(PropTypes.number)
  })).isRequired
};

export default LogItem;