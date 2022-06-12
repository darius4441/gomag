import { fr } from "@formkit/i18n";
import { generateClasses } from "@formkit/themes";
import { defaultConfig, plugin } from "@formkit/vue";
import "@suadelabs/vue3-multiselect/dist/vue3-multiselect.css";
import { MotionPlugin } from "@vueuse/motion";
import axios from "axios";
import { createPinia } from "pinia";
import "primeicons/primeicons.css";
import Avatar from "primevue/avatar";
import Button from "primevue/button";
import PrimeVue from "primevue/config";
import InputSwitch from "primevue/inputswitch";
import InputText from "primevue/inputtext";
import Menu from "primevue/menu";
import Menubar from "primevue/menubar";
import "primevue/resources/primevue.min.css";
import "primevue/resources/themes/tailwind-light/theme.css";
import ToastService from "primevue/toastservice";
import { createApp } from "vue-demi";
import { VueQueryPlugin } from "vue-query";
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
app.use(VueQueryPlugin);
app.use(MotionPlugin);
app.use(PrimeVue);
app.component("PrimeButton", Button);
app.component("PrimeInputText", InputText);
app.component(ToastService);
app.component("PrimeMenu", Menu);
app.component("PrimeInputSwitch", InputSwitch);
app.component("PrimeAvatar", Avatar);
app.component("PrimeMenubar", Menubar);
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
app.mount("#app");
