<script setup>
import { ref, computed } from "vue-demi";

import { SelectorIcon, CheckIcon } from "@heroicons/vue/solid";

const props = defineProps({
  context: Object,
});

const isOpen = ref(false);
const query = ref("");

const options = Object(props.context.options);
const item = ref(props.context.value || {});

function handleInput(e) {
  props.context.node.input(e.target.value);
  query.value = e.target.value;
  console.log(item.value);
}

function updateInputValue(val) {
  props.context.node.input(val);
  console.log(item.value);

  isOpen.value = false;
}

let filteredOptions = computed(() =>
  query.value === ""
    ? options.slice(0, 17)
    : options
        .filter(
          (item) =>
            item.name ??
            item.label
              .toLowerCase()
              .replace(/\s+/g, "")
              .includes(query.value.toLowerCase().replace(/\s+/g, ""))
        )
        .slice(0, 17)
);

const isSelected = (item) => {
  const comparator = item == props.context._value;

  return comparator;
};
</script>

<template>
  <div class="relative text-slate-700">
    <div class="relative">
      <input
        :value="props.context._value"
        @input="handleInput"
        @click="isOpen = true"
        class="pl-2 pr-6"
        :class="context.classes.combobox"
      />
      <SelectorIcon
        @click="isOpen = !isOpen"
        class="absolute right-1 top-1 h-5 w-5"
      />
    </div>

    <ul
      v-if="isOpen"
      class="absolute top-8 z-10 max-h-64 w-full overflow-y-auto rounded-b-lg bg-white"
    >
      <div
        v-if="filteredOptions.length === 0 && query !== ''"
        class="relative cursor-default select-none py-2 px-4 text-gray-700"
      >
        Desolé, il n'y a aucune correspondance.
      </div>

      <li
        v-else
        class="flex cursor-pointer justify-between px-2 py-1 text-sm hover:bg-kPrimaryColor hover:text-white"
        v-for="(opt, idx) in filteredOptions"
        :key="idx"
        @click="updateInputValue(opt ?? opt)"
      >
        <span class="truncate">{{ opt.name ?? opt.label }}</span>
        <CheckIcon
          v-if="isSelected(opt) == true"
          @click="isOpen = !isOpen"
          class="h-5 w-5 text-emerald-600"
        />
      </li>
    </ul>
  </div>
</template>
