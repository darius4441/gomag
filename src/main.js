import { MotionPlugin } from "@vueuse/motion";
import axios from "axios";
import { createPinia } from "pinia";
import "primeicons/primeicons.css";
import AutoComplete from "primevue/autocomplete";
import Avatar from "primevue/avatar";
import Badge from "primevue/badge";
import BadgeDirective from "primevue/badgedirective";
import Breadcrumb from "primevue/breadcrumb";
import Button from "primevue/button";
import Calendar from "primevue/calendar";
import Card from "primevue/card";
import Column from "primevue/column";
import PrimeVue from "primevue/config";
import DataTable from "primevue/datatable";
import Dropdown from "primevue/dropdown";
import InputMask from "primevue/inputmask";
import InputNumber from "primevue/inputnumber";
import InputSwitch from "primevue/inputswitch";
import InputText from "primevue/inputtext";
import Menu from "primevue/menu";
import Menubar from "primevue/menubar";
import "primevue/resources/primevue.min.css";
import "primevue/resources/themes/tailwind-light/theme.css";
import Skeleton from "primevue/skeleton";
import Textarea from "primevue/textarea";
import Toast from "primevue/toast";
import ToastService from "primevue/toastservice";
import Toolbar from "primevue/toolbar";
import Tooltip from "primevue/tooltip";
import { createApp } from "vue-demi";
import { VueQueryPlugin } from "vue-query";
import App from "./App.vue";
import "./assets/tailwind.css";
import router from "./router";

axios.defaults.baseURL = "http://127.0.0.1:8000";

const app = createApp(App);

const pinia = createPinia();

app.use(pinia);
app.use(router);
app.use(VueQueryPlugin);
app.use(MotionPlugin);
app.use(PrimeVue, {
  locale: {
    startsWith: "Commence par",
    contains: "Contient",
    notContains: "Ne contient pas",
    endsWith: "Se termine par",
    equals: "Egal à",
    notEquals: "Different de",
    noFilter: "Aucun filtre",
    lt: "Plus petit que",
    lte: "Plus petit ou egal à",
    gt: "Plus grand que",
    gte: "Plus grand ou egal à",
    dateIs: "La date est",
    dateIsNot: "La date n'est pas",
    dateBefore: "Avant la date",
    dateAfter: "Après la date",
    clear: "Effacer",
    apply: "Appliquer",
    matchAll: "Toute correspondance",
    matchAny: "Aucune correspondance",
    addRule: "Ajouter un filtre",
    removeRule: "Supprimer un filtre",
    accept: "Oui",
    reject: "Non",
    choose: "Choisir",
    upload: "Importer",
    cancel: "Annuler",
    dayNames: [
      "Dimanche",
      "Lundi",
      "Mardi",
      "Mercredi",
      "Jeudi",
      "Vendredi",
      "Samedi",
    ],
    dayNamesShort: ["Dim", "Lun", "Mar", "Mer", "Jeu", "Ven", "Sam"],
    dayNamesMin: ["Di", "Lu", "Ma", "Me", "Je", "Ve", "Sa"],
    monthNames: [
      "Janvier",
      "Février",
      "Mars",
      "Avril",
      "Mai",
      "Juin",
      "Juillet",
      "Aout",
      "Septembre",
      "Octobre",
      "Novembre",
      "Décembre",
    ],
    monthNamesShort: [
      "Jan",
      "Fev",
      "Mar",
      "Avr",
      "Mai",
      "Jun",
      "Jul",
      "Aou",
      "Sep",
      "Oct",
      "Nov",
      "Déc",
    ],
    today: "Aujourd'hui",
    weekHeader: "Sm",
    firstDayOfWeek: 1,
    dateFormat: "mm/dd/yy",
    weak: "Petit",
    medium: "Moyen",
    strong: "Grand",
    passwordPrompt: "Entrer un mot de passe",
    emptyFilterMessage: "Pas de résultat",
    emptyMessage: "Pas d'option disponible",
  },
});
app.use(ToastService);
app.component("PrimeButton", Button);
app.component("PrimeInputText", InputText);
app.component("PrimeAutoComplete", AutoComplete);
app.component("PrimeInputNumber", InputNumber);
app.component("PrimeDropdown", Dropdown);
app.component("PrimeCard", Card);
app.component("PrimeTextarea", Textarea);
app.component("PrimeColumn", Column);
app.component("PrimeDataTable", DataTable);
app.component("PrimeSkeleton", Skeleton);
app.component("PrimeMenu", Menu);
app.component("PrimeCalendar", Calendar);
app.component("PrimeBreadcrumb", Breadcrumb);
app.component("PrimeToast", Toast);
app.component("PrimeToolbar", Toolbar);
app.component("PrimeBadge", Badge);
app.component("PrimeInputMask", InputMask);
app.component("PrimeInputSwitch", InputSwitch);
app.component("PrimeAvatar", Avatar);
app.component("PrimeMenubar", Menubar);

app.directive("badge", BadgeDirective);
app.directive("tooltip", Tooltip);
app.mount("#app");
