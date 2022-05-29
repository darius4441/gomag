<script setup>
import { ref, onMounted, computed } from "vue-demi";
import { useTempStore } from "../../stores/temp";
import { SearchIcon } from "@heroicons/vue/outline";
import axios from "axios";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";

import MyButton from "../../components/shared/my-action.vue";

import articlePhoto from "@/assets/images/article-default-img.png";

// ? Define composables
const pageStore = useTempStore();

// ? Define vars - consts
const products = ref([]);
const search = ref("");
const order_test = ref([
  {
    id: 272,
    name: "ABATTANT SIPPEC",
    prod_type: "storable",
    category: "Sanitaire",
    code: null,
    description: null,
    providers: null,
    uom: "pcs",
    slug: "abattant-sippec",
    getReplenish: 20,
    alert_stock: 40,
    optimal_stock: 200,
    real_quantity: 180,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 1,
    created_at: "2022-05-13T12:27:47.861614Z",
    created_by: 1,
    modified_at: "2022-05-20T21:30:32.713217Z",
    modified_by: 1,
    getUom: "pcs",
  },
  {
    id: 236,
    name: "AMPOULE 3W E27 QUALITEC",
    prod_type: "storable",
    category: "Electricité",
    code: null,
    description: null,
    providers: "QUALITEC",
    uom: "pqt",
    slug: "ampoule-3w-e27-qualitec",
    getReplenish: 0,
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 8,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 1,
    created_at: "2022-05-11T18:29:31.850414Z",
    created_by: 1,
    modified_at: "2022-05-20T21:30:32.888605Z",
    modified_by: 1,
    getUom: "pqt",
  },
  {
    id: 435,
    name: "AMPOULE 6W",
    prod_type: "storable",
    category: "Electricité",
    code: null,
    description: null,
    providers: null,
    uom: "pcs",
    slug: "ampoule-6w",
    getReplenish: 0,
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 0,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 1,
    created_at: "2022-05-24T09:22:53.097112Z",
    created_by: 1,
    modified_at: "2022-05-25T18:01:05.306864Z",
    modified_by: 1,
    getUom: "pcs",
  },
  {
    id: 501,
    name: "AMPOULE 9W B22 INGELEC",
    prod_type: "storable",
    category: "Electricité",
    code: null,
    description: null,
    providers: "INGELEC",
    uom: "pcs",
    slug: "ampoule-9w-b22-ingelec",
    getReplenish: 0,
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 0,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 1,
    created_at: "2022-05-25T11:36:07.533196Z",
    created_by: 1,
    modified_at: "2022-05-25T17:26:05.218467Z",
    modified_by: 1,
    getUom: "pcs",
  },
  {
    id: 150,
    name: "AMPOULE 9W E27 INGELEC",
    prod_type: "storable",
    category: "Electricité",
    code: null,
    description: null,
    providers: null,
    uom: "pcs",
    slug: "ampoule-9w-e27-ingelec",
    getReplenish: 0,
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 0,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 1,
    created_at: "2022-05-09T17:25:00Z",
    created_by: 1,
    modified_at: "2022-05-20T21:30:33.429689Z",
    modified_by: 1,
    getUom: "pcs",
  },
  {
    id: 503,
    name: "AMPOULE LED 1.2m T8 QUALITEC",
    prod_type: "storable",
    category: "Electricité",
    code: null,
    description: null,
    providers: "QUALITEC",
    uom: "pcs",
    slug: "ampoule-led-12m-t8-qualitec",
    getReplenish: 0,
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 0,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 1,
    created_at: "2022-05-25T17:27:29.930955Z",
    created_by: 1,
    modified_at: "2022-05-25T17:27:30.026594Z",
    modified_by: 1,
    getUom: "pcs",
  },
  {
    id: 395,
    name: "ANTIROUILLE GRIS 4KG",
    prod_type: "storable",
    category: "Peinture",
    code: null,
    description: null,
    providers: "C2CI",
    uom: "pot",
    slug: "antirouille-gris-4kg",
    getReplenish: 0,
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 12,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 6250,
    created_at: "2022-05-20T10:09:01.336275Z",
    created_by: 1,
    modified_at: "2022-05-25T14:05:08.998013Z",
    modified_by: 1,
    getUom: "pot",
  },
  {
    id: 385,
    name: "ARRACHE CLOU COURT FHM 21-11",
    prod_type: "storable",
    category: "Divers",
    code: null,
    description: null,
    providers: null,
    uom: "colie",
    slug: "arrache-clou-court-fhm-21-11",
    getReplenish: 0,
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 2,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 30000,
    created_at: "2022-05-19T14:08:56.161981Z",
    created_by: 1,
    modified_at: "2022-05-20T21:30:32.115753Z",
    modified_by: 1,
    getUom: "colie",
  },
  {
    id: 387,
    name: "ARRACHE CLOU LONG FHM 21-13",
    prod_type: "storable",
    category: "Divers",
    code: null,
    description: null,
    providers: null,
    uom: "colie",
    slug: "arrache-clou-long-fhm-21-13",
    getReplenish: 0,
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 1,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 45000,
    created_at: "2022-05-19T14:09:24.553400Z",
    created_by: 1,
    modified_at: "2022-05-24T18:05:26.042099Z",
    modified_by: 1,
    getUom: "colie",
  },
  {
    id: 386,
    name: "ARRACHE CLOU MOYEN FHM 21-12",
    prod_type: "storable",
    category: "Divers",
    code: null,
    description: null,
    providers: null,
    uom: "colie",
    slug: "arrache-clou-moyen-fhm-21-12",
    getReplenish: 0,
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 1,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 39000,
    created_at: "2022-05-19T14:09:11.506162Z",
    created_by: 1,
    modified_at: "2022-05-24T18:05:26.129273Z",
    modified_by: 1,
    getUom: "colie",
  },
  {
    id: 233,
    name: "ATTACHE N°8 QUALITEC",
    prod_type: "storable",
    category: "Divers",
    code: "11084",
    description: null,
    providers: "QUALITEC",
    uom: "pcs",
    slug: "attache-n8-qualitec",
    getReplenish: 1500,
    alert_stock: 1000,
    optimal_stock: 2000,
    real_quantity: 500,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 1,
    created_at: "2022-05-11T18:29:31.837970Z",
    created_by: 1,
    modified_at: "2022-05-24T18:05:26.281132Z",
    modified_by: 1,
    getUom: "pcs",
  },
  {
    id: 234,
    name: "ATTACHE N°9 QUALITEC",
    prod_type: "storable",
    category: "Divers",
    code: "11085",
    description: null,
    providers: "QUALITEC",
    uom: "pcs",
    slug: "attache-n9-qualitec",
    getReplenish: 1600,
    alert_stock: 1000,
    optimal_stock: 2000,
    real_quantity: 400,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 1,
    created_at: "2022-05-11T18:29:31.842435Z",
    created_by: 1,
    modified_at: "2022-05-24T18:05:26.436611Z",
    modified_by: 1,
    getUom: "pcs",
  },
]);
const newItem = ref({
  article: "",
  quantity: 1,
  unit: "",
  unit_price: 0,
});
const rowTotal = computed(
  () => newItem.value.quantity * newItem.value.unit_price
);
const totalAmount = computed(() => {
  let tot = order_test.value.reduce((total, currentVal) => {
    return total + currentVal.real_quantity * currentVal.unit_cost;
  }, 0);
  console.log(tot);
  return tot;
});

