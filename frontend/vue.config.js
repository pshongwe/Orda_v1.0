const { defineConfig } = require('@vue/cli-service');
const webpack = require('webpack');

module.exports = defineConfig({
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        'process.env.VUE_APP_ORDERS_API': JSON.stringify(
          process.env.ENV === 'prod' || process.env.ENV === 'dev'
            ? `https://orda-v10-backend-${process.env.ENV}.onrender.com/api/v1/orders`
            : 'http://localhost:5000/api/v1/orders'
        )
      })
    ]
  },
  devServer: {
    client: {
      progress: true,
    },
    port: 8080,   // Set the port to 8080
    https: true, // Enable HTTPS
    host: 'localhost',
    headers: {
      // Additional headers configuration
      'Access-Control-Allow-Origin': '*', // Allow all origins (CORS)
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
      'Access-Control-Allow-Headers': 'X-Requested-With, content-type, Authorization'
    }
  },
  transpileDependencies: true
});