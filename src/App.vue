<script setup>
import axios from "axios";
import { RouterView } from "vue-router";
import Navigation from "./components/shared/nav-bar.vue";
import { useAuthStore } from "./stores/auth";

// access to store and router in composition mode
const storeAuth = useAuthStore();

storeAuth.initializeStore;

// consts - vars declaration
const token = storeAuth.token;

if (token) {
  // execute some functions when authentication passed
  axios.defaults.headers.common["Authorization"] = "Token " + token;
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
