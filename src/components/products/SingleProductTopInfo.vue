<script setup>
import {
  DatabaseIcon,
  RefreshIcon,
  SwitchHorizontalIcon,
} from "@heroicons/vue/solid";

const props = defineProps({
  label: String,
  icon: String,
  value: Number,
});
</script>

<template>
  <div
    @click="enableShowModal"
    class="h-full w-44 cursor-pointer border-l duration-500 ease-in-out hover:bg-kPrimaryColor hover:text-kWhiteColor"
  >
    <div class="flex flex-row items-center justify-between gap-x-3 p-2 text-sm">
      <div>
        <DatabaseIcon v-if="props.icon == 'stock'" class="h-5 w-5" />
        <RefreshIcon
          v-else-if="props.icon == 'replenishment'"
          class="h-5 w-5"
        />
        <SwitchHorizontalIcon v-else class="h-5 w-5" />
      </div>

      <div class="w-full">
        <p>
          {{ props.value }}
        </p>

        <p class="overflow-hidden truncate font-bold">
          {{ props.label }}
        </p>
      </div>
    </div>
  </div>
</template>
