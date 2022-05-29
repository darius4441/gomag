<script setup>
const props = defineProps({
  initialData: Object,
});
</script>

<template>
  <table class="relative w-full">
    <thead>
      <tr>
        <th
          class="sticky text-left top-0 whitespace-nowrap bg-kWhiteColor py-3 align-middle text-xs font-semibold dark:bg-kDarkColor"
        >
          Article
        </th>
        <th
          class="sticky text-right top-0 whitespace-nowrap bg-kWhiteColor py-3 align-middle text-xs font-semibold dark:bg-kDarkColor"
        >
          En stock
        </th>
        <th
          class="sticky top-0 text-center whitespace-nowrap bg-kWhiteColor py-3 align-middle text-xs font-semibold dark:bg-kDarkColor"
        >
          Unité
        </th>
      </tr>
    </thead>
    <tbody>
      <tr
        v-for="(item, idx) in props.initialData"
        :key="idx"
        class="py-1 hover:bg-kPrimaryColor hover:text-kWhiteColor"
      >
        <th class="whitespace-nowrap py-1 text-left align-middle text-xs">
          {{ item.name }}
        </th>
        <td class="whitespace-nowrap py-1 text-right align-middle text-xs">
          {{ item.real_quantity }}
        </td>
        <td class="whitespace-nowrap py-1 text-center align-middle text-xs">
          {{ item.uom }}
        </td>
      </tr>
    </tbody>
  </table>
</template>
