<script setup>
import { Menu, MenuItems } from "@headlessui/vue";

const props = defineProps({
  menuItemsWidthClass: { type: String, default: "right-0" },
  menuItemsColorClass: { type: String, default: "divide-gray-500 bg-white" },
});
</script>

<template>
  <div class="text-right">
    <Menu as="div" class="relative w-full inline-block text-left">
      <div>
        <slot name="menu_button"></slot>
      </div>

      <transition
        enter-active-class="transition duration-100 ease-out"
        enter-from-class="transform scale-95 opacity-0"
        enter-to-class="transform scale-100 opacity-100"
        leave-active-class="transition duration-75 ease-in"
        leave-from-class="transform scale-100 opacity-100"
        leave-to-class="transform scale-95 opacity-0"
      >
        <MenuItems
          as="section"
          class="absolute z-10 mt-2 origin-top-right divide-y rounded-md px-4 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
          :class="props.menuItemsWidthClass + ' ' + props.menuItemsColorClass"
        >
          <div class="px-1 py-1">
            <slot name="title"></slot>
          </div>

          <div class="px-1 py-1">
            <slot name="menu_content"></slot>
          </div>

          <div class="px-1 py-1">
            <slot name="menu_footer"></slot>
          </div>
        </MenuItems>
      </transition>
    </Menu>
  </div>
</template>
