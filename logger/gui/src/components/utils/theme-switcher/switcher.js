import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet-async';
import validThemes from './themes';
import './assets/css/loader.css';

import * as themeActions from './theme-actions';

const setItem = (key, obj) => {
  if (!key) return null;
  try {
    localStorage.setItem(key, JSON.stringify(obj));
  } catch (err) {
    return null;
  }
};

const getItem = key => {
  if (!key) return null;
  try {
    const item = localStorage.getItem(key);
    return item ? JSON.parse(item) : null;
  } catch (err) {
    return null;
  }
};

//------------------------------------------------------------------------------
// Top level ThemeSwitcher Component
//------------------------------------------------------------------------------
class ThemeSwitcher extends Component {
  constructor(props, context) {
    super(props, context);
    this.load = this.load.bind(this);
    this.loadTheme = this.loadTheme.bind(this);

    const themeOptions = new Set(this.props.themeOptions.filter(t => validThemes.includes(t)));

    let defaultTheme = getItem(this.props.storeThemeKey);
    defaultTheme = defaultTheme || this.props.defaultTheme;
    themeOptions.add(defaultTheme);

    this.state = {
      currentTheme: defaultTheme,
      themes: this.props.themes || {},
      themeOptions
    };

    this.loadTheme(defaultTheme);
    setTimeout(() => {
      themeOptions.forEach(theme => this.loadTheme(theme));
    }, 100);
  }

  // pass reference to this down to ThemeChooser component
  getChildContext() {
    return {
      defaultTheme: this.props.defaultTheme,
      themeSwitcher: this,
      themes: [ ...this.state.themeOptions ],
      currentTheme: this.state.currentTheme
    };
  }

  async loadTheme(theme) {
    if (!this.state.themeOptions.has(theme)) { return; }

    if (!(theme in this.state.themes)) {
      themeActions.loadTheme(theme).then(rsp => {
        this.setState(prevState => ({
          themes: {
            ...prevState.themes,
            [rsp.theme]: rsp.styles
          }
        }));
      });
    }
  }

  async load(theme) {
    if (!theme) {
      const storedTheme = getItem(this.props.storeThemeKey);
      // see if a theme was previously stored, will return null if storedThemeKey not set
      // eslint-disable-next-line no-param-reassign
      theme = storedTheme || this.props.defaultTheme;
    }

    if (!this.state.themeOptions.has(theme)) { return; }

    setItem(this.props.storeThemeKey, theme);
    this.setState({
      currentTheme: theme
    });

    if (Object.keys(this.state.themes).indexOf(theme) === -1) {
      return themeActions.loadTheme(theme).then(rsp => {
        this.setState(prevState => ({
          themes: {
            ...prevState.themes,
            [rsp.theme]: rsp.styles
          }
        }));
      });
    }
  }

  getContents() {
    if (Object.keys(this.state.themes).length === 0) {
      return (
        <div style={{
          display: 'table',
          position: 'fixed',
          top: 0,
          height: '100%',
          width: '100%'
        }}>
          <div style={{
            display: 'table-cell',
            textAlign: 'center',
            verticalAlign: 'middle'
          }}>
            <div className="loader" />
            <p className='pt-0 mt-0'>Loading...</p>
          </div>
        </div>
      );
    }
    return this.props.children || <span />;
  }

  render() {
    return (
      <div>
        <Helmet>
          <style type="text/css" data-type="theme">
            { this.state.themes[this.state.currentTheme] || '' }
          </style>
        </Helmet>
        { this.getContents() }
      </div>
    );
  }
}

ThemeSwitcher.childContextTypes = {
  defaultTheme: PropTypes.string,
  themeSwitcher: PropTypes.instanceOf(ThemeSwitcher),
  themes: PropTypes.array,
  currentTheme: PropTypes.string
};

ThemeSwitcher.propTypes = {
  defaultTheme: PropTypes.string,
  storeThemeKey: PropTypes.string,
  themes: PropTypes.object,
  themeOptions: PropTypes.array,
  children: PropTypes.element
};

ThemeSwitcher.defaultProps = {
  defaultTheme: 'lumen',
  storeThemeKey: null,
  themes: null,
  themeOptions: validThemes,
  children: null
};

export default ThemeSwitcher;