// ? Declare functions
async function getProducts() {
  await axios
    .get(`api/v1/stock/pos/?${newItem.value}`)
    .then((response) => {
      products.value = response.data;
    })
    .catch((error) => {
      console.log(JSON.stringify(error));
    });
}

const getCorrectPhoto = (item) => {
  item;
  return articlePhoto;
};

onMounted(async () => {
  pageStore.updatePageName("Point de vente");

  await getProducts();
});
</script>

<template>
  <div class="flex flex-row p-4">
    <!-- add item area -->
    <div class="basis-3/4">
      <div class="m-4 flex flex-wrap gap-4">
        <button
          v-for="(item, idx) in products"
          :key="idx"
          class="w-32 cursor-pointer rounded bg-white shadow-lg duration-300 hover:-translate-y-2"
        >
          <div class="relative">
            <img :src="getCorrectPhoto(item)" alt="person" />
            <div
              class="absolute top-2 right-2 rounded bg-kPrimaryColor text-kWhiteColor"
            >
              <span class="px-2 text-sm">
                {{ Number(item.unit_price).toLocaleString() }} F</span
              >
            </div>
          </div>
          <div class="h-12 w-full overflow-y-hidden bg-white p-1 shadow-lg">
            <p class="text-left text-xs">{{ item.name }}</p>
          </div>
        </button>
      </div>

      <div
        class="my-4 flex flex-col items-center py-4 shadow shadow-indigo-400"
      >
        <div
          class="flex flex-row items-center justify-between rounded-lg bg-kPrimaryColor/50 py-2 px-4"
        >
          <div class="flex space-x-4">
            <div class="relative">
              <input
                type="text"
                v-model="newItem.article"
                placeholder="Article"
                class="w-72 bg-kWhiteColor text-slate-600 placeholder:text-slate-400"
              />
              <SearchIcon class="absolute right-4 top-2 h-5 w-5" />
            </div>

            <div>
              <input
                type="text"
                v-model="newItem.quantity"
                placeholder="Qté"
                class="w-16 bg-kWhiteColor text-right text-slate-600 placeholder:text-slate-400"
              />
            </div>

            <div>
              <input
                type="text"
                v-model="newItem.unit"
                placeholder="unité"
                class="w-20 bg-kWhiteColor text-center text-slate-600 placeholder:text-slate-400"
              />
            </div>

            <div>
              <input
                type="text"
                v-model="newItem.unit_price"
                placeholder="Prix"
                class="w-16 bg-kWhiteColor text-right text-slate-600 placeholder:text-slate-400"
              />
            </div>

            <div>
              <input
                type="text"
                v-model="rowTotal"
                placeholder="Total"
                disabled
                class="w-20 bg-kWhiteColor text-right text-slate-600 placeholder:text-slate-400"
              />
              <SearchIcon class="absolute right-4 top-2 h-5 w-5" />
            </div>
          </div>

          <MyButton label="Ajouter" />
        </div>

        <div
          class="flex w-3/5 rounded-b-lg bg-kPrimaryColor/50 pt-4 pb-2 shadow-inner shadow-indigo-300"
        >
          <div class="w-full">
            <div class="relative mx-auto w-1/2">
              <input
                type="text"
                v-model="search"
                @input="getProducts()"
                placeholder="Chercher ..."
                class="bg-kWhiteColor text-slate-600 placeholder:text-slate-400"
              />
              <SearchIcon class="absolute right-4 top-2 h-5 w-5" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- order area -->
    <div class="basis-1/4 bg-kPrimaryColor px-4 text-kWhiteColor">
      <p>Votre panier</p>

      <div v-if="order_test.length" class="w-full pt-5">
        <div class="h-[68vh] overflow-y-auto">
          <div
            v-for="(item, idx) in order_test"
            :key="idx"
            class="mx-auto mt-2 w-full rounded-lg bg-white"
          >
            <Disclosure>
              <DisclosureButton class="w-full text-xs">
                <div
                  class="rounded-md bg-kPrimaryColor/90 px-4 py-2 hover:bg-kPrimaryColor/75"
                >
                  <div class="flex justify-between">
                    <span class="truncate">{{ item.name }}</span>
                    <span
                      >{{ item.real_quantity }} x
                      {{ item.unit_cost.toLocaleString() }}F
                    </span>
                  </div>
                  <p class="text-right font-bold">
                    {{
                      (item.real_quantity * item.unit_cost).toLocaleString()
                    }}F
                  </p>
                </div>
              </DisclosureButton>
              <DisclosurePanel
                class="max-h-64 overflow-y-auto px-4 pt-4 pb-2 text-sm"
              >
                <div>Roch Arthur on the beat</div>
              </DisclosurePanel>
            </Disclosure>
          </div>
        </div>

        <div class="mt-6">
          <div class="flex justify-between">
            <span class="text-lg font-bold"
              >{{ totalAmount.toLocaleString() }}F
            </span>
          </div>

          <MyButton label="Paiement" :isOutlined="true" />
        </div>
      </div>

      <div v-else>
        <p>
          Votre panier est vide, ajouter des elements comme vous le voulez :)
        </p>
      </div>
    </div>
  </div>
</template>
