<script setup>
const props = defineProps({
  initialItem: Object,
});
</script>

<template>
  <div class="grid grid-cols-5 gap-x-4">
    <div class="col-span-3 w-full">
      <FormKit type="text" name="article" validation="required" />
    </div>
    <FormKit type="number" name="quantity" validation="required|min:1" />
    <FormKit type="text" name="uom" validation="required|min:1" />
  </div>
</template>
d
