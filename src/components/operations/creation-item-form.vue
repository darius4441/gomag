<script setup>
import { useField } from "vee-validate";
import { computed, ref } from "vue-demi";

const props = defineProps({
  idx: { type: Number, default: 0 },
  checkType: { type: String, default: "out" },
  products: { type: Array, default: () => [] },
});

const emits = defineEmits(["addItem", "saveOps"]);

const { value: article } = useField(`items[${props.idx}].article`);
const { value: quantity } = useField(`items[${props.idx}].quantity`);
const { value: unit } = useField(`items[${props.idx}].unit`);
const { value: cost } = useField(`items[${props.idx}].cost`);

const products = computed(() => props.products);
const filteredProducts = ref();

const searchProducts = (event) => {
  setTimeout(() => {
    if (!event.query.trim().length) {
      filteredProducts.value = [...products.value];
    } else {
      filteredProducts.value = products.value.filter((item) => {
        return item.name.toLowerCase().includes(event.query.toLowerCase());
      });
    }
  }, 250);
};

function updateItemData(item) {
  unit.value = item.uom;
  props.checkType == "in" ? (cost.value = item.unit_cost) : (cost.value = null);
}
</script>

<template>
  <td class="whitespace-nowrap py-1 px-1.5 text-right align-middle text-xs">
    {{ props.idx + 1 }}
  </td>

  <th class="whitespace-nowrap py-1 px-1.5 text-left align-middle text-xs">
    <PrimeAutoComplete
      field="name"
      autoHighlight
      forceSelection
      dropdownMode="current"
      v-model:model-value="article"
      :suggestions="filteredProducts"
      @complete="searchProducts($event)"
      @item-select="
        updateItemData({
          uom: $event.value.uom,
          unit_cost: $event.value.unit_cost,
        })
      "
      class="w-full"
      inputClass="w-full"
    >
      <template #item="slotProps">
        <div class="flex justify-between items-center">
          <div class="">
            {{ slotProps.item.name }}
          </div>
          <span
            class="px-2 py-0.5 truncate text-white rounded-lg bg-indigo-400"
          >
            {{ slotProps.item.real_quantity }} {{ slotProps.item.uom }}
          </span>
        </div>
      </template>
    </PrimeAutoComplete>
  </th>

  <td class="whitespace-nowrap py-1 px-1.5 text-left align-middle text-xs">
    <PrimeInputNumber
      :min="1"
      mode="decimal"
      class="w-full"
      v-model:model-value="quantity"
      inputClass="w-full text-right"
      @keyup.enter="emits('addItem')"
    />
  </td>

  <td class="whitespace-nowrap py-1 px-1.5 text-center align-middle text-xs">
    <PrimeInputText
      disabled
      type="text"
      v-model:model-value="unit"
      class="w-full text-center"
    />
  </td>

  <td
    v-if="props.checkType == 'in'"
    class="whitespace-nowrap py-1 px-1.5 text-left align-middle text-xs"
  >
    <PrimeInputNumber
      :min="5"
      mode="decimal"
      v-model:model-value="cost"
      class="w-full"
      inputClass="w-full text-right"
    />
  </td>
</template>
