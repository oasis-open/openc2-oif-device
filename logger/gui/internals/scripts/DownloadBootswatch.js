#!/usr/bin/env node
const path = require('path');
const fs = require('fs-extra');
const NamedRegExp = require('named-regexp-groups');
const download = require('download-file');
const request = require('sync-request');
const csso = require('csso');

const ROOT_DIR = path.join(__dirname, '..', '..', 'src', 'components', 'utils', 'theme-switcher');
const CHECK_DIRS = ['assets', 'assets/css', 'assets/fonts'];

const THEME_API = 'https://bootswatch.com/api/4.json';
const THEME_FONT_DIR = '/assets/';
const THEME_FONT_URL = '../assets/';

const CSS_URL_IMPORT = new NamedRegExp(/^@import url\(["'](:<url>.*?)["']\);\s*?$/);
const FILE_URL_IMPORT = new NamedRegExp(/\s*?src:( local\(.*?\),)? local\(['"](:<name>.*?)['"]\), url\(['"]?(:<url>.*?)['"]?\) format\(['"](:<format>.*?)['"]\);/);
const URL_REPLACE = new NamedRegExp(/url\([""]?(:<url>.*?)[""]?\)/);

CHECK_DIRS.forEach(d => {
  const dir = path.join(ROOT_DIR, d);
  if (!fs.pathExistsSync(dir)) {
    fs.mkdirSync(dir);
  }
});

let BootswatchThemes = request('GET', THEME_API);
BootswatchThemes = JSON.parse(BootswatchThemes.getBody('utf8'));
const themeNames = [];

BootswatchThemes.themes.forEach(theme => {
  console.log(`Downloading Theme: ${theme.name}`);
  const themeName = theme.name.toLowerCase();
  themeNames.push(themeName);

  let preProcessCss = [];
  const css = request('GET', theme.css).getBody('utf8');

  css.split(/\n\r?/gm).forEach(line => {
    if (line.startsWith('@import url(')) {
      const cssImportURL = line.replace(CSS_URL_IMPORT, '$+{url}');
      const cssImport = request('GET', cssImportURL).getBody('utf8');

      preProcessCss.push(`/* ${line} */`);
      preProcessCss = preProcessCss.concat(cssImport.split(/\n\r?/g));
    } else {
      preProcessCss.push(line);
    }
  });

  // set imports to local & download files
  const postProcessCss = preProcessCss.map(line => {
    let processedLine = line;
    if (line.match(/\s*?src:.*url\(["']?https?:\/\/.*/) && !line.startsWith('/*')) {
      const src = FILE_URL_IMPORT.exec(line).groups;
      const ext = path.extname(src.url);
      const fileName = `fonts/${src.name}${ext}`;

      if (!fs.existsSync(path.join(ROOT_DIR, THEME_FONT_DIR, fileName))) {
        const opts = {
          directory: path.join(ROOT_DIR, THEME_FONT_DIR, 'fonts'),
          filename: src.name + ext
        };
        download(src.url, opts, err => {
          if (err) throw err;
          console.log(`Downloaded reference: ${opts.filename}`);
        });
      }
      processedLine = processedLine.replace(URL_REPLACE, `url('${THEME_FONT_URL}${fileName}')`);
    }

    processedLine = processedLine.replace(/\\[^\\]/g, '\\\\');
    processedLine = processedLine.replace(/^\s+\*/, '*');
    processedLine = processedLine.replace(/^\s+/, '\t');
    return processedLine;
  });

  const themeFile = fs.createWriteStream(path.join(ROOT_DIR, 'assets', 'css', `${themeName}.css`), {flags: 'w'});

  const minStyles = csso.minify(postProcessCss.join(''), {
    comments: false,
    restructure: true,
    sourceMap: false
  }).css;

  themeFile.write(minStyles);
  themeFile.end();
});

// make theme index file
const themeIndexFile = fs.createWriteStream(path.join(ROOT_DIR, 'themes.js'), {flags: 'w'});
themeIndexFile.write(`const validThemes = [\n  '${themeNames.join("',\n  '")}'\n];\n`);
themeIndexFile.write('export default validThemes;');
themeIndexFile.end();
