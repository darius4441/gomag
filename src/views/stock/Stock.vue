<template>
  <div class="flex flex-col">
    <!-- sub-navigation start -->
    <div class="mb-6 flex flex-row items-center justify-between">
      <div class="flex flex-row gap-x-3">
        <!-- <RouterLink
          :to="{ name: 'Stock' }"
          class="bg-kBgColor rounded-xl px-3 py-1 text-white"
        >
          Retour
        </RouterLink> -->
      </div>
      <div>
        <RouterLink
          :to="{ name: 'Products' }"
          class="text-kBgColor rounded-xl px-3 py-1 italic underline"
        >
          Voir les produits
        </RouterLink>
        <RouterLink
          :to="{ name: 'Inventory' }"
          class="text-kBgColor rounded-xl px-3 py-1 italic underline"
        >
          Inventaire
        </RouterLink>
      </div>
    </div>
    <!-- sub-navigation end -->
  </div>
</template>
<script>
import { RouterLink } from "vue-router";
export default {
  name: "stock-home",
  components: { RouterLink },

  setup() {},
};
</script>
