<script setup>
import { onMounted } from "vue-demi";
import { useTempStore } from "../../stores/temp";

// init utils composables to variables
const pageStore = useTempStore();

onMounted(async () => {
  pageStore.updatePageName("Contacts");
});
</script>

<template>
  <div>
    <p>Dupliquer de contact</p>
  </div>
</template>
