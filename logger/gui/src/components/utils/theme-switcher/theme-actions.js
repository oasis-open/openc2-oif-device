// Actions for Theme endpoints
const baseAPI = '/assets/css/'; // ${theme}.css`

// API Calls
// GET - '/assets/css/{theme}.css'
export const loadTheme = async theme => {
  return fetch(`${window.location.origin}${baseAPI}${theme}.css`)
    .then(rsp => rsp.text())
    .then(data => ({
      theme,
      styles: data
    }))
    .catch(err => ({
      err,
      theme,
      styles: ''
    }));
};
