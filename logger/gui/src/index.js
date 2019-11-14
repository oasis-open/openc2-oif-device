import React from 'react'
import ReactDOM from 'react-dom'

// Styles
import { ThemeSwitcher } from './components/utils'
import 'bootstrap'
import './components/dependencies/css/searchkit.less'

import App from './app'
import registerServiceWorker from './registerServiceWorker'

// Theme Options
const validThemes = ['cyborg', 'darkly', 'lumen', 'slate', 'solar', 'superhero']

const Root = () => (
  <ThemeSwitcher storeThemeKey="theme" defaultTheme="lumen" themeOptions={ validThemes }>
    <App />
  </ThemeSwitcher>
)

ReactDOM.render(<Root />, document.getElementById('root'));

registerServiceWorker()
