import path from 'path';
import webpack from 'webpack';
import { merge } from 'webpack-merge';

import DeadCodePlugin from 'webpack-deadcode-plugin';
import CircularDependencyPlugin from 'circular-dependency-plugin';

import baseConfig from './webpack.config.base';

const NODE_ENV = 'development';

const ROOT_DIR = path.join(__dirname, '..');
const BUILD_DIR = path.join(ROOT_DIR, 'build');
const COMPONENTS_DIR = path.join(ROOT_DIR, 'src', 'components');
const DEPEND_DIR = path.join(COMPONENTS_DIR, 'dependencies');

export default merge(baseConfig, {
  mode: NODE_ENV,
  devtool: 'eval',
  plugins: [
    new webpack.DefinePlugin({
      NODE_ENV
    }),
    new DeadCodePlugin({
      patterns: [
        'src/**/*.(js|jsx|css|less)'
      ],
      exclude: [
        '**/*.(stories|spec).(js|jsx)$',
        DEPEND_DIR
      ]
    }),
    new CircularDependencyPlugin({
      exclude: /node_modules/,
      failOnError: false,
      allowAsyncCycles: false,
      cwd: ROOT_DIR
    }),
    new webpack.NoEmitOnErrorsPlugin()
  ],
  devServer: {
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
    },
    static: {
      directory: BUILD_DIR
    }
  },
  optimization: {
    usedExports: true
  }
});
