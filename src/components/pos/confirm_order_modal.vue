<script setup>
import { useNow, useDateFormat } from "@vueuse/core";
import { PrinterIcon, DownloadIcon } from "@heroicons/vue/solid";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogOverlay,
  DialogTitle,
  DialogDescription,
} from "@headlessui/vue";

import MyButton from "../shared/my-action.vue";

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  order: { type: Object },
  overlay_bg: { type: String, default: "bg-slate-600/70" },
});

const emits = defineEmits(["closeModal"]);

const date = useDateFormat(useNow(), "DD-MM-YYYY");
const time = useDateFormat(useNow(), "HH:mm");

function closeModal() {
  emits("closeModal");
}

const overlayClass = `fixed inset-0 ${props.overlay_bg}`;
</script>

<template>
  <TransitionRoot appear :show="props.isOpen" as="template">
    <Dialog as="div" @close="closeModal" class="w-60">
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
            <DialogOverlay :class="overlayClass" />
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
              class="text-sm inline-block max-w-sm transform overflow-hidden rounded-2xl bg-white p-3 text-left align-middle shadow-xl transition-all"
            >
              <DialogTitle>
                <div>
                  <h3 class="text-center font-bold">DIM-AD</h3>
                  <div>
                    <span>Contact:</span>
                    <span> +225 27 30 62 5060 </span>
                    <span> +225 85 32 4567 </span>
                  </div>
                  <p>
                    Vendeur
                    <span>Succursale 5</span>
                    <span> - Administrateur</span>
                  </p>
                </div>

                <div
                  class="flex border-y py-2 border-black border-dashed justify-between mt-2"
                >
                  <span class="text-center">{{ date }}</span>
                  <span class="text-center ml-3">Réçu n°{{ date }}</span>
                  <span class="text-center">{{ time }}</span>
                </div>
              </DialogTitle>

              <DialogDescription>
                <div class="mt-2">
                  <table class="w-full">
                    <tbody>
                      <tr v-for="(item, idx) in props.order.items" :key="idx">
                        <td
                          class="whitespace-nowrap py-1 text-left align-middle text-xs"
                        >
                          {{ item.article }}
                        </td>
                        <td
                          class="whitespace-nowrap py-1 text-left align-middle text-xs"
                        >
                          {{ item.quantity }}
                        </td>
                        <td
                          class="whitespace-nowrap py-1 text-left align-middle text-xs"
                        >
                          {{ item.unit }}
                        </td>
                        <td
                          class="whitespace-nowrap py-1 text-left align-middle text-xs"
                        >
                          {{
                            (item.quantity * item.unit_price).toLocaleString()
                          }}F
                        </td>
                      </tr>
                    </tbody>

                    <tfoot class="border-black border-t border-dashed">
                      <tr>
                        <td class="text-lg h-8">Net à payer</td>
                        <td></td>
                        <td></td>
                        <td class="text-lg">
                          {{ order.resumeInfo.totalAmount }} F
                        </td>
                      </tr>
                      <tr>
                        <td>Sous total</td>
                        <td></td>
                        <td></td>
                        <td>{{ order.resumeInfo.subTotal }} F</td>
                      </tr>
                      <tr>
                        <td>Reduction</td>
                        <td></td>
                        <td></td>
                        <td>
                          {{
                            order.resumeInfo.discount
                              ? order.resumeInfo.discount
                              : 0
                          }}
                          F
                        </td>
                      </tr>
                      <tr>
                        <td>Total</td>
                        <td></td>
                        <td></td>
                        <td>{{ order.resumeInfo.totalAmount }} F</td>
                      </tr>
                    </tfoot>
                  </table>
                </div>

                <div
                  v-motion-slide-bottom
                  class="mt-2 border-black border-t border-dashed"
                >
                  <div class="flex mt-12 flex-row justify-between">
                    <div class="flex gap-x-4">
                      <PrinterIcon class="h-5 w-5 text-slate-600" />
                      <DownloadIcon class="h-5 w-5 text-slate-600" />
                    </div>
                    <MyButton
                      label="Valider"
                      :isOutlined="true"
                      @click="closeModal"
                    />
                  </div>
                </div>
              </DialogDescription>
            </div>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
