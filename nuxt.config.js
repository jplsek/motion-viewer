export default {
  head: {
    titleTemplate: '%s - Motion Viewer',
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
  bootstrapVue: {
    icons: true
  },
  serverMiddleware: ['~/api/motion.js']
}