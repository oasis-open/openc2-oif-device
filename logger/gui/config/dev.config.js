const generalConfig = require('./general.config')
const webpack = require('webpack')
const merge = require('webpack-merge')
const path = require('path')

env = 'development'
console.log('NODE_ENV: ' + env)

const ROOT_DIR = path.join(__dirname, '..')
const BUILD_DIR = path.join(ROOT_DIR, 'build')

const config = merge(generalConfig, {
  mode: env,
  devtool: 'eval',
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify(env),
      }
    }),
    new webpack.NoEmitOnErrorsPlugin(),
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
    usedExports: true,
  }
});

module.exports = config