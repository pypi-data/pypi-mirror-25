const webpack = require('webpack');
const path = require('path');
const ManifestPlugin = require('webpack-manifest-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');

// input dir
const APP_DIR = path.resolve(__dirname, './');

// output dir
const BUILD_DIR = path.resolve(__dirname, './dist');

const config = {
  //devtool: 'eval-source-map',//配置生成Source Maps，选择合适的选项
  node: {
    fs: 'empty',
  },
  entry: {
    'jquery': ['jquery'],
    'bootstrap': ['bootstrap'],
    'react': ['react'],
    'd3': ['d3','d3-cloud','d3-sankey','d3-scale'],
    'd3-tip': ['d3-tip'],
    'nvd3': ['nvd3'],
    'redux': ['redux'],
    'echarts': ['echarts'],
    'ag-grid': ['ag-grid-react', 'ag-grid','ag-grid-enterprise'],
    'react-ace': ['react-ace'],
    'react-bootstrap': [ 'react-bootstrap'],
    'react-bootstrap-table': ['react-bootstrap-table'],
    'react-dom': ['react-dom'],
    'react-gravatar': ['react-gravatar'],
    'react-grid-layout': ['react-grid-layout'],
    'react-map-gl': ['react-map-gl'],
    'react-redux': ['react-redux'],
    'react-resizable': ['react-resizable'],
    'react-select': ['react-select'],
    'react-syntax-highlighter': ['react-syntax-highlighter'],
    'datatables.net-bs': ['datatables.net-bs'],

    theme: APP_DIR + '/javascripts/theme.js',
    common: APP_DIR + '/javascripts/common.js',
    addSlice: ['babel-polyfill', APP_DIR + '/javascripts/addSlice/index.jsx'],
    explore: ['babel-polyfill', APP_DIR + '/javascripts/explore/index.jsx'],
    dashboard: ['babel-polyfill', APP_DIR + '/javascripts/dashboard/Dashboard.jsx'],
    sqllab: ['babel-polyfill', APP_DIR + '/javascripts/SqlLab/index.jsx'],
    welcome: ['babel-polyfill', APP_DIR + '/javascripts/welcome.js'],
    profile: ['babel-polyfill', APP_DIR + '/javascripts/profile/index.jsx'],
    scheduler: ['babel-polyfill', APP_DIR + '/javascripts/scheduler/index.jsx'],
    dashboard_download: ['babel-polyfill', APP_DIR + '/javascripts/download/index.jsx'],
  },
  output: {
    path: BUILD_DIR,
    filename: '[name].[chunkhash].entry.js',
    chunkFilename: '[name].[chunkhash].entry.js',
  },
  resolve: {
    extensions: [
      '.js',
      '.jsx',
    ],
    alias: {
      webworkify: 'webworkify-webpack',
    },
  },
  module: {
    // noParse: /mapbox-gl\/dist/,
    loaders: [
      {
        test: /datatables\.net.*/,
        loader: 'imports-loader?define=>false',
      },
      {
        test: /mapbox-gl\/.*\.js$/,
        loader: 'babel-loader',
        query: {
          presets: [
            'es2015',
          ],
        },
      },

      {
        test: /\.jsx?$/,
        // exclude: APP_DIR + '/node_modules',
        exclude: [
          APP_DIR + '/node_modules',
          '/cache/superset19/node_modules/',
        ],
        loader: 'babel-loader',
        query: {
          presets: [
            'airbnb',
            'es2015',
            'react',
          ],
          "plugins": [
            ["import", { "libraryName": "antd", "style": true }],
          ]
        },
      },
      // Extract css files
      {
        test: /\.js$/,
        // include: APP_DIR + '/node_modules/mapbox-gl/js',
        include: [
          APP_DIR + '/node_modules/mapbox-gl/js',
          '/cache/superset19/node_modules/mapbox-gl/js',
        ],
        loader: 'babel-loader',
      },
      // Extract css files
      {
        test: /\.css$/,
        // include: APP_DIR,
        include: [
          APP_DIR,
          '/cache/superset19/node_modules/',
        ],
        loader: ExtractTextPlugin.extract({
          use: ['css-loader'],
          fallback: 'style-loader',
        }),
      },
      // Optionally extract less files
      // or any other compile-to-css language
      {
        test: /\.less$/,
        // include: APP_DIR,
        include: [
          APP_DIR,
          '/cache/superset19/',
        ],
        loader: ExtractTextPlugin.extract({
          use: ['css-loader', 'less-loader'],
          fallback: 'style-loader',
        }),
      },
      /* for css linking images */
      {
        test: /\.png$/,
        loader: 'url-loader?limit=100000',
      },
      {
        test: /\.jpg$/,
        loader: 'file-loader',
      },
      {
        test: /\.gif$/,
        loader: 'file-loader',
      },
      /* for font-awesome */
      {
        test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        loader: 'url-loader?limit=10000&mimetype=application/font-woff',
      },
      {
        test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        loader: 'file-loader',
      },
      /* for mapbox */
      {
        test: /\.json$/,
        loader: 'json-loader',
      },
      {
        test: /\.js$/,
        include: APP_DIR + '/node_modules/mapbox-gl/js/render/painter/use_program.js',
        loader: 'transform/cacheable?brfs',
      },
      /* for require('*.po') */
      {
        test: /\.po$/,
        loader: 'po-catalog-loader',
        query: {
          referenceExtensions: ['.js', '.jsx'],
          domain: 'superset',
        },
      },
    ],
  },
  externals: {
    cheerio: 'window',
    'react/lib/ExecutionEnvironment': true,
    'react/lib/ReactContext': true,
  },
  plugins: [
    new ManifestPlugin(),
    new CleanWebpackPlugin(['dist']),
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify(process.env.NODE_ENV),
      },
    }),
    new ExtractTextPlugin('[name].[chunkhash].css'),
    new webpack.ProvidePlugin({
      $: "jquery",
      jQuery: "jquery",
      "window.jQuery": "jquery"
    }),
    new webpack.optimize.CommonsChunkPlugin({name: [
      'datatables.net-bs',
      'react-syntax-highlighter',
      'react-select', 
      'react-resizable', 
      'react-redux',
      'react-map-gl', 
      'react-grid-layout',
      'react-gravatar',
      'react-dom', 
      'react-bootstrap-table',
      'react-bootstrap', 
      'react-ace',
      'ag-grid',
      'echarts',
      'redux',
      'nvd3', 
      'd3-tip', 
      'd3',
      'react',
      'bootstrap',
      'jquery'
    ],  minChunks: Infinity}),
  ],
};
if (process.env.NODE_ENV === 'production') {
  // Using settings suggested in https://github.com/webpack/webpack/issues/537
  const UJSplugin = new webpack.optimize.UglifyJsPlugin({
    sourceMap: false,
    minimize: true,
    parallel: {
      cache: true,
      workers: 4,
    },
    compress: false,
  });
  config.plugins.push(UJSplugin);
}
module.exports = config;