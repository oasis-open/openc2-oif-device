/* eslint import/no-unresolved: off, import/no-self-import: off */
require('@babel/register');
const package = require('../package.json');

const config = require('./dev.config.babel').default;
config.externals = [...Object.keys(package.dependencies || {})];

module.exports = config;
