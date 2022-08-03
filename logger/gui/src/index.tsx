import React from 'react';
import ReactDOM from 'react-dom';
import { HelmetProvider } from 'react-helmet-async';

// Styles
import { ThemeSwitcher } from 'react-bootswatch-theme-switcher';
import './components/dependencies/css/searchkit.css';

import App from './app';
import registerServiceWorker from './registerServiceWorker';

// Theme Options
const validThemes = ['cyborg', 'darkly', 'lumen', 'slate', 'solar', 'superhero'];

const Root = () => (
  <ThemeSwitcher storeThemeKey="theme" defaultTheme="lumen" themeRoot="assets" themeOptions={ validThemes }>
    <HelmetProvider>
      <App />
    </HelmetProvider>
  </ThemeSwitcher>
);

ReactDOM.render(<Root />, document.getElementById('root'));
registerServiceWorker();
