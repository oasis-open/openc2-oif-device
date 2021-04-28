import React, { Component } from 'react';
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
} from 'searchkit';

import { LogItem } from './components/lib';
import { ThemeChooser } from './components/utils';

class App extends Component {
  constructor(props, context) {
    super(props, context);

    this.searchkit = new SearchkitManager('/api/');
    this.searchkit.addDefaultQuery(query => query);
    this.refreshInterval = null;

    this.searchkit.translateFunction = key => {
      return {
        'pagination.next': 'Next Page',
        'pagination.previous': 'Previous Page'
      }[key];
    };

    this.themeOptionStyles = {
      position: 'fixed',
      bottom: '5px',
      right: '5px'
    };
  }

  componentDidMount() {
    this.refreshInterval = setInterval(this.refresh.bind(this), 5000);
  }

  componentWillUnmount() {
    clearInterval(this.refreshInterval);
  }

  refresh() {
    try {
      this.searchkit.performSearch();
    } catch (err) {
      console.error('Cannot connect to log data store');
    }
  }

  render() {
    return (
      <SearchkitProvider id="contents" searchkit={ this.searchkit }>
        <nav className="navbar navbar-expand-sm fixed-top navbar-dark bg-dark">
          <div className="container-fluid">
            <a className="navbar-brand" href="/">Logger</a>
            <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#searchNav" aria-controls="searchNav" aria-expanded="false" aria-label="Toggle navigation">
              <span className="navbar-toggler-icon" />
            </button>

            <div className="collapse navbar-collapse" id="searchNav">
              <SearchBox
                translations={{'searchbox.placeholder': 'search logs'}}
                queryOptions={{'minimum_should_match': '50%'}}
                searchOnChange
                queryFields={['appname^1', 'severity^2', 'msg^3']}
              />
            </div>
          </div>
        </nav>

        <div className="container-fluid" style={{ marginTop: '100px'}}>
          <div className="row mx-auto">
            <div className="col-md-2 col-12">
              <div className="pb-3 mb-3 border-bottom">
                <h5>App</h5>
                <RefinementListFilter
                  id="appnames"
                  field="appname.keyword"
                  operator="OR"
                  size={ 10 }
                />
              </div>
              <div className="pb-3 mb-3 border-bottom">
                <h5>Severity</h5>
                <RefinementListFilter
                  id="severity"
                  field="severity.keyword"
                  operator="OR"
                  size={ 10 }
                />
              </div>
              <div className="pb-3 mb-3 border-bottom">
                <h5>Source</h5>
                <RefinementListFilter
                  id="log_source"
                  field="hostname.keyword"
                  operator="OR"
                  size={ 10 }
                />
              </div>
            </div>

            <div className="col-12 m-2 d-md-none" />

            <div className="col-md-10 col-12">
              <ActionBar mod="row mx-auto">
                <ActionBarRow>
                  <SelectedFilters />
                  <ResetFilters />
                </ActionBarRow>

                <ActionBarRow>
                  <HitsStats translations={{'hitstats.results_found': '{hitCount} results found'}} />
                  <PageSizeSelector
                    showNumbers
                    options={[10, 20, 30, 40, 50]}
                  />
                  <SortingSelector
                    options={[
                      {label: 'Most Recent', field: 'timestamp', order: 'desc', defaultOption: true},
                      {label: 'App', field: 'appname.keyword', order: 'asc'},
                      {label: 'Severity', field: 'severity.keyword', order: 'asc'}
                    ]}
                  />
                </ActionBarRow>
              </ActionBar>

              <Hits hitsPerPage={ 10 } sourceFilter={ ['appname', 'severity', 'timestamp', 'msg'] } listComponent={ LogItem } />

              <NoHits
                translations={{
                  'NoHits.NoResultsFound': 'No logs found were found for {query}',
                  'NoHits.DidYouMean': 'Search for {suggestion}',
                  'NoHits.SearchWithoutFilters': 'Search for {query} without filters'
                }}
                suggestionsField='appname'
              />

              <InitialLoader />

              <Pagination showNumbers={ true } />
            </div>
          </div>
        </div>

        <div style={ this.themeOptionStyles }>
          <ThemeChooser size='sm' />
        </div>
      </SearchkitProvider>
    );
  }
}

export default App;
