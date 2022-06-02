<script setup>
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogOverlay,
  DialogTitle,
} from "@headlessui/vue";

import MyButton from "../../my-action.vue";

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  product: { type: Object, default: () => {} },
});

const emits = defineEmits(["closeModal", "refreshProduct"]);

function closeModal() {
  emits("closeModal");
}
</script>

<template>
  <TransitionRoot appear :show="props.isOpen" as="template">
    <Dialog as="div" @close="closeModal">
      <div class="fixed inset-0 z-10 overflow-y-auto">
        <div class="min-h-screen px-4 text-center">
          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0"
            enter-to="opacity-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100"
            leave-to="opacity-0"
          >
            <DialogOverlay class="fixed inset-0 bg-slate-600/70" />
          </TransitionChild>

          <span class="inline-block h-screen align-middle" aria-hidden="true">
            &#8203;
          </span>

          <TransitionChild
            as="template"
            enter="duration-300 ease-out"
            enter-from="opacity-0 scale-95"
            enter-to="opacity-100 scale-100"
            leave="duration-200 ease-in"
            leave-from="opacity-100 scale-100"
            leave-to="opacity-0 scale-95"
          >
            <div
              class="my-8 inline-block w-full max-w-md transform overflow-hidden rounded-2xl bg-white p-6 text-left align-middle shadow-xl transition-all"
            >
              <DialogTitle
                as="h3"
                class="text-lg font-medium leading-6 text-gray-900"
              >
                Revoyer la quantité de ces produits
              </DialogTitle>
              <div class="my-6">
                <table class="relative w-full">
                  <thead>
                    <tr>
                      <td
                        class="sticky top-0 whitespace-nowrap bg-kWhiteColor py-3 text-left align-middle text-xs font-semibold dark:bg-kDarkColor"
                      >
                        Article
                      </td>
                      <td
                        class="sticky top-0 whitespace-nowrap bg-kWhiteColor py-3 text-right align-middle text-xs font-semibold dark:bg-kDarkColor"
                      >
                        Besoin
                      </td>
                      <td
                        class="sticky top-0 whitespace-nowrap bg-kWhiteColor py-3 text-right align-middle text-xs font-semibold dark:bg-kDarkColor"
                      >
                        Disponible
                      </td>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="(item, idx) in props.product"
                      :key="idx"
                      class="cursor-pointer py-1 hover:bg-kPrimaryColor hover:text-kWhiteColor"
                    >
                      <td
                        class="whitespace-nowrap py-2.5 text-left align-middle text-xs"
                      >
                        {{ item.get_article_name }}
                      </td>
                      <td
                        class="whitespace-nowrap py-2.5 text-right align-middle text-xs"
                      >
                        {{ item.quantity }} {{ item.unit }}
                      </td>
                      <td
                        class="whitespace-nowrap py-2.5 text-right align-middle text-xs font-bold text-red-500"
                      >
                        {{ parseFloat(item.get_article_available_qty) }}
                        {{ item.unit }}
                      </td>
                    </tr>
                  </tbody>
                </table>

                <div class="mt-8 flex justify-center">
                  <MyButton label="Fermer" @click="closeModal" />
                </div>
              </div>
            </div>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
