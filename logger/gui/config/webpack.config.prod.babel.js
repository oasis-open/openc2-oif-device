import webpack from 'webpack';
import { merge } from 'webpack-merge';
import path from 'path';

import CopyWebpackPlugin from 'copy-webpack-plugin';
import FaviconsWebpackPlugin from 'favicons-webpack-plugin';
import MiniCssExtractPlugin from 'mini-css-extract-plugin';
import OptimizeCSSAssetsPlugin from 'optimize-css-assets-webpack-plugin';
import TerserPlugin from 'terser-webpack-plugin';
import { BundleAnalyzerPlugin } from 'webpack-bundle-analyzer';
import { CleanWebpackPlugin } from 'clean-webpack-plugin';

import baseConfig from './webpack.config.base';
import Loaders from './webpack.loaders';

const NODE_ENV = 'production';

const ROOT_DIR = path.join(__dirname, '..');
const BUILD_DIR = path.join(ROOT_DIR, 'build');
const COMPONENTS_DIR = path.join(ROOT_DIR, 'src', 'components');
const DEPEND_DIR = path.join(COMPONENTS_DIR, 'dependencies');

export default merge(baseConfig, {
  mode: NODE_ENV,
  devtool: 'source-map',
  plugins: [
    new webpack.DefinePlugin({
      NODE_ENV
    }),
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      generateStatsFile: true,
      openAnalyzer: false,
      statsFilename: path.join(ROOT_DIR, 'analyzer.stats.json'),
      reportFilename: path.join(ROOT_DIR, 'analyzer.stats.html')
    }),
    new MiniCssExtractPlugin({
      filename: 'css/[name].bundle.min.css',
      chunkFilename: 'css/[name].bundle.min.css'
    }),
    new CopyWebpackPlugin({
      patterns: [
        { // Custom Assets
          from: path.join(DEPEND_DIR, 'assets'),
          to: path.join(BUILD_DIR, 'assets'),
          toType: 'dir'
        },
        { // Theme Assets
          from: path.resolve('node_modules', 'react-bootswatch-theme-switcher', 'assets'),
          to: path.join(BUILD_DIR, 'assets'),
          toType: 'dir'
        }
      ]
    }),
    new FaviconsWebpackPlugin({
      logo: path.join(DEPEND_DIR, 'img', 'log-favicon.png'),
      cache: true,
      outputPath: 'img/favicons/',
      prefix: 'img/favicons/',
      statsFilename: 'favicons-[hash].json',
      inject: true,
      favicons: {
        appName: 'Logger UI',
        background: '#ffffff',
        theme_color: '#333',
        appleStatusBarStyle: 'black-translucent',
        pixel_art: false,
        icons: {
          android: true,        // Create Android homescreen icon. `boolean` or `{ offset, background, mask, overlayGlow, overlayShadow }`
          appleIcon: true,      // Create Apple touch icons. `boolean` or `{ offset, background, mask, overlayGlow, overlayShadow }`
          appleStartup: false,  // Create Apple startup images. `boolean` or `{ offset, background, mask, overlayGlow, overlayShadow }`
          coast: false,         // Create Opera Coast icon. `boolean` or `{ offset, background, mask, overlayGlow, overlayShadow }`
          favicons: true,       // Create regular favicons. `boolean` or `{ offset, background, mask, overlayGlow, overlayShadow }`
          firefox: true,        // Create Firefox OS icons. `boolean` or `{ offset, background, mask, overlayGlow, overlayShadow }`
          opengraph: false,
          twitter: false,
          windows: true,        // Create Windows 8 tile icons. `boolean` or `{ offset, background, mask, overlayGlow, overlayShadow }`
          yandex: false         // Create Yandex browser icon. `boolean` or `{ offset, background, mask, overlayGlow, overlayShadow }`
        }
      }
    }),
    new CleanWebpackPlugin({
      dry: false
    })
  ],
  optimization: {
    minimizer: [
      new TerserPlugin({
        extractComments: false,
        parallel: true
      }),
      new OptimizeCSSAssetsPlugin({
        cssProcessorPluginOptions: {
          preset: [
            'default',
            {
              discardComments: {
                removeAll: true
              }
            }
          ]
        },
        canPrint: true
      })
    ]
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          Loaders.css
        ]
      },
      {
        test: /\.s[ac]ss$/,
        use: [
          MiniCssExtractPlugin.loader,
          Loaders.css,
          'sass-loader'
        ]
      }
    ]
  }
});
