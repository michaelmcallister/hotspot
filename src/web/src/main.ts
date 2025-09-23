import { createApp } from 'vue'
import App from '../src/App.vue'
import './assets/styles.css'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import router from './router'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'hotspot',
    themes: {
      hotspot: {
        dark: false,
        colors: {
          primary: '#07a377',
          secondary: '#0b1541',
          success: '#10b981',
          error: '#ef4444',
          warning: '#f59e0b',
          info: '#3b82f6',
          surface: '#ffffff',
        },
      },
    },
  },
})

createApp(App)
  .use(vuetify)
  .use(router)
  .mount('#app')
