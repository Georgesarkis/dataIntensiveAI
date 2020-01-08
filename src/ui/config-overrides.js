/**
*   @author @MartinStanchev
*/

const path = require("path");
const { useBabelRc } = require("customize-cra");
const HtmlWebpackPlugin = require("html-webpack-plugin");

const entries = {
  index: "Index",
  admin: "Admin"
};



module.exports = function override(config, env) {
  config.entry = {
    index: "./src/index.js",
    admin: "./src/AdminIndex.js"
  };

  config.output.path = path.join(__dirname, "build");
    config.output.filename = "static/js/[name].js";
    config.output.chunkFilename = "static/js/[name].js";
    config.optimization.runtimeChunk = false;

    Object.keys(entries).forEach(id =>
      config.plugins.push(
        new HtmlWebpackPlugin({
          inject: "body",
          chunks: ["common", id],
          template: "!!html-webpack-plugin/lib/loader.js!./public/" + id + ".html",
          filename: `./${id}.html`,
          title: entries[id]
        })
      )
    );

  return useBabelRc()(config);
};
