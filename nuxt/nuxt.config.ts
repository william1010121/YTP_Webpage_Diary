// nuxt.config.js
export default defineNuxtConfig({
  // ... existing configurations
  devtools: { enabled: true },

  css: [
    'vuetify/styles', // Import Vuetify styles
  ],

  plugins: [
    '~/plugins/axios.js',
    '~/plugins/vuetify.js', // Register Vuetify plugin
  ],

  vite: {
    define: {
      'process.env.DEBUG': false,
    },
    ssr: {
      noExternal: ['vuetify'],
    },
  },

  compatibilityDate: '2024-10-30',
})