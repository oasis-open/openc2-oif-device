import webpack from 'webpack';
import merge from 'webpack-merge';
import path from 'path';

import DeadCodePlugin from 'webpack-deadcode-plugin';
// import CircularDependencyPlugin from 'circular-dependency-plugin';

import baseConfig from './base.config.babel';

const env = 'development';

const ROOT_DIR = path.join(__dirname, '..');
const BUILD_DIR = path.join(ROOT_DIR, 'build');
const COMPONENTS_DIR = path.join(ROOT_DIR, 'src', 'components');
const DEPEND_DIR = path.join(COMPONENTS_DIR, 'dependencies');

export default merge(baseConfig, {
  mode: env,
  devtool: 'eval',
  plugins: [
    new webpack.DefinePlugin({
      NODE_ENV: env
    }),
    new DeadCodePlugin({
      patterns: [
        'src/**/*.(js|jsx|css|less)'
      ],
      exclude: [
        '**/*.(stories|spec).(js|jsx)$',
        DEPEND_DIR,
        '**/theme-switcher/download_themes.js',
        path.join(COMPONENTS_DIR, 'utils', 'theme-switcher', 'assets')
      ]
    }),/*
    new CircularDependencyPlugin({
      exclude: /node_modules/,
      failOnError: false,
      allowAsyncCycles: false,
      cwd: ROOT_DIR
    }),*/
  ],
  devServer: {
    contentBase: BUILD_DIR,
    compress: true,
    port: 3000,
    hot: true,
    open: false,
    historyApiFallback: true,
    proxy: {
      '/api': {
        target: 'http://localhost:9200',
        pathRewrite: {"^/api/" : ""},
        secure: false
      }
    }
  },
  optimization: {
    usedExports: true
  }
});
