<script setup>
import { Popover, PopoverPanel } from "@headlessui/vue";

const props = defineProps({
  menuItemsWidthClass: { type: String, default: "right-0" },
  menuItemsColorClass: { type: String, default: "divide-gray-500 " },
});
</script>

<template>
  <div class="text-right">
    <Popover as="div" class="relative inline-block w-full text-left">
      <div>
        <slot name="button"></slot>
      </div>

      <transition
        enter-active-class="transition duration-100 ease-out"
        enter-from-class="transform scale-95 opacity-0"
        enter-to-class="transform scale-100 opacity-100"
        leave-active-class="transition duration-75 ease-in"
        leave-from-class="transform scale-100 opacity-100"
        leave-to-class="transform scale-95 opacity-0"
      >
        <PopoverPanel
          as="section"
          class="absolute z-10 mt-3 -translate-x-1/2 transform px-4"
          :class="props.menuItemsWidthClass + ' ' + props.menuItemsColorClass"
        >
          <div
            class="overflow-hidden rounded-lg shadow-lg ring-1 ring-black ring-opacity-5"
          >
            <div
              class="relative bg-white p-7 dark:bg-kPrimaryColor lg:grid-cols-2"
            >
              <slot name="content"></slot>
            </div>
          </div>
        </PopoverPanel>
      </transition>
    </Popover>
  </div>
</template>
