<script setup>
import { MenuButton, MenuItem } from "@headlessui/vue";
import {
  BanIcon,
  BeakerIcon,
  CogIcon,
  LibraryIcon,
  MenuAlt4Icon,
  PresentationChartLineIcon,
  ShoppingBagIcon,
  TruckIcon,
  UserGroupIcon,
  UserIcon,
} from "@heroicons/vue/solid";
import { computed, ref } from "vue-demi";
import { RouterLink } from "vue-router";
import { useTempStore } from "../../stores/temp";
import UserProfile from "../profiles/profile-nav.vue";
import MyMenu from "./my-menu.vue";
import ToggleThemeBtn from "./toggle-theme-btn.vue";

const store = useTempStore();

const navTitle = computed(() => store.pageName);

const sidebarItem = ref([
  {
    label: "Tableau de bord",
    icon: "presentation",
    toRoute: "Dashboard",
  },
  {
    label: "Contacts",
    icon: "contact",
    toRoute: "Contacts",
  },
  {
    label: "Employé",
    icon: "user",
    toRoute: "Employee",
  },
  {
    label: "Entrées - Sorties",
    icon: "truck",
    toRoute: "Operations",
  },
  {
    label: "Stock",
    icon: "library",
    toRoute: "Products",
  },
  {
    label: "Point de vente",
    icon: "pos",
    toRoute: "POS",
  },
  {
    label: "Paramètre",
    icon: "setting",
    toRoute: "Settings",
  },
  {
    label: "Ecran de test",
    icon: "test",
    toRoute: "TestScreen",
  },
]);
</script>

<template>
  <!-- Navbar -->
  <nav
    class="mb-6 flex w-full items-center p-4 shadow-md dark:shadow-kPrimaryColor print:hidden sm:flex-row sm:flex-nowrap sm:justify-start"
  >
    <div
      class="mx-auto flex w-full flex-wrap items-center justify-between px-4 md:flex-nowrap md:px-10"
    >
      <!-- Toggler -->
      <MyMenu
        menuItemsWidthClass="right-6 top-4"
        menuItemsColorClass="bg-kPrimaryColor divide-gray-100"
        class="w-56"
      >
        <template #menu_button>
          <MenuButton>
            <MenuAlt4Icon
              class="h-7 w-7 cursor-pointer rounded-full bg-slate-400 p-1 text-white hover:bg-slate-600 dark:text-kWhiteColor"
            />
          </MenuButton>
        </template>

        <template #menu_content>
          <MenuItem as="div">
            <RouterLink
              v-for="(side, idx) in sidebarItem"
              :key="idx"
              :to="{ name: side.toRoute }"
              class="flex flex-row items-center py-3 text-xs font-bold uppercase text-slate-400 duration-300 hover:translate-x-2"
            >
              <PresentationChartLineIcon
                v-if="side.icon == 'presentation'"
                :class="[
                  side.label == navTitle ? 'text-kWhiteColor' : 'font-medium',
                  'inline-block h-5 w-5',
                ]"
              />
              <UserGroupIcon
                v-else-if="side.icon == 'contact'"
                :class="[
                  side.label == navTitle ? 'text-kWhiteColor' : 'font-medium',
                  'inline-block h-5 w-5',
                ]"
              />
              <UserIcon
                v-else-if="side.icon == 'user'"
                :class="[
                  side.label == navTitle ? 'text-kWhiteColor' : 'font-medium',
                  'inline-block h-5 w-5',
                ]"
              />
              <TruckIcon
                v-else-if="side.icon == 'truck'"
                :class="[
                  side.label == navTitle ? 'text-kWhiteColor' : 'font-medium',
                  'inline-block h-5 w-5',
                ]"
              />
              <LibraryIcon
                v-else-if="side.icon == 'library'"
                :class="[
                  side.label == navTitle ? 'text-kWhiteColor' : 'font-medium',
                  'inline-block h-5 w-5',
                ]"
              />
              <ShoppingBagIcon
                v-else-if="side.icon == 'pos'"
                :class="[
                  side.label == navTitle ? 'text-kWhiteColor' : 'font-medium',
                  'inline-block h-5 w-5',
                ]"
              />
              <BeakerIcon
                v-else-if="side.icon == 'test'"
                :class="[
                  side.label == navTitle ? 'text-kWhiteColor' : 'font-medium',
                  'inline-block h-5 w-5',
                ]"
              />
              <CogIcon
                v-else-if="side.icon == 'setting'"
                :class="[
                  side.label == navTitle ? 'text-kWhiteColor' : 'font-medium',
                  'inline-block h-5 w-5',
                ]"
              />
              <BanIcon
                v-else
                :class="[
                  side.label == navTitle ? 'text-kWhiteColor' : 'font-medium',
                  'inline-block h-5 w-5',
                ]"
              />
              <span
                :class="[
                  side.label == navTitle
                    ? 'font-bold text-kWhiteColor'
                    : 'font-medium',
                  'ml-2',
                ]"
              >
                {{ side.label }}
              </span>
            </RouterLink>
          </MenuItem>
        </template>
      </MyMenu>

      <!-- Brand -->
      <a
        class="block truncate text-sm font-semibold uppercase"
        href="javascript:void(0)"
      >
        {{ navTitle }}
      </a>

      <div
        class="hidden list-none flex-row items-center gap-x-4 sm:flex sm:flex-row"
      >
        <i
          class="pi pi-bell p-text-secondary"
          style="font-size: 2rem"
          v-badge.danger
        ></i>

        <ToggleThemeBtn />
        <!-- User -->
        <UserProfile />
      </div>
    </div>
  </nav>
  <!-- End Navbar -->
</template>
