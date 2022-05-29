<script setup>
import * as zod from "zod";
import { toFormValidator } from "@vee-validate/zod";
import { useForm } from "vee-validate";
import { useToast } from "vue-toast-notification";
import {
  TransitionRoot,
  TransitionChild,
  Dialog,
  DialogOverlay,
  DialogTitle,
} from "@headlessui/vue";

import MyButton from "../../my-action.vue";
import MyInput from "../../forms/BaseInput.vue";
import axios from "axios";

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  product: { type: Object, default: () => {} },
});

const emits = defineEmits(["closeModal", "refreshProduct"]);

const toast = useToast();

function closeModal() {
  emits("closeModal");
}

const validationSchema = toFormValidator(
  zod.object({
    real_quantity: zod
      .number({
        required_error: "La quantité compté est obligatoire",
        invalid_type_error: "La quantité compté doit etre un nombre",
      })
      .gte(0, { message: "La quantité compté doit avoir minimum 0" }),
  })
);

// Create a form context with the validation schema
const { handleSubmit } = useForm({
  validationSchema: validationSchema,
});

function onInvalidSubmit({ errors }) {
  Object.entries(errors).forEach((item) => {
    toast.error(item[1], {
      position: "top-right",
    });
  });
}

// auto call by node when submitForm was called
const onSubmit = handleSubmit(async (values) => {
  await axios
    .patch(`api/v1/stock/products/${props.product.id}/`, values)
    .then(() => {
      emits("refreshProduct");
      toast.success(
        `La quantité de l'article ${props.product.name} a été modifié avec succès`,
        {
          position: "top-right",
        }
      );

      closeModal();
    })
    .catch((e) => {
      toast.error(e, {
        position: "top-right",
      });
    });
}, onInvalidSubmit);
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
                {{ props.product.name }} (en {{ props.product.uom }})
              </DialogTitle>
              <div class="my-8">
                <form>
                  <MyInput
                    type="number"
                    name="real_quantity"
                    label="Quantité compté"
                  />
                </form>
              </div>

              <div class="mt-4">
                <MyButton label="Sauver" @click="onSubmit" />
                <MyButton
                  label="Annuler"
                  :isOutlined="true"
                  @click="closeModal"
                />
              </div>
            </div>
          </TransitionChild>
        </div>
      </div>
    </Dialog>
  </TransitionRoot>
</template>
