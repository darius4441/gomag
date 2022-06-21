<script setup>
import axios from "axios";
import { computed, ref } from "vue-demi";
import { RouterView } from "vue-router";
import Navigation from "./components/shared/nav-bar.vue";
import { useOperations, useProducts } from "./composables";
import { useAuthStore } from "./stores/auth";

// access to store and router in composition mode
const storeAuth = useAuthStore();

storeAuth.initializeStore;

// consts - vars declaration
const token = storeAuth.token;
const prodLoad = ref(false);
const opsLoad = ref(false);

if (token) {
  axios.defaults.headers.common["Authorization"] = "Token " + token;
  // execute some functions when authentication passed
  const { isLoading: productLoading } = useProducts();
  const { isLoading: operationLoading } = useOperations();

  prodLoad.value = computed(() => productLoading.value);
  opsLoad.value = computed(() => operationLoading.value);
} else {
  axios.defaults.headers.common["Authorization"] = "";
}
</script>

<template>
  <div
    class="min-h-screen bg-kWhiteColor text-kPrimaryColor dark:bg-kDarkColor dark:text-kWhiteColor"
  >
    <div>
      <Navigation v-if="storeAuth.isAuthenticated" />

      <div
        :class="[
          storeAuth.isAuthenticated ? 'px-4 md:px-10' : '',
          'mx-auto w-full',
        ]"
      >
        <RouterView />
      </div>
    </div>
  </div>
</template>

<style>
.p-card {
  --tw-bg-opacity: 1;
  background-color: rgb(255 253 250 / var(--tw-bg-opacity));

  color: rgb(3 65 89 / var(--tw-text-opacity));
}
</style>
