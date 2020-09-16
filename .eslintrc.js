module.exports = {
  env: {
    browser: true,
    es2021: true
  },
  extends: [
    '@nuxtjs/eslint-config-typescript',
    'plugin:vue/strongly-recommended',
    'standard',
  ],
  parserOptions: {
    ecmaVersion: 12,
    sourceType: 'module'
  },
  plugins: [
    'vue',
  ],
  rules: {
  }
}
