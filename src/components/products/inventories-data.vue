<script setup>
import { ref } from "vue-demi";
const inventoryData = ref([
  {
    label: "Tuyauterie",
    date: "24 September 2022 15:30 UTC",
  },
  {
    label: "Plomberie",
    date: "24 September 2022 15:30 UTC",
  },
  {
    label: "Electricité",
    date: "24 September 2022 15:30 UTC",
  },
  {
    label: "Divers",
    date: "24 September 2022 15:30 UTC",
  },
]);

// format date
const formatDate = (dateString) => {
  const date = new Date(dateString);
  // Then specify how you want your dates to be formatted
  return new Intl.DateTimeFormat("fr-FR", { dateStyle: "medium" }).format(date);
};
</script>

<template>
  <div>
    <div class="grid grid-cols-4 gap-4 pt-1 pb-4">
      <NuxtLink
        v-for="(inventory, index) in inventoryData"
        :key="index"
        to="/"
        class="cursor-pointer space-y-4 rounded-lg bg-emerald-500 px-2 py-4 text-white duration-300 ease-in-out hover:scale-110"
      >
        <h1 class="text-center font-semibold">Inv. {{ inventory.label }}</h1>

        <p class="text-center text-sm">{{ formatDate(inventory.date) }}</p>
        <!-- <p class="text-center text-xs">
          <span>318</span>
          produits inventorié
        </p> -->
      </NuxtLink>
    </div>
  </div>
</template>
