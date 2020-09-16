export default {
  head: {
    titleTemplate: 'Motion Viewer',
    htmlAttrs: {
      lang: 'en'
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    ]
  },
  buildModules: ['@nuxt/typescript-build'],
  modules: ['bootstrap-vue/nuxt'],
  serverMiddleware: ['~/api/motion.js']
}