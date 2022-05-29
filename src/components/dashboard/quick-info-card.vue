<script setup>
import {
  ShoppingBagIcon,
  ChartPieIcon,
  UserGroupIcon,
  ShoppingCartIcon,
} from "@heroicons/vue/solid";

const props = defineProps({
  untitled: { type: String, default: "" },
  icon: { type: String, default: "" },
  iconColor: { type: String, default: "" },
  rate: { type: Number, default: 0 },
  value: { type: [String, Number], default: "" },
});
</script>

<template>
  <div class="flex flex-col rounded-md border-2 border-slate-300 p-3">
    <div class="flex flex-row items-center justify-between">
      <ShoppingBagIcon
        v-if="icon == 'basket'"
        class="h-5 w-5"
        :class="iconColor"
      />
      <ChartPieIcon
        v-else-if="icon == 'pie'"
        class="h-5 w-5"
        :class="iconColor"
      />
      <UserGroupIcon
        v-else-if="icon == 'users'"
        class="h-5 w-5"
        :class="iconColor"
      />
      <ShoppingCartIcon v-else class="h-5 w-5" :class="iconColor" />
      <div
        :class="[
          props.rate >= 0 ? 'text-emerald-600' : 'text-red-600',
          ' font-semibold',
        ]"
      >
        {{ props.rate >= 0 ? `+ ${props.rate}` : props.rate }}
      </div>
    </div>
    <h3 class="my-1 font-semibold">{{ props.value }}</h3>
    <h3 class="text-md truncate">{{ props.untitled }}</h3>
  </div>
</template>
