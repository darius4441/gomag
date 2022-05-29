<script setup>
import { onMounted } from "vue-demi";
import { useTempStore } from "../stores/temp";

// init utils composables to variables
const pageStore = useTempStore();

onMounted(() => {
  pageStore.updatePageName("Paramètre");
});
</script>

<template>
  <div>
    <div class="text-2xl first-letter:text-7xl">
      Ecran de parametrage des données de l'entreprise
    </div>
  </div>
</template>
