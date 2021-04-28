import React, { Component } from 'react';
import PropTypes from 'prop-types';

const capitalize = s => s.charAt(0).toUpperCase() + s.substring(1);

class ThemeChooser extends Component {
  constructor(props, context) {
    super(props, context);
    this.onSelect = this.onSelect.bind(this);

    // get themes from context and sort them for display
    this.themes = [ ...context.themes ];

    this.themes.sort();

    this.state = {
      currentTheme: this.context.currentTheme || '',
      defaultTheme: this.context.defaultTheme
    };
  }

  onSelect(e) {
    e.preventDefault();
    this.setState({
      currentTheme: e.target.getAttribute('data-theme')
    }, () => {
      // eslint-disable-next-line promise/catch-or-return
      this.context.themeSwitcher.load(this.state.currentTheme).then(() => {
        return this.props.change(this.state.currentTheme);
      });
    });
  }

  render() {
    const themes = this.themes.map(theme => {
      return (
        <li key={ theme }>
          <a
            href='#'
            className={ `dropdown-item ${theme === this.state.currentTheme ? ' active' : ''}` }
            data-theme={ theme }
            onClick={ this.onSelect }
          >
            { theme === this.state.defaultTheme ? '* ' : '' }{ capitalize(theme) }
          </a>
        </li>
      );
    });

    return (
      <div className='dropdown dropdown-menu-right' style={ this.props.style }>
        <button
          id='theme-menu'
          className={ `btn btn-default dropdown-toggle ${this.props.size === '' ? '' : `btn-${this.props.size}` }` }
          type='button'
          data-toggle='dropdown'
          aria-haspopup='true'
          aria-expanded='true'
        >
          Theme
        </button>

        <ul className='dropdown-menu'>
          { themes }
        </ul>
      </div>
    );
  }
}

ThemeChooser.contextTypes = {
  defaultTheme: PropTypes.string,
  themeSwitcher: PropTypes.object,
  themes: PropTypes.array,
  currentTheme: PropTypes.string
};

ThemeChooser.propTypes = {
  style: PropTypes.object,
  size: PropTypes.oneOf(['sm', 'lg', '']),
  change: PropTypes.func
};

ThemeChooser.defaultProps = {
  style: {},
  size: '',
  change: () => {}
};

export default ThemeChooser;