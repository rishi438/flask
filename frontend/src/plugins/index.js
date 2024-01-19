/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

// Plugins
import vuetify from "./vuetify";
import router from "../router";
import "../assets/fonts/Roboto-Regular.ttf";
import "../assets/fonts/Roboto-Bold.ttf";
import "../assets/fonts/Roboto-Italic.ttf";
export function registerPlugins(app) {
  app.use(vuetify).use(router);
}
