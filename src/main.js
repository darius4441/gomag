import { createApp } from "vue-demi";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import "./assets/tailwind.css";
import axios from "axios";

import "@suadelabs/vue3-multiselect/dist/vue3-multiselect.css";
import VueToast from "vue-toast-notification";
import "vue-toast-notification/dist/theme-sugar.css";

axios.defaults.baseURL = "http://127.0.0.1:8000";

const app = createApp(App);

const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(VueToast, {
  position: "top-right",
});
app.mount("#app");
