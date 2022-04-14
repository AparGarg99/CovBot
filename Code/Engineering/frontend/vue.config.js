// vue.config.js

/**
 * @type {import('@vue/cli-service').ProjectOptions}
 * @argument {https://cli.vuejs.org/zh/config/#vue-config-js}
 */
 module.exports = {
    // options...
    publicPath: './',
    devServer: {

      host: '0.0.0.0',
      https: false,
      /* use agent */
      proxy: {
          '/api': {
              /* target agent address */
              target: 'http://127.0.0.1:5000/',
              /* allow cross origin */
              changeOrigin: true,
          },
      }
    }
  }