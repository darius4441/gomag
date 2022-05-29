<script setup>
import { ref, computed } from "vue-demi";
import { RouterLink } from "vue-router";
import { useTempStore } from "../../stores/temp";
import {
  MenuAlt4Icon,
  PresentationChartLineIcon,
  TruckIcon,
  LibraryIcon,
  BeakerIcon,
  BanIcon,
  BellIcon,
  CogIcon,
  XIcon,
} from "@heroicons/vue/solid";

import UserProfile from "../profiles/profile-nav.vue";
import ToggleThemeBtn from "./toggle-theme-btn.vue";

const store = useTempStore();

const navTitle = computed(() => store.pageName);

const collapseShow = ref("hidden");
const toggleCollapseShow = (classes) => (collapseShow.value = classes);

const sidebarItem = ref([
  {
    label: "Tableau de bord",
    icon: "presentation",
    toRoute: "Dashboard",
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
  <nav
    class="sm:w-54 relative z-10 flex flex-wrap items-center justify-between py-4 px-6 shadow-xl dark:bg-kDarkColor md:fixed md:left-0 md:top-0 md:bottom-0 md:block md:flex-row md:flex-nowrap md:overflow-hidden md:overflow-y-auto lg:w-64"
  >
    <div
      class="mx-auto flex w-full flex-wrap items-center justify-between px-0 md:min-h-full md:flex-col md:flex-nowrap md:items-stretch"
    >
      <!-- Toggler -->
      <button
        class="cursor-pointer rounded border border-solid border-transparent bg-transparent px-3 py-1 text-xl leading-none text-black opacity-50 md:hidden"
        type="button"
        v-on:click="toggleCollapseShow('bg-kWhiteColor m-2 py-3 px-6')"
      >
        <MenuAlt4Icon class="h-6 w-6 dark:text-kWhiteColor" />
      </button>
      <!-- Brand -->
      <RouterLink
        to="/"
        @click="toggleCollapseShow('hidden')"
        class="mr-0 inline-block whitespace-nowrap p-4 px-0 text-left text-sm font-bold uppercase dark:text-kWhiteColor md:block md:pb-2"
      >
        Gomag | DIM-AD
      </RouterLink>
      <!-- User -->
      <ul class="flex list-none flex-wrap items-center md:hidden">
        <li class="relative inline-block">
          <BellIcon class="h-5 w-5 dark:to-kWhiteColor" />
        </li>
        <li class="relative inline-block">
          <ToggleThemeBtn />
        </li>
        <li class="relative inline-block">
          <UserProfile />
        </li>
      </ul>
      <!-- Collapse -->
      <div
        class="absolute top-0 left-0 right-0 z-40 h-auto flex-1 items-center overflow-y-auto overflow-x-hidden rounded shadow md:relative md:mt-4 md:flex md:flex-col md:items-stretch md:opacity-100 md:shadow-none"
        v-bind:class="collapseShow"
      >
        <!-- Collapse header -->
        <div
          class="mb-4 block border-b border-solid border-slate-200 pb-4 md:hidden md:min-w-full"
        >
          <div class="flex flex-wrap items-center">
            <div class="w-6/12">
              <RouterLink
                to="/"
                class="mr-0 inline-block whitespace-nowrap p-4 px-0 text-left text-sm font-bold uppercase text-slate-600 dark:text-kWhiteColor md:block md:pb-2"
              >
                Gomag | DIM-AD
              </RouterLink>
            </div>
            <div class="flex w-6/12 justify-end">
              <XIcon
                @click="toggleCollapseShow('hidden')"
                class="h-5 w-5 cursor-pointer rounded-full bg-slate-400 p-1 text-white hover:bg-slate-600"
              />
              <!-- class="h-5 w-5 cursor-pointer rounded border border-solid px-3 py-1 text-xl leading-none text-black md:hidden" -->
            </div>
          </div>
        </div>
        <!-- Form -->
        <form class="mt-6 mb-4 md:hidden">
          <div class="mb-3 pt-0">
            <input
              type="text"
              placeholder="Search"
              class="relative w-full rounded border-0 bg-kWhiteColor px-3 py-2 pl-10 text-sm placeholder-slate-400 shadow outline-none focus:outline-none focus:ring dark:bg-kWhiteColor/90 dark:text-kPrimaryColor dark:placeholder-kPrimaryColor/70"
            />
          </div>
        </form>

        <!-- Divider -->
        <hr class="my-4 md:min-w-full" />

        <!-- Navigation -->
        <div class="flex flex-col md:min-w-full md:flex-col">
          <RouterLink
            v-for="(side, idx) in sidebarItem"
            :key="idx"
            :to="{ name: side.toRoute }"
            @click="toggleCollapseShow('hidden')"
            class="flex flex-row items-center py-3 text-xs font-bold uppercase hover:text-slate-500 active:text-emerald-500 active:hover:text-emerald-600"
          >
            <PresentationChartLineIcon
              v-if="side.icon == 'presentation'"
              :class="[
                side.label == navTitle
                  ? ' text-kPrimaryColor dark:text-kWhiteColor'
                  : 'font-medium',
                'inline-block h-5 w-5 ',
              ]"
            />
            <TruckIcon
              v-else-if="side.icon == 'truck'"
              :class="[
                side.label == navTitle
                  ? ' text-kPrimaryColor dark:text-kWhiteColor'
                  : 'font-medium',
                'inline-block h-5 w-5',
              ]"
            />
            <LibraryIcon
              v-else-if="side.icon == 'library'"
              :class="[
                side.label == navTitle
                  ? ' text-kPrimaryColor dark:text-kWhiteColor'
                  : 'font-medium',
                'inline-block h-5 w-5 ',
              ]"
            />
            <BeakerIcon
              v-else-if="side.icon == 'test'"
              :class="[
                side.label == navTitle
                  ? ' text-kPrimaryColor dark:text-kWhiteColor'
                  : 'font-medium',
                'inline-block h-5 w-5 ',
              ]"
            />
            <CogIcon
              v-else-if="side.icon == 'setting'"
              :class="[
                side.label == navTitle
                  ? ' text-kPrimaryColor dark:text-kWhiteColor'
                  : 'font-medium',
                'inline-block h-5 w-5 ',
              ]"
            />
            <BanIcon
              v-else
              :class="[
                side.label == navTitle
                  ? ' text-kPrimaryColor dark:text-kWhiteColor'
                  : 'font-medium',
                'inline-block h-5 w-5',
              ]"
            />
            <span
              :class="[
                side.label == navTitle
                  ? 'font-bold text-kPrimaryColor dark:text-kWhiteColor'
                  : 'font-medium',
                'ml-2',
              ]"
            >
              {{ side.label }}
            </span>
          </RouterLink>
        </div>
      </div>
    </div>
  </nav>
</template>
