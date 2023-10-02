const { defineConfig } = require('@vue/cli-service')

module.exports = {
  devServer: {
    open: process.platform === 'darwin',
    host: '0.0.0.0',
    port: 8880, // CHANGE YOUR PORT HERE!
    https: true,
  },
}