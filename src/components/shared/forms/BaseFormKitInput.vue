<script setup>
import { ref, computed } from "vue-demi";

import { SelectorIcon, CheckIcon } from "@heroicons/vue/solid";

const props = defineProps({
  context: Object,
});

const isOpen = ref(false);
const query = ref("");

const currentVal = computed(() => props.context._value);

const options = Object(props.context.options);

function handleInput(e) {
  if (!isOpen.value) {
    isOpen.value = true;
  }
  query.value = e.target.value;

  console.log(query.value);

  props.context.node.input(e.target.value);
}

function updateInputValue(val) {
  props.context.node.input(val);

  isOpen.value = false;
}

const selectedItemName = computed(() => {
  let valueName = currentVal.value;

  if (typeof valueName == "object") {
    valueName = valueName.name;
  }

  return valueName;
});

let filteredOptions = computed(() =>
  query.value === ""
    ? options.slice(0, 17)
    : options
        .filter((item) => {
          let filterVal = item.name
            .toLowerCase()
            .replace(/\s+/g, "")
            .includes(query.value.toLowerCase().replace(/\s+/g, ""));

          return filterVal;
        })
        .slice(0, 17)
);

const isSelected = (item) => {
  const comparator = item == props.context._value;

  return comparator;
};
</script>

<template>
  <div class="relative text-slate-700">
    <div
      class="relative mb-1 w-full max-w-md overflow-hidden rounded-lg border border-gray-400 focus-within:border-blue-500 formkit-invalid:border-red-500"
    >
      <input
        :value="selectedItemName"
        @input="handleInput"
        @blur="isOpen = false"
        class="h-10 w-full border-none px-3 pl-2 pr-6 text-base text-gray-700 placeholder-gray-400"
        :class="context.classes.combobox"
      />
      <SelectorIcon
        @click="isOpen = !isOpen"
        class="absolute right-1 top-3 h-5 w-5"
      />
    </div>

    <ul
      v-if="isOpen"
      tabindex="-1"
      class="absolute top-11 z-10 max-h-64 w-full overflow-y-auto rounded-b-lg border border-gray-400 bg-white"
    >
      <div
        v-if="filteredOptions.length === 0 && query !== ''"
        class="relative cursor-default select-none py-2 px-4 text-center text-sm text-gray-700"
      >
        Aucun resultat trouvé :(
      </div>

      <li
        v-else
        class="flex cursor-pointer justify-between px-2 py-1 text-sm hover:bg-kPrimaryColor hover:text-white"
        v-for="(opt, idx) in filteredOptions"
        :key="idx"
        :id="opt.id + '-' + idx"
        @click="updateInputValue(opt)"
      >
        <span tabindex="1" class="truncate">{{ opt.name ?? opt.label }}</span>
        <CheckIcon
          v-if="isSelected(opt) == true"
          @click="isOpen = !isOpen"
          class="h-5 w-5 text-emerald-600"
        />
      </li>
    </ul>
  </div>
</template>
