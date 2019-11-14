const webpack = require('webpack')
const path = require('path')

const HtmlWebpackPlugin = require('html-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const DeadCodePlugin = require('webpack-deadcode-plugin')
const FaviconsWebpackPlugin = require('favicons-webpack-plugin')
const BundleTracker = require('webpack-bundle-tracker')

const ROOT_DIR = path.join(__dirname, '..')
const BUILD_DIR = path.join(ROOT_DIR, 'build')
const COMPONENTS_DIR = path.join(ROOT_DIR, 'src', 'components')
const DEPEND_DIR = path.join(COMPONENTS_DIR, 'dependencies')

const config  = {
  mode: 'none',
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
    modules: [
      'node_modules',
      path.join(ROOT_DIR, 'src')
    ],
    extensions: ['.js', '.jsx', '.json', '.css']
  },
  plugins: [
    new DeadCodePlugin({
      patterns: [
        'src/**/*.(js|jsx|css)',
      ],
      exclude: [
        '**/*.(stories|spec).(js|jsx)',
      ]
    }),
    new HtmlWebpackPlugin({
      title: 'HtmlWebpackPlugin',
      filename: 'index.html',
      template: path.join(DEPEND_DIR, 'index.html')
    }),
    new BundleTracker({
      filename: './webpack.stats.json'
    }),
    new webpack.ProvidePlugin({ // REMOVE ME!!
      moment: 'moment'
    }),
    new MiniCssExtractPlugin({
      filename: "css/[name].bundle.min.css",
      chunkFilename: "css/[name].bundle.min.css",
      allChunks: true
    }),
    new CopyWebpackPlugin([
      { // Custom Assets
        from: path.join(DEPEND_DIR, 'assets'),
        to: path.join(BUILD_DIR, 'assets'),
        toType: 'dir'
      },
      { // Theme Assets
        from: path.join(COMPONENTS_DIR, 'utils', 'theme-switcher', 'assets'),
        to: path.join(BUILD_DIR, 'assets'),
        toType: 'dir'
      }
    ]),
    new FaviconsWebpackPlugin({
      logo: path.join(DEPEND_DIR, 'img', 'log-favicon.png'),
      prefix: 'img/favicons/',
      statsFilename: 'favicons-[hash].json',
      persistentCache: true,
      inject: true,
      background: '#ffffff',
      title: 'Logger UI',
      icons: {
        android: true,              // Create Android homescreen icon. `boolean` or `{ offset, background, mask, overlayGlow, overlayShadow }`
        appleIcon: true,            // Create Apple touch icons. `boolean` or `{ offset, background, mask, overlayGlow, overlayShadow }`
        appleStartup: true,         // Create Apple startup images. `boolean` or `{ offset, background, mask, overlayGlow, overlayShadow }`
        coast: false,               // Create Opera Coast icon. `boolean` or `{ offset, background, mask, overlayGlow, overlayShadow }`
        favicons: true,             // Create regular favicons. `boolean` or `{ offset, background, mask, overlayGlow, overlayShadow }`
        firefox: true,              // Create Firefox OS icons. `boolean` or `{ offset, background, mask, overlayGlow, overlayShadow }`
        opengraph: false,
        twitter: false,
        windows: true,              // Create Windows 8 tile icons. `boolean` or `{ offset, background, mask, overlayGlow, overlayShadow }`
        yandex: false               // Create Yandex browser icon. `boolean` or `{ offset, background, mask, overlayGlow, overlayShadow }`
      }
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
          chunks: 'all',
        },
        themes: {
          test: /[\\/]themes[\\/]/,
          name: 'themes',
          chunks: 'all',
        }
      }
    }
  },
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
          options: {
            babelrc: false,
            presets: [
              [
                '@babel/preset-env',
                {
                  modules: false,
                  exclude: [
                    'babel-plugin-transform-classes'
                  ]
                }
              ],
              '@babel/preset-react'
            ],
            plugins: [
              '@babel/plugin-syntax-dynamic-import',
              '@babel/plugin-proposal-object-rest-spread'
            ]
          }
        }
      },
      {
        test: /\.(c|le)ss$/,
        use: [
          MiniCssExtractPlugin.loader,
          {
            loader: 'css-loader',
            options: {
              url: false
            }
          },
          'less-loader'
        ]
      },
      {
        test: /\.(svg|jpe?g|gif|bmp|tiff|png|ico)$/,
        use: [{
          loader: 'url-loader',
          options: {
            limit: 25000,
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

module.exports = config