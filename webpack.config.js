const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const TerserPlugin = require("terser-webpack-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");

const isProduction = process.env.NODE_ENV === "production";

/** @type {import("webpack").WebpackOptionsNormalized } */
module.exports = {
  mode: isProduction ? "production" : "development",
  entry: {
    main: [
      "./stopwatch/scss/index.scss",
      "./stopwatch/ts/index.ts"
    ],
  },
  devtool: isProduction ? false : "eval-source-map",

  module: {
    rules: [
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: "asset/resource",
      },
      {
        test: /\.jsx?/,
        use: [
          {
            loader: "babel-loader",
          },
        ],
      },
      {
        test: /\.(scss)$/,
        use: [
          {
            loader: isProduction ? MiniCssExtractPlugin.loader : "style-loader",
          },
          {
            loader: "css-loader",
          },
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                plugins: function () {
                  return [require("autoprefixer")];
                },
              },
            },
          },
          {
            loader: "sass-loader",
          },
        ],
      },
      {
        test: /\.(css)$/,
        use: [
          {
            loader: isProduction ? MiniCssExtractPlugin.loader : "style-loader",
          },
          {
            loader: "css-loader",
          },
          {
            loader: "postcss-loader",
            options: {
              postcssOptions: {
                plugins: function () {
                  return [require("autoprefixer")];
                },
              },
            },
          },
        ],
      },
    ],
  },

  devServer: {
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, PATCH, OPTIONS",
      "Access-Control-Allow-Headers":
        "X-Requested-With, content-type, Authorization",
    },
  },

  plugins: [
    new BundleTracker({
      path: __dirname,
      filename: "./dist/webpack-stats.json",
    }),
    ...(isProduction
      ? [
        new MiniCssExtractPlugin({
          filename: "[name]-[fullhash].css",
          chunkFilename: "[id].bundle.css",
        }),
      ]
      : []),
  ],

  optimization: {
    minimize: isProduction,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          compress: {
            drop_console: true,
          },
        },
      }),
      new CssMinimizerPlugin(),
    ],
    splitChunks: {
      chunks: 'all',
      cacheGroups: {
        vendor: {
          test: /[\\/]node_modules[\\/]/,
          name: 'vendors',
          chunks: 'all',
        },
      },
    },
  },

  output: {
    filename: "[name]-[fullhash].js",
    chunkFilename: "[id].bundle.js",
    path: path.resolve(__dirname, "dist"),
    publicPath: "/static/",
    pathinfo: false,
  },
};
