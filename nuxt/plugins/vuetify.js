// plugins/vuetify.js
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';

// Import Material Design Icons font (ensure @mdi/font is installed)
import '@mdi/font/css/materialdesignicons.css';

export default defineNuxtPlugin((nuxtApp) => {
    const vuetify = createVuetify({
        components,
        directives,
        // Configure icons to use the font-based MDI set
        icons: {
            defaultSet: 'mdi',
            iconfont: 'mdi', // Explicitly use font-based MDI
        },
        theme: {
            defaultTheme: 'light',
            themes: {
                light: {
                    colors: {
                        primary: '#1976D2',
                        secondary: '#424242',
                        accent: '#82B1FF',
                        error: '#FF5252',
                        info: '#2196F3',
                        success: '#4CAF50',
                        warning: '#FFC107',
                    },
                },
            },
        },
    });

    nuxtApp.vueApp.use(vuetify);
});
