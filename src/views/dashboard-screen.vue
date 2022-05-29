<script setup>
import { ref, onMounted, computed } from "vue-demi";
import { useTempStore } from "../stores/temp";

import moment from "moment";
import axios from "axios";
import { ArrowSmLeftIcon, ArrowSmRightIcon } from "@heroicons/vue/solid";

import react from "@/assets/images/react.jpg";
import ChartsBarChart from "../components/charts/bar-chart.vue";
import QuickInfoCard from "../components/dashboard/quick-info-card.vue";
import AlertProductData from "../components/dashboard/alert-product-data.vue";
import BestArticlePerformanceCard from "../components/dashboard/best-article-performance-card.vue";

// access to store and router in composition mode
const pageStore = useTempStore();

const alertProducts = ref([]);
const totalDailySale = ref(0);
const totalDailyInvoice = ref("");
const totalStockValue = ref(0);
const totalSales = ref(0);
const chartLabel = ref([]);
const chartDataset = ref([]);

const currentPage = ref(1);

// display pagination button
const asPreviousPage = ref([false]);
const asNextPage = ref([false]);

const quickInfoData = ref([
  {
    untitled: "Vente jours",
    icon: "basket",
    iconColor: "text-orange-600",
    rate: 24,
    value: computed(() => currencyFormater(totalDailySale.value, "currency")),
  },
  {
    untitled: "Bon du jour",
    icon: "users",
    iconColor: "text-emerald-600",
    rate: 48,
    value: computed(() => totalDailyInvoice.value),
  },
  {
    untitled: "Valeur stock",
    icon: "pie",
    iconColor: "text-indigo-600",
    rate: -32,
    value: computed(() => currencyFormater(totalStockValue.value, "currency")),
  },
  {
    untitled: "Total vente",
    icon: "shop",
    iconColor: "text-red-600",
    rate: 12,
    value: computed(() => currencyFormater(totalSales.value, "currency")),
  },
]);

const chartData = ref({
  value: {
    labels: chartLabel.value,
    datasets: [
      {
        data: chartDataset.value,
        backgroundColor: [
          "#FF0000",
          "#FF7F00",
          "#FFFF00",
          "#00FF00",
          "#0000FF",
          "#4B0082",
          "#9400D3",
        ],
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        position: "top",
      },
      title: {
        display: true,
        text: "Chart.js Doughnut Chart",
      },
    },
  },
  styles: {
    width: 100 + "%",
    height: 100 + "%",
  },
});

async function getalertProducts() {
  asPreviousPage.value = false;
  asNextPage.value = false;

  await axios
    .get(`/api/v1/stock/alert_products/?page=${currentPage.value}`)
    .then((response) => {
      alertProducts.value = response.data.results;

      if (response.data.previous) {
        asPreviousPage.value = true;
      }

      if (response.data.next) {
        asNextPage.value = true;
      }
    })
    .catch((error) => {
      console.log(JSON.stringify(error));
    });
}

function goToPreviousPage() {
  currentPage.value -= 1;

  getalertProducts();
}

function goToNextPage() {
  currentPage.value += 1;

  getalertProducts();
}

const bestArticle = ref({
  article: "React Material Dashboard",
  photoUrl: react,
  soldQty: "218",
  soldCash: "480,000",
  designTool: [
    {
      label: "Quantité",
      value: "4520",
      icon: "bag",
    },
    {
      label: "Valeur",
      value: "40 000",
      icon: "cash",
    },
  ],
});

function currencyFormater(val, format) {
  let localData = "";

  format === "currency"
    ? (localData = new Intl.NumberFormat().format(Number(val)) + " F")
    : (localData = new Intl.NumberFormat().format(Number(val)));

  return localData;
}

async function getDashboardData() {
  let start_date = moment().subtract(6, "day").format("YYYY-MM-DD");
  let end_date = moment().format("YYYY-MM-DD");

  const weekDay = [
    { id: 0, value: "Dimanche" },
    { id: 1, value: "Lundi" },
    { id: 2, value: "Mardi" },
    { id: 3, value: "Mercredi" },
    { id: 4, value: "Jeudi" },
    { id: 5, value: "Vendredi" },
    { id: 6, value: "Samedi" },
  ];

  const response = await axios
    .get(`api/v1/power_filter/?start_date=${start_date}&end_date=${end_date}`)
    .then((res) => {
      return res.data;
    });

  totalDailyInvoice.value = response.daily_client;
  totalStockValue.value = response.stock_value.total;
  totalSales.value = response.total_sale.total;

  response.daily_performance.map((e) => {
    const d = new Date(e.date);

    chartLabel.value.push(weekDay[d.getUTCDay()].value);
    chartDataset.value.push(e.sub_total);
  });

  totalDailySale.value = chartDataset.value.slice(-1)[0];
}

onMounted(() => {
  pageStore.updatePageName("Tableau de bord");

  getalertProducts();
  getDashboardData();
});
</script>

<template>
  <div class="flex flex-row gap-x-4">
    <!-- left part, it take 5/6 part of screen -->
    <div class="flex w-2/3 flex-col gap-y-6 print:w-full">
      <!-- quick info -->
      <div class="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <QuickInfoCard
          v-for="(card, idx) in quickInfoData"
          :key="idx"
          :untitled="card.untitled"
          :icon="card.icon"
          :iconColor="card.iconColor"
          :rate="card.rate"
          :value="card.value"
        />
      </div>

      <!-- last 7 days chart -->
      <div class="h-56 w-full rounded-md border-2 border-slate-300">
        <ChartsBarChart :initialData="chartData" />
      </div>

      <!-- alert product table -->
      <div
        class="h-56 px-3 w-full overflow-auto rounded-md border-2 border-slate-300 print:h-auto"
      >
        <h3 class="mb-2 text-lg font-semibold">Articles en alerte</h3>
        <AlertProductData :initialData="alertProducts" />
        <div
          v-if="currentPage >= 1"
          class="flex flex-row items-center justify-end gap-x-4 p-3"
        >
          <button
            v-if="asPreviousPage"
            @click="goToPreviousPage"
            class="mb-1 rounded px-6 py-1 text-xs font-bold uppercase text-kPrimaryColor shadow outline-none ring-1 ring-kPrimaryColor transition-all duration-150 ease-linear hover:shadow-md hover:ring-2 focus:outline-none dark:text-kWhiteColor dark:ring-kWhiteColor sm:mr-2"
          >
            <ArrowSmLeftIcon class="h-5 w-5" />
          </button>

          <button
            v-if="asNextPage"
            @click="goToNextPage"
            class="mb-1 rounded px-6 py-1 text-xs font-bold uppercase text-kPrimaryColor shadow outline-none ring-1 ring-kPrimaryColor transition-all duration-150 ease-linear hover:shadow-md hover:ring-2 focus:outline-none dark:text-kWhiteColor dark:ring-kWhiteColor sm:mr-2"
          >
            <ArrowSmRightIcon class="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>

    <!-- right part, it take 5/6 part of screen -->
    <div
      class="rounded-md border-2 border-slate-300 px-6 py-4 print:hidden sm:w-1/3"
    >
      <div class="">
        <img
          :src="bestArticle.photoUrl"
          alt="..."
          class="mx-auto h-24 w-24 rounded-full"
        />
        <h3 class="truncate text-center font-semibold">
          {{ bestArticle.article }}
        </h3>

        <div class="mt-2 rounded-md border-2 border-slate-300">
          <div class="grid grid-cols-2 gap-x-4">
            <BestArticlePerformanceCard
              v-for="(info, idx) in bestArticle.designTool"
              :key="idx"
              :initialData="info"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
