import React, { Suspense, lazy } from 'react'
import PropTypes from 'prop-types'
import './assets/css/loader.css'

const setItem = (key, obj) => {
    if (!key) return null;
    try {
        localStorage.setItem(key, JSON.stringify(obj));
    } catch (err) {
        return null;
    }
}

const getItem = (key) => {
    if (!key) return null;
    try {
        let item = localStorage.getItem(key)
        return item ? JSON.parse(item) : null;
    } catch (err) {
        return null;
    }
}

const loader = (styles, cb) => {
    const head = document.getElementsByTagName('head')[0];
    let styleElm = document.createElement('style')
    styleElm.setAttribute("type", "text/css")
    styleElm.setAttribute("data-type", "theme")
    styleElm.innerHTML = styles !== '' ? styles : ''
    head.append(styleElm)

    if (typeof(cb) === "function") {
        cb()
    }
}

// check if boootstrap styles are loaded
const isLoaded = () =>  {
    const head = document.getElementsByTagName('head')[0];
    const nodes = head.childNodes;
    let loaded = false;

    nodes.forEach(node => {
        let tag = (node.tagName || '').toLowerCase()
        let dataAttrs = node.dataset || {}
        let theme = dataAttrs.hasOwnProperty('type') ? (dataAttrs.type == 'theme') : false
        let styles = node.innerHTML !== ''

        if (tag == 'style' && theme && styles) {
            loaded = true;
        }
    })
    return loaded;
}

// remove any bootstrap style
const removeCurrentTheme = () => {
    const head = document.getElementsByTagName('head')[0];
    const nodes = head.childNodes;

    nodes.forEach(node => {
        let tag = (node.tagName || '').toLowerCase()
        let dataAttrs = node.dataset || {}
        let theme = dataAttrs.hasOwnProperty('type') ? (dataAttrs.type == 'theme') : false

        if (tag == 'style' && theme) {
            head.removeChild(node)
        }
    })
}

//------------------------------------------------------------------------------
// Top level ThemeSwitcher Component
//------------------------------------------------------------------------------
class ThemeSwitcher extends React.Component {
    constructor(props, context) {
        super(props, context);
        this.load = this.load.bind(this);
        this.loadTheme = this.loadTheme.bind(this);

        if (Object.keys(this.props.themes || {}).length === 0) {
            import(
                /* webpackChunkName: "themes" */
                /* webpackMode: "lazy" */
                /* webpackPrefetch: true */
                /* webpackPreload: true */
                './themes'
            ).then(theme_module => {
                this.setState({
                    themes: theme_module
                }, () => {
                    let storedTheme = getItem(this.props.storeThemeKey)
                    let theme = storedTheme ? storedTheme : this.props.defaultTheme
                    this.load(theme)
                })
            })
        }

        this.state = {
            loaded: false,
            currentTheme: null,
            themes: this.props.themes || {}
        }
    }

    componentDidMount() {
        if (!isLoaded()) {
            this.load(); // load default theme
        }
    }

    loadTheme(name) {
        name = Object.keys(this.state.themes).indexOf(name) >= 0 ? name : this.props.defaultTheme
        removeCurrentTheme()

        setItem(this.props.storeThemeKey, name);
        loader(this.state.themes[name], () => {
            this.setState({
                loaded: true,
                currentTheme: name
            })
        })
    }

    load(theme) {
        this.setState({
            loaded: false
        })

        if (!theme) {
            let storedTheme = getItem(this.props.storeThemeKey)
            // see if a theme was previously stored, will return null if storedThemeKey not set
            theme = storedTheme ? storedTheme : this.props.defaultTheme
        }

        this.loadTheme(theme)
    }

    // pass reference to this down to ThemeChooser component
    getChildContext() {
        return {
            defaultTheme: this.props.defaultTheme,
            themeSwitcher: this,
            themes: this.props.themeOptions.filter(t => true),
            currentTheme: this.state.currentTheme
        }
    }

    render() {
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
            )
        } else {
            return this.props.children || <span />
        }
    }
}

ThemeSwitcher.childContextTypes = {
    defaultTheme: PropTypes.string,
    themeSwitcher: PropTypes.object,
    themes: PropTypes.array,
    currentTheme: PropTypes.string
};

ThemeSwitcher.propTypes = {
    defaultTheme: PropTypes.string,
    storeThemeKey: PropTypes.string,
    themes: PropTypes.object,
    themeOptions: PropTypes.array
};

ThemeSwitcher.defaultProps = {
    defaultTheme: 'lumen',
    storeThemeKey: null,
    themes: null,
    themeOptions: ['cerulean', 'cosmo', 'cyborg', 'darkly', 'flatly', 'journal', 'litera', 'lumen', 'lux', 'materia', 'minty', 'pulse', 'sandstone', 'simplex', 'sketchy', 'slate', 'solar', 'spacelab', 'superhero', 'united', 'yeti']
};

export default ThemeSwitcher;