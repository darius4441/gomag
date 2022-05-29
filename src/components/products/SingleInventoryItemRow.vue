<template>
  <div
    class="hover: mx-3 grid cursor-pointer grid-cols-7 gap-x-3 hover:mx-0 hover:bg-gray-100 hover:px-3"
  >
    <div class="col-span-4 block w-full py-1 text-left text-sm text-gray-900">
      {{ item.getArticleName }}
    </div>
    <div class="block w-full py-1 text-right text-sm text-gray-900">
      {{ item.initial_quantity }}
    </div>
    <div class="block w-full py-1 text-center text-sm text-gray-900">
      {{ item.getArticleUom }}
    </div>
  </div>

  <!--
 <div class="ml-3 text-sm">
    <label for="remember" class="font-medium text-gray-900 dark:text-gray-300">Remember me</label>
</div>
--></template>

<script>
export default {
  name: "inventory-item-row",
  props: { initialItem: Object },

  setup(props) {
    const item = props.initialItem;

    return { item };
  },
};
</script>
