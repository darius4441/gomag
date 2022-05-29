<script setup>
import { onMounted, ref, computed } from "vue-demi";
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";

import axios from "axios";

// access to store and router in composition mode
const router = useRouter();
const store = useAuthStore();

const onCreation = ref(false);

const user = computed(() => {
  return store.user;
});

onMounted(() => {
  onCreation.value = false;
});

const updateOrganisation = () => {};

const logout = () => {
  axios
    .post("/api/v1/token/logout/")
    .then((res) => {
      res;
      axios.defaults.headers.common["Authorization"] = "";

      localStorage.clear();

      store.commit("removeToken");

      router.push({ name: "Login" });
    })
    .catch((error) => {
      if (error.response) {
        console.log(JSON.stringify(error.response.data));
      } else if (error.message) {
        console.log(JSON.stringify(error.message));
      } else {
        console.log(JSON.stringify(error));
      }
    });
};
</script>

<template>
  <div>
    <div v-if="!onCreation" class="table">
      <div>
        Nom:
        <strong>{{ user.firstName }}</strong>
      </div>

      <div>
        Prénom:
        <strong>{{ user.lastName }}</strong>
      </div>

      <div>
        Contact:
        <strong>{{ user.phoneNumber }}</strong>
      </div>

      <div>
        Email:
        <strong>{{ user.email }}</strong>
      </div>

      <div>
        Identifiant:
        <strong>{{ user.username }}</strong>
      </div>
    </div>
    <div v-else>
      <form>
        <!-- name field -->
        <div class="mt-4">
          <div>
            <label for="name" class="block">insert v-model on input</label>
            <input
              type="text"
              id="name"
              placeholder="insert v-model on input"
              class="mt-2 w-full rounded-md border px-4 py-2 focus:outline-none focus:ring-1 focus:ring-blue-600"
            />
            <span class="text-xs tracking-wide text-red-600">
              Ce champ est requis
            </span>
          </div>
        </div>
      </form>
    </div>

    <button
      @click="logout"
      class="my-2 mr-2 rounded-lg border border-gray-200 bg-red-500 py-2 px-4 text-sm font-bold uppercase text-white hover:border-red-500 hover:bg-gray-100 hover:text-red-700 focus:z-10 focus:text-red-500 focus:ring-2 focus:ring-red-500"
    >
      Se deconnecter
    </button>
    <button
      v-if="!onCreation"
      @click="onCreation = !onCreation"
      class="my-2 mr-2 rounded-lg border border-gray-200 bg-green-500 py-2 px-4 text-sm font-bold uppercase text-white hover:border-red-500 hover:bg-gray-100 hover:text-red-700 focus:z-10 focus:text-red-500 focus:ring-2 focus:ring-red-500"
    >
      Modifier
    </button>
    <button
      v-else
      @click="updateOrganisation"
      class="my-2 mr-2 rounded-lg border border-gray-200 bg-green-500 py-2 px-4 text-sm font-bold uppercase text-white hover:border-red-500 hover:bg-gray-100 hover:text-red-700 focus:z-10 focus:text-red-500 focus:ring-2 focus:ring-red-500"
    >
      Mettre à jour
    </button>
  </div>
</template>
