import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import colors from 'vuetify/util/colors'

export default createVuetify({
  theme: {
    themes: {
      light: {
        primary: colors.red.darken1, // #E53935
        secondary: colors.red.lighten4, // #
        // define other colors hereFFCDD2
      },
      dark: {
        primary: colors.red.darken1,
        secondary: colors.red.lighten4,
        // define other colors here for dark theme if needed
      },
    },
  },
});