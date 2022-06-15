/**
 * Base webpack config used across other specific configs
 */
import path from 'path';
import webpack from 'webpack';
import { merge } from 'webpack-merge';

import HtmlWebpackPlugin from 'html-webpack-plugin';
import Loaders, { commonImages } from './webpack.loaders';

const NODE_ENV = 'production';

const ROOT_DIR = path.join(__dirname, '..');
const BUILD_DIR = path.join(ROOT_DIR, 'build');
const COMPONENTS_DIR = path.join(ROOT_DIR, 'src', 'components');
const DEPEND_DIR = path.join(COMPONENTS_DIR, 'dependencies');

export default {
  devtool: 'inline-source-map',
  entry: {
    main: path.join(ROOT_DIR, 'src', 'index.jsx')
  },
  output: {
    path: BUILD_DIR,
    publicPath: '/',
    filename: 'js/[name].bundle.min.js'
  },
  context: ROOT_DIR,
  resolve: {
    extensions: ['.js', '.jsx', '.json', '.ts', '.tsx'],
    modules: ['node_modules', path.join(ROOT_DIR, 'src')]
  },
  plugins: [
    new webpack.EnvironmentPlugin({
      NODE_ENV
    }),
    new HtmlWebpackPlugin({
      filename: 'index.html',
      template: path.join(DEPEND_DIR, 'index.html')
    })
  ],
  optimization: {
    mergeDuplicateChunks: true,
    runtimeChunk: false,
    splitChunks: {
      automaticNameDelimiter: '_',
      cacheGroups: {
        vendors: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all'
        },
        utils: {
          test: /components\/(static|utils)[\\/]/,
          name: 'utils',
          chunks: 'all'
        }
      }
    }
  },
  target: 'web',
  module: {
    rules: [
      {
        test: /\.[jt]sx?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            cacheDirectory: true
          }
        }
      },
      {
        test: /\.css$/,
        use: [
          'style-loader',
          Loaders.css
        ]
      },
      {
        test: /\.s[ac]ss$/,
        use: [
          'style-loader',
          Loaders.css,
          'sass-loader'
        ]
      },
      {  // WOFF Font
        test: /\.woff(\?v=\d+\.\d+\.\d+)?$/,
        use: merge(Loaders.url, {
          options: {
            mimetype: 'application/font-woff'
          }
        })
      },
      {  // WOFF2 Font
        test: /\.woff2(\?v=\d+\.\d+\.\d+)?$/,
        use: merge(Loaders.url, {
          options: {
            mimetype: 'application/font-woff'
          }
        })
      },
      {  // TTF Font
        test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
        use: merge(Loaders.url, {
          options: {
            mimetype: 'application/octet-stream'
          }
        })
      },
      {  // EOT Font
        test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,
        use: 'file-loader'
      },
      {
        test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
        loader: 'svg-url-loader',
        options: {
          limit: 10 * 1024,
          noquotes: true,
          fallback: Loaders.file
        }
      },
      {  // Common Image Formats
        test: commonImages,
        use: Loaders.url
      }
    ]
  }
};
