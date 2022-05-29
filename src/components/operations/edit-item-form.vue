<script>
import { ref } from "vue-demi";
import { useProductStore } from "../../stores/product";

import { TrashIcon } from "@heroicons/vue/solid";

import MyInput from "../shared/forms/BaseInput.vue";

export default {
  name: "CreateOpsItems",

  components: { MyInput, TrashIcon },

  props: {
    idx: Number,
  },

  setup(props, context) {
    // init utils composables to variables
    const store = useProductStore();

    // Define vars / const
    const uom_displayer = ref("");
    const products = store.products;

    // define functions
    function setUomDisplayerVal(val) {
      uom_displayer.value = val.getUom;
    }

    function emitSomething(label, val) {
      val ? context.emit(label, val) : context.emit(label);
    }

    return {
      uom_displayer,
      products,
      setUomDisplayerVal,
      emitSomething,
    };
  },
};
</script>

<template>
  <h3 class="col-span-1 mt-1 h-6 text-right text-sm">
    {{ idx + 1 }}
  </h3>
  <div class="col-span-6">
    <MyInput
      type="combobox"
      :name="`items[${idx}].article`"
      :options="products"
      @addNewLineOne="emitSomething('addNewLineEDT')"
      @cbboxValOne="setUomDisplayerVal"
      myclass="h-6"
      placeholder="Article"
      :newErrorPath="`errors['items[${idx}].article']`"
    />
  </div>

  <div class="col-span-2">
    <MyInput
      type="number"
      :name="`items[${idx}].quantity`"
      myclass="h-6 col-span-1 text-right"
      placeholder="Quantité"
      :newErrorPath="`errors['items[${idx}].quantity']`"
    />
  </div>

  <div class="col-span-2">
    <input
      type="text"
      v-model="uom_displayer"
      placeholder="uom"
      disabled
      class="col-span-1 h-6 w-16 bg-blue-50 text-center"
    />
  </div>

  <TrashIcon
    @click="emitSomething('removeLineEDT', idx)"
    class="col-span-1 mt-1 h-5 w-5 cursor-pointer text-red-500"
  />
</template>
