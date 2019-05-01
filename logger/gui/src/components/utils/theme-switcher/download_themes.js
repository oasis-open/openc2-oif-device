#!/usr/bin/env node

const path = require('path');
const fs = require('fs-extra');
const NamedRegExp = require('named-regexp-groups');
const download = require('download-file');
const request = require('sync-request');
const csso = require('csso');

const ROOT_DIR = __dirname
const CHECK_DIRS = ['themes', 'assets', 'assets/fonts']

const THEME_API = 'https://bootswatch.com/api/4.json'
const THEME_FONT_DIR = '/assets/'

const CSS_URL_IMPORT = new NamedRegExp(/^@import url\([\"\'](:<url>.*?)[\"\']\);\s*?$/);
const FILE_URL_IMPORT = new NamedRegExp(/\s*?src:( local\(.*?\),)? local\([\'\"](:<name>.*?)[\'\"]\), url\([\'\"]?(:<url>.*?)[\'\"]?\) format\([\'\"](:<format>.*?)[\'\"]\);/);
const URL_REPLACE = new NamedRegExp(/url\([\"\"]?(:<url>.*?)[\"\"]?\)/)

for (i in CHECK_DIRS) {
    let dir = path.join(ROOT_DIR, CHECK_DIRS[i])
    if (!fs.pathExistsSync(dir)) {
        fs.mkdirSync(dir);
    }
}

let themes = request('GET', THEME_API);
themes = JSON.parse(themes.getBody('utf8'));
theme_names = []

for (let theme of themes['themes']) {
    console.log('Downloading Theme: ' + theme['name']);
    let theme_name = theme['name'].toLowerCase();
    theme_names.push(theme_name)

    let css = request('GET', theme['css']).getBody('utf8'),
        pre_css_lines = [],
        post_css_lines = []

    for (let line of css.split(/\n\r?/gm)) {
        if (line.startsWith('@import url(')) {
            let css_import_url = line.replace(CSS_URL_IMPORT, "$+{url}");
            css_import = request('GET', css_import_url).getBody('utf8');

            pre_css_lines.push('/* ' + line + ' */')
            pre_css_lines = pre_css_lines.concat(css_import.split(/\n\r?/g))
        } else {
            pre_css_lines.push(line)
        }
    }

    // set imports to local & download files
    for (let line of pre_css_lines) {
        if (line.match(/\s*?src:.*url\([\"\']?https?:\/\/.*/) && !line.startsWith('/*')) {
            let src = FILE_URL_IMPORT.exec(line)['groups']
            let ext = path.extname(src['url'])
            let fileName = 'fonts/' + src['name'] + ext

            if (!fs.existsSync(path.join(ROOT_DIR, THEME_FONT_DIR, fileName))) {
                let opts = {
                    directory: path.join(ROOT_DIR, THEME_FONT_DIR, 'fonts'),
                    filename: src['name'] + ext
                }
                download(src['url'], opts, (err) => {
                    if (err) throw err
                    console.log("Downloaded file: " + opts['filename'])
                });
            }
            line = line.replace(URL_REPLACE, 'url(\'' + THEME_FONT_DIR + fileName + '\')')
        }

        line = line.replace(/\\[^\\]/g, '\\\\')
        line = line.replace(/^\s+\*/, '*')
        line = line.replace(/^\s+/, '\t')
        post_css_lines.push(line)
    }

    let css_file = fs.createWriteStream(path.join(ROOT_DIR, 'themes', theme_name + '.js'), {
        flags: 'w'
    });
    css_file.write('export default `\n')

    css_file.write(csso.minify(post_css_lines.join(''), {
        comments: false,
        restructure: true,
        sourceMap: false
    }).css)

    css_file.write('\n`')
    css_file.end();
}

// make theme index file
let theme_index_file = fs.createWriteStream(path.join(ROOT_DIR, 'themes', 'index.js'), {
    flags: 'w'
});

for (let name of theme_names) {
    theme_index_file.write('import ' + name + ' from \'./' + name + '\'\n')
}
theme_index_file.write('\n\n')
theme_index_file.write('export {\n')
for (let name of theme_names) {
    theme_index_file.write('\t' + name + ',\n')
}
theme_index_file.write('}')

theme_index_file.end()
