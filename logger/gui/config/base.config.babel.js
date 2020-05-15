import webpack from 'webpack';
import path from 'path';

import HtmlWebpackPlugin from 'html-webpack-plugin';

const env = 'production';

const ROOT_DIR = path.join(__dirname, '..');
const BUILD_DIR = path.join(ROOT_DIR, 'build');
const COMPONENTS_DIR = path.join(ROOT_DIR, 'src', 'components');
const DEPEND_DIR = path.join(COMPONENTS_DIR, 'dependencies');

export default {
  mode: env,
  devtool: 'inline-source-map',
  entry: {
    main: path.join(ROOT_DIR, 'src', 'index.js')
  },
  output: {
    path: BUILD_DIR,
    publicPath: '/',
    filename: 'js/[name].bundle.min.js'
  },
  context: ROOT_DIR,
  resolve: {
    extensions: ['.js', '.jsx', '.json'],
    modules: ['node_modules', path.join(ROOT_DIR, 'src')]
  },
  plugins: [
    new webpack.DefinePlugin({
      NODE_ENV: env
    }),
    new webpack.NamedModulesPlugin(),
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
          test: /components\/utils[\\/]/,
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
        test: /\.jsx?$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
          options: {
            cacheDirectory: true
          }
        }
      },
      {
        test: /\.(c|le)ss$/,
        use: [
          'style-loader',
          {
            loader: 'css-loader',
            options: {
              url: false
            }
          },
          {
            loader: 'less-loader',
            options: {
              strictMath: true
            }
          }
        ]
      },
      {
        test: /\.svg$/,
        loader: 'svg-url-loader',
        options: {
          limit: 10 * 1024,
          noquotes: true,
          fallback: {
            loader: 'file-loader',
            options: {
              name: 'assets/img/[name].[ext]'
            }
          }
        }
      },
      {
        test: /\.(jpe?g|gif|bmp|tiff|png|ico)$/,
        use: [{
          loader: 'url-loader',
          options: {
            limit: 10 * 1024,
            fallback: {
              loader: 'file-loader',
              options: {
                name: 'assets/img/[name].[ext]'
              }
            }
          }
        }]
      },
      {
        test: /\.(ttf|eot|woff|woff2)$/,
        use: [{
          loader: 'file-loader',
          options: {
            name: 'css/fonts/[name].[ext]'
          }
        }]
      }
    ]
  }
};
