import React from 'react';
import ReactDOM from 'react-dom';
import { HelmetProvider } from 'react-helmet-async';

// Styles
import 'bootstrap';
import { ThemeSwitcher } from './components/utils';
import './components/dependencies/css/searchkit.less';

import App from './app';
import registerServiceWorker from './registerServiceWorker';

// Theme Options
const validThemes = ['cyborg', 'darkly', 'lumen', 'slate', 'solar', 'superhero'];

const Root = () => (
  <HelmetProvider>
    <ThemeSwitcher storeThemeKey="theme" defaultTheme="lumen" themeOptions={ validThemes }>
      <App />
    </ThemeSwitcher>
  </HelmetProvider>
);

ReactDOM.render(<Root />, document.getElementById('root'));
registerServiceWorker();
