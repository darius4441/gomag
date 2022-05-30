<script setup>
import photoUrl from "@/assets/images/default/profile_pic.png";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import { LogoutIcon, UserCircleIcon } from "@heroicons/vue/solid";
import axios from "axios";
import { RouterLink, useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";

// access to store and router in composition mode
const storeAuth = useAuthStore();
const router = useRouter();

// logout function
function logout() {
  axios
    .post("/api/v1/token/logout/")
    .then(() => {
      axios.defaults.headers.common["Authorization"] = "";

      localStorage.removeItem("userid");
      localStorage.removeItem("username");
      localStorage.removeItem("email");
      localStorage.removeItem("firstName");
      localStorage.removeItem("lastName");
      localStorage.removeItem("phoneNumber");
      localStorage.removeItem("token");

      storeAuth.removeToken;

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
}
</script>

<template>
  <Menu as="div" class="relative inline-block text-left">
    <MenuButton>
      <div class="flex items-center">
        <span
          class="inline-flex h-12 w-12 items-center justify-center rounded-full"
        >
          <img
            alt="..."
            class="w-full rounded-full border-none align-middle shadow-lg"
            :src="photoUrl"
          />
        </span>
      </div>
    </MenuButton>

    <transition
      enter-active-class="transition duration-100 ease-out"
      enter-from-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100"
      leave-active-class="transition duration-75 ease-in"
      leave-from-class="transform scale-100 opacity-100"
      leave-to-class="transform scale-95 opacity-0"
    >
      <MenuItems
        class="absolute right-0 z-50 mt-2 w-56 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
      >
        <div class="px-1 py-1">
          <MenuItem v-slot="{ active }">
            <RouterLink
              :to="{ name: 'Profile' }"
              @click="updateNavigationTitle('Profil')"
              :class="[
                active
                  ? ' bg-kPrimaryColor  text-kWhiteColor'
                  : ' text-kDarkColor',
                'group flex w-full items-center rounded-md px-2 py-2 text-sm',
              ]"
            >
              <UserCircleIcon class="mr-2 h-5 w-5" />
              <span>Profil</span>
            </RouterLink>
          </MenuItem>
        </div>

        <div class="px-1 py-1">
          <MenuItem v-slot="{ active }">
            <button
              @click="logout"
              :class="[
                active
                  ? 'bg-red-600  font-bold text-kWhiteColor'
                  : 'text-red-600',
                'group flex w-full items-center rounded-md px-2 py-2 text-sm',
              ]"
            >
              <LogoutIcon class="mr-2 h-5 w-5" />
              <span>Se déconnecter</span>
            </button>
          </MenuItem>
        </div>
      </MenuItems>
    </transition>
  </Menu>
</template>
