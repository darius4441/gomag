<script setup>
import { ref, onMounted } from "vue-demi";
import { useRoute } from "vue-router";

import axios from "axios";

import MyButton from "../../components/shared/my-action.vue";
import SingleInventoryItemRow from "../../components/products/SingleInventoryItemRow.vue";

const route = useRoute();

const inventoryID = route.params.id;

onMounted(async () => {
  await getInventory();
});

const inventory = ref({});

// get single inventory
const getInventory = async () => {
  await axios
    .get(`/api/v1/stock/inventory/${inventoryID}`)
    .then((response) => {
      inventory.value = response.data;
    })
    .catch((error) => {
      console.log(JSON.stringify(error));
    });
};
</script>

<template>
  <div>
    <!-- Header -->
    <div class="flex w-full flex-row items-center">
      <MyButton label="Sauver" @click="onSubmit" />

      <MyButton label="Retour" to="Inventory" :isOutlined="true" />
    </div>

    <!-- card -->
    <div class="mt-4 flex flex-wrap">
      <div class="mb-12 w-full px-4">
        <div
          class="relative mb-6 flex w-full min-w-0 flex-col break-words rounded bg-white shadow-lg"
        >
          <div class="mb-0 rounded-t border-0 px-4 py-3">
            <div class="flex flex-wrap items-center">
              <div class="relative w-full max-w-full flex-1 flex-grow px-4">
                <h3 class="text-lg font-semibold text-slate-700">
                  {{ inventory.name }}
                </h3>
              </div>
            </div>
          </div>

          <div class="block w-full overflow-x-auto p-4">
            <!-- inventaory main info -->
            <div
              class="grid grid-flow-col grid-cols-2 gap-3 rounded-lg border-2 p-3"
            >
              <div>
                <span
                  class="mb-2 block text-sm font-medium text-gray-900 dark:text-gray-300"
                >
                  Nom
                </span>
                <div
                  class="block w-full rounded-lg border p-1 text-sm font-bold tracking-wide text-gray-900"
                >
                  {{ inventory.name }}
                </div>
              </div>
              <div>
                <span
                  class="mb-2 block text-sm font-medium text-gray-900 dark:text-gray-300"
                >
                  Date
                </span>
                <div
                  class="block w-full rounded-lg border p-1 text-sm font-bold tracking-wide text-gray-900"
                >
                  {{ inventory.date }}
                </div>
              </div>
            </div>

            <!-- inventory items info -->
            <div class="mt-3 gap-y-3 rounded-lg border-2 p-3">
              <div
                class="mb-2 grid grid-cols-7 gap-3 px-3 text-sm font-medium text-gray-900 dark:text-gray-300"
              >
                <p class="col-span-4 truncate text-left">Article</p>
                <p class="truncate text-right">Quantité compté</p>
                <p class="truncate text-center">Unité</p>
              </div>
              <div class="flex flex-col gap-y-3 rounded-lg bg-gray-50 py-3">
                <SingleInventoryItemRow
                  v-for="(item, idx) in inventory.items_inventory"
                  :key="idx"
                  :initialItem="item"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
