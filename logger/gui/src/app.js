import React, { Component } from 'react'

import Moment from 'react-moment'

import {
  ActionBar,
  ActionBarRow,
  Hits,
  HitsStats,
  InitialLoader,
  NoHits,
  PageSizeSelector,
  Pagination,
  RefinementListFilter,
  ResetFilters,
  SearchBox,
  SearchkitManager,
  SearchkitProvider,
  Select,
  SelectedFilters,
  SortingSelector
} from "searchkit"

import { ThemeChooser } from './components/utils'


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
      {props.hits.map((hit, i) => (
        <tr className={ hit._source.appname } key={ i }>
          <td>{ hit._source.appname }</td>
          <td>{ hit._source.severity }</td>
          <td><Moment date={ hit._source.timestamp } /></td>
          <td>{ hit._source.msg }</td>
        </tr>
      ))}
    </tbody>
  </table>
)

class App extends Component {
  constructor(props, context) {
    super(props, context)
    this.searchkit = new SearchkitManager('/api/')
    this.searchkit.addDefaultQuery(query => query)
    this.refreshInterval = null

    this.searchkit.translateFunction = key => {
      return {
        "pagination.next": "Next Page",
        "pagination.previous": "Previous Page"
      }[key]
    }

    this.themeOptionStyles = {
      position: 'fixed',
      bottom: '5px',
      right: '5px'
    }
  }

  componentDidMount() {
    this.refreshInterval = setInterval(this.refresh.bind(this), 5000)
  }

  componentWillUnmount() {
    clearInterval(this.refreshInterval);
  }

  refresh() {
    try {
      this.searchkit.performSearch()
    } catch (err) {
      print('Cannot connect to log data store')
    }
  }

  render() {
    return (
      <SearchkitProvider searchkit={ this.searchkit } >
        <div id="contents">
          <nav className="navbar navbar-expand-sm fixed-top navbar-dark bg-dark">
            <div className="container-fluid">
              <a className="navbar-brand" href="/">Logger</a>
              <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#searchNav" aria-controls="searchNav" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
              </button>

              <div className="collapse navbar-collapse" id="searchNav">
                <SearchBox
                  translations={ {"searchbox.placeholder": "search logs"} }
                  queryOptions={ {"minimum_should_match":"50%"} }
                  searchOnChange={ true }
                  queryFields={ ["appname^1", "severity^2", "msg^3"] }
                />
              </div>
            </div>
          </nav>

          <div className="container-fluid" style={{ marginTop: 120+'px'}}>
            <div className="row mx-auto">
              <div className="col-md-2 col-12">
                <RefinementListFilter
                  id="appnames"
                  title="App"
                  field="appname.keyword"
                  operator="OR"
                  size={ 10 }
                />
                <hr />
                <RefinementListFilter
                  id="severity"
                  title="Severity"
                  field="severity.keyword"
                  operator="OR"
                  size={ 10 }
                />
                <hr />
                <RefinementListFilter
                  id="log_source"
                  title="Source"
                  field="hostname.keyword"
                  operator="OR"
                  size={ 10 }
                />
              </div>

              <div className="col-12 m-2 d-md-none"></div>

              <div className="col-md-10 col-12">
                <ActionBar mod="row mx-auto">
                  <ActionBarRow>
                    <HitsStats translations={ {"hitstats.results_found": "{hitCount} results found"} } />
                    <PageSizeSelector
                      showNumbers={ true }
                      options={ [10,20,30,40,50] }
                      listComponent={ Select }
                    />
                    <SortingSelector
                      options={[
                        {label: "Most Recent", field: "timestamp", order: "desc", defaultOption: true},
                        {label: "App", field: "appname.keyword", order: "asc"},
                        {label: "Severity", field: "severity.keyword", order: "asc"}
                      ]}
                    />
                  </ActionBarRow>

                  <ActionBarRow>
                    <SelectedFilters/>
                    <ResetFilters/>
                  </ActionBarRow>
                </ActionBar>

                <Hits hitsPerPage={ 10 } sourceFilter={ ["appname", "severity", "timestamp", "msg"] } listComponent={ LogItem } />

                <NoHits
                  translations={{
                    "NoHits.NoResultsFound": "No logs found were found for {query}",
                    "NoHits.DidYouMean": "Search for {suggestion}",
                    "NoHits.SearchWithoutFilters": "Search for {query} without filters"
                  }}
                  suggestionsField={ "appname" }
                />

                <InitialLoader />

                <Pagination showNumbers={ true } />
              </div>
            </div>
          </div>

          <div style={ this.themeOptionStyles }>
            <ThemeChooser size='sm' />
          </div>
        </div>
      </SearchkitProvider>
    );
  }
}

export default App;
