<script setup>
import { useDark, useToggle } from "@vueuse/core";
import { SunIcon, MoonIcon } from "@heroicons/vue/solid";

const isDark = useDark();
const toggleDark = useToggle(isDark);
</script>

<template>
  <button
    @click="toggleDark()"
    class="rounded-lg p-2.5 text-sm duration-300 ease-in-out hover:text-kPrimaryColor dark:hover:text-kPrimaryColor"
  >
    <MoonIcon v-if="isDark" class="h-5 w-5" />
    <SunIcon v-else class="h-5 w-5" />
  </button>
</template>
