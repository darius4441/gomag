<script setup>
import { RouterLink } from "vue-router";
import { onMounted, ref } from "vue-demi";

import axios from "axios";

import MyButton from "../../components/shared/my-action.vue";

const inventoryData = ref([]);

// format date
const formatDate = (dateString) => {
  const date = new Date(dateString);
  // Then specify how you want your dates to be formatted
  return new Intl.DateTimeFormat("fr-FR", { dateStyle: "medium" }).format(date);
};

onMounted(
  async () =>
    await axios.get("api/v1/stock/inventory/").then((res) => {
      inventoryData.value = res.data;
    })
);
</script>

<template>
  <div>
    <!-- Header -->
    <div class="flex w-full flex-row items-center px-4">
      <MyButton label="Créer" to="CreateInventory" />
      <MyButton label="Retour" to="Products" :isOutlined="true" />
    </div>

    <div class="mt-4 flex flex-wrap">
      <div class="mb-12 w-full px-4">
        <div
          class="relative mb-6 flex w-full min-w-0 flex-col break-words rounded bg-white shadow-lg dark:bg-emerald-700 dark:text-white"
        >
          <div class="mb-0 rounded-t border-0 px-4 py-3">
            <div class="flex flex-wrap items-center">
              <div class="relative w-full max-w-full flex-1 flex-grow px-4">
                <h3
                  class="text-lg font-semibold text-slate-700 dark:text-white"
                >
                  Liste des inventaires
                </h3>
              </div>
            </div>
          </div>
          <div class="block max-h-[65vh] w-full overflow-x-auto p-4">
            <div class="grid grid-cols-4 gap-3">
              <RouterLink
                v-for="(inventory, index) in inventoryData"
                :key="index"
                :to="{ name: 'SingleInv', params: { id: inventory.id } }"
                class="cursor-pointer space-y-6 rounded-lg bg-kPrimaryColor px-2 py-3 text-white duration-300 ease-in-out hover:scale-110"
              >
                <h1 class="text-center font-semibold">
                  Inv. {{ inventory.name }}
                </h1>

                <p class="text-center text-sm">
                  {{ formatDate(inventory.date) }}
                </p>
                <!-- <p class="text-center text-xs">
          <span>318</span>
          produits inventorié
        </p> -->
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
