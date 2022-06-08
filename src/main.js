import { fr } from "@formkit/i18n";
import { generateClasses } from "@formkit/themes";
import { defaultConfig, plugin } from "@formkit/vue";
import "@suadelabs/vue3-multiselect/dist/vue3-multiselect.css";
import { MotionPlugin } from "@vueuse/motion";
import axios from "axios";
import { createPinia } from "pinia";
import { createApp } from "vue-demi";
import VueToast from "vue-toast-notification";
import "vue-toast-notification/dist/theme-sugar.css";
import App from "./App.vue";
import "./assets/tailwind.css";
import router from "./router";
import theme from "./utils/theme";

axios.defaults.baseURL = "http://127.0.0.1:8000";

const app = createApp(App);

const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(
  plugin,
  defaultConfig({
    locales: { fr },
    locale: "fr",
    config: {
      classes: generateClasses(theme),
    },
  })
);
app.use(VueToast, {
  position: "top-right",
});
app.use(MotionPlugin);
app.mount("#app");
