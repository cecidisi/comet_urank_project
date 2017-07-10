var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var WebpackCleanupPlugin = require('webpack-cleanup-plugin');
const ExtractTextPlugin = require("extract-text-webpack-plugin");


module.exports = {
  context: __dirname,

  entry: {
    vendor : './assets/vendor',
    main_comet : './assets/main_comet',
    main_conf_nav: './assets/main_conf_nav',
    main_conf_nav_eval: './assets/main_conf_nav_eval',
    conf_nav_eval_general: './assets/conf_nav_eval_general'
  },

  output: {
      path: path.resolve('./assets/bundles/'),
      // publicPath: '/static/bundles/',
      publicPath: 'http://localhost:8080/assets/bundles/', // Tell django to use this URL to load packages and not use STATIC_URL + bundle_name
      filename: "[name]-[hash].js",
  },

  devtool: 'source-map',

  module: {
    loaders: [    
      /* Generates separate css files */
      // {
      //     test: /\.css$/,
      //     use: ExtractTextPlugin.extract({
      //       use: "css-loader",
      //       fallback: "style-loader",
      //       allChunks: true
      //     })
      // },
      // {
      //     test: /\.scss$/,
      //     use: ExtractTextPlugin.extract({
      //       use: "css-loader!sass-loader",
      //       fallback: "style-loader",
      //       allChunks: true
      //     })
      // },

      /*  Style embedded in js (for debugging) */
      {
        test: /\.css$/,
        loader:  'style-loader!css-loader?sourceMap'
      },
      {
        test: /\.scss$/,
        loader:  'style-loader!css-loader?sourceMap!sass-loader?sourceMap'
      },

      { 
        test: /\.(jpe?g|png|gif)$/i, 
        loader: "file-loader" 
      },
      {
        test: /\.woff2?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        // Limiting the size of the woff fonts breaks font-awesome ONLY for the extract text plugin 
        // loader: "url?limit=10000" 
        loader: "url-loader?limit=10000"
      },
      {
        test: /\.(ttf|eot|svg)(\?[\s\S]+)?$/,
        loader: 'file-loader'
      }
      // { test: /\.js$/, loader: 'babel-loader', exclude: /node_modules/ },
      // , { test: /\main.js$/, exclude: /node_modules/, loader: 'babel-loader' }
    ],
  },

  plugins: [
    new webpack.HotModuleReplacementPlugin(),
    // Clean /bundles folder
    new WebpackCleanupPlugin(),
    // Tracks generated static files so that Django can find them
    new BundleTracker({filename: './webpack-stats.json'}),
    // Generate separate .css files
    new ExtractTextPlugin("[name]-[hash].css"),
    // Separate vendor modules from main entries
    new webpack.optimize.CommonsChunkPlugin("vendor"),
    // Expose vendor modules as global variables
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      d3 : "d3",
      _ : 'underscore',
      colorbrewer: 'colorbrewer'
    })
  ],

  resolve: {
    modules : ['node_modules'],
    alias: {
      d3: 'd3/d3',
      'jquery-ui': 'jquery-ui-bundle',
      bootstrap: 'bootstrap-sass',
      urank: path.resolve(__dirname, "plugins/urank/js/controller/urank")
    }
  },

  stats : {
    colors : true
  }

}