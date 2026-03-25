const { defineConfig } = require('@vue/cli-service')

const proxyTarget = process.env.VUE_APP_PROXY_TARGET || 'http://localhost:8000'

module.exports = defineConfig({
  devServer: {
    proxy: {
      '/api': {
        target: proxyTarget,
        changeOrigin: true
      }
    }
  },
  transpileDependencies: [
    'vuetify'
  ],
  chainWebpack: config => {
    config.plugin('define').tap(definitions => {
      Object.assign(definitions[0]['process.env'], {
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(false)
      })
      return definitions
    })
  }
})
