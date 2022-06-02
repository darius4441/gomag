<script setup>
import { RouterLink } from "vue-router";
const props = defineProps({
  label: String,
  to: String,
  params: String,
  isOutlined: { type: Boolean, default: false },
});
</script>

<template>
  <template v-if="to">
    <RouterLink
      v-if="!params"
      :to="{ name: to }"
      type="button"
      :class="[
        props.isOutlined == true
          ? 'text-kPrimaryColor ring-1 ring-kPrimaryColor hover:ring-2 dark:text-kWhiteColor'
          : 'bg-kPrimaryColor text-white ring-1 ring-kPrimaryColor hover:bg-kSecondaryColor',
        'mb-1 rounded px-4 py-2 text-xs font-bold uppercase  shadow outline-none transition-all duration-150 ease-linear hover:shadow-md focus:outline-none  sm:mr-2',
      ]"
    >
      {{ props.label }}
    </RouterLink>

    <RouterLink
      v-else
      :to="{ name: to, params: { id: params } }"
      type="button"
      :class="[
        props.isOutlined == true
          ? 'text-kPrimaryColor ring-1 ring-kPrimaryColor hover:ring-2 dark:text-kWhiteColor'
          : 'bg-kPrimaryColor text-white ring-1 ring-kPrimaryColor hover:bg-kSecondaryColor',
        'mb-1 rounded px-4 py-2 text-xs font-bold uppercase  shadow outline-none transition-all duration-150 ease-linear hover:shadow-md focus:outline-none  sm:mr-2',
      ]"
    >
      {{ props.label }}
    </RouterLink>
  </template>

  <button
    v-else
    type="button"
    :class="[
      props.isOutlined == true
        ? 'text-kPrimaryColor ring-1 ring-kPrimaryColor hover:ring-2 dark:text-kWhiteColor dark:ring-kWhiteColor'
        : 'bg-kPrimaryColor text-kWhiteColor ring-1 ring-kPrimaryColor hover:bg-kSecondaryColor dark:bg-kWhiteColor dark:text-kPrimaryColor',
      'mb-1 rounded px-4 py-2 text-xs font-bold uppercase  shadow outline-none transition-all duration-150 ease-linear hover:shadow-md focus:outline-none  sm:mr-2',
    ]"
  >
    {{ props.label }}
  </button>
</template>
