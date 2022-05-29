<script setup>
import { ShoppingBagIcon, CashIcon } from "@heroicons/vue/solid";

const props = defineProps({
  initialData: Object,
});

const label = props.initialData.label;
const value = props.initialData.value;
const icon = props.initialData.icon;
</script>

<template>
  <div class="px-4 py-2">
    <div class="flex w-full flex-row items-center justify-between">
      <ShoppingBagIcon v-if="icon == 'bag'" class="h-5 w-5" />
      <CashIcon v-else class="h-5 w-5" />
      <div>
        <h3 class="truncate text-left text-sm font-semibold">
          {{ value }}
        </h3>
        <p class="truncate text-left text-sm">{{ label }}</p>
      </div>
    </div>
  </div>
</template>
