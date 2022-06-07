<script setup>
import { ref } from "vue-demi";

import MyInput from "../shared/forms/BaseInput.vue";

const props = defineProps({
  idx: { type: Number, default: 0 },
});

const emits = defineEmits(["addItem"]);

const uom = ref("");
</script>

<template>
  <td class="whitespace-nowrap py-1 px-1.5 text-right align-middle text-xs">
    {{ idx + 1 }}
  </td>

  <th class="whitespace-nowrap py-1 px-1.5 text-left align-middle text-xs">
    <MyInput
      type="combobox"
      :name="`items[${props.idx}].article`"
      placeholder="Article"
      myclass="h-6 col-span-1 text-left"
      :newErrorPath="`errors['items[${props.idx}].article']`"
      @updateUom="(val) => (uom = val.getUom)"
    />
  </th>

  <td class="whitespace-nowrap py-1 px-1.5 text-left align-middle text-xs">
    <MyInput
      type="number"
      :name="`items[${props.idx}].quantity`"
      myclass="h-6 col-span-1 text-right"
      placeholder="Quantité"
      @keydown.enter="emits('addItem')"
      :newErrorPath="`errors['items[${props.idx}].quantity']`"
    />
  </td>

  <td class="whitespace-nowrap py-1 px-1.5 text-center align-middle text-xs">
    <input
      type="text"
      v-model="uom"
      placeholder="unit"
      class="h-6 bg-kPrimaryColor/25 text-center text-slate-800 placeholder:text-slate-500 dark:text-kWhiteColor dark:placeholder:text-kWhiteColor/50"
      disabled
    />
  </td>

  <td class="whitespace-nowrap py-1 px-1.5 text-left align-middle text-xs">
    <MyInput
      type="number"
      :name="`items[${props.idx}].cost`"
      myclass="h-6 col-span-1 text-right"
      placeholder="Cout"
      @keydown.enter="emits('addItem')"
      :newErrorPath="`errors['items[${props.idx}].cost']`"
    />
  </td>
</template>
