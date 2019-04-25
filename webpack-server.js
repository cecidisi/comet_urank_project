var webpack = require('webpack')
var WebpackDevServer = require('webpack-dev-server')
var config = require('./webpack.config.devel')
var port = 8088

new WebpackDevServer(webpack(config), {
  publicPath: config.output.publicPath,
  hot: true,
  inline: true,
  historyApiFallback: true,
  headers: {
	'Access-Control-Allow-Origin': '*'
  }
}).listen(port, '0.0.0.0', function (err, result) {
  if (err) {
    console.log(err)
  }

  console.log('Listening at 0.0.0.0:', port)
})