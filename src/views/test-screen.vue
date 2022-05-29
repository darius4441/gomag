<script setup>
import { ref, computed, onMounted } from "vue-demi";
import {
  Combobox,
  ComboboxInput,
  ComboboxButton,
  ComboboxOptions,
  ComboboxOption,
  TransitionRoot,
} from "@headlessui/vue";
import { CheckIcon, SelectorIcon, XIcon } from "@heroicons/vue/solid";
import { toFormValidator } from "@vee-validate/zod";
import { useField, useFieldArray, useForm } from "vee-validate";
import { useTempStore } from "../stores/temp";
import { useProductStore } from "../stores/product";
import { useToast } from "vue-toast-notification";
import * as zod from "zod";
const pageStore = useTempStore();

const toast = useToast();
const productStrore = useProductStore();
const products = computed(() => productStrore.products);

let query = ref("");

let filteredPeople = computed(() =>
  query.value === ""
    ? products.value.slice(0, 17)
    : products.value
        .filter((item) =>
          item.name
            .toLowerCase()
            .replace(/\s+/g, "")
            .includes(query.value.toLowerCase().replace(/\s+/g, ""))
        )
        .slice(0, 17)
);

const validationSchema = toFormValidator(
  zod.object({
    contact: zod
      .string({
        required_error: "contact est obligatoire",
      })
      .min(3, { message: "contact doit avoir 3 charactère minimum" }),
    items: zod
      .object({
        article: zod.object({
          id: zod.number(),
          name: zod.string({
            required_error: "obligatoire",
          }),
          prod_type: zod.string({
            required_error: "obligatoire",
          }),
          category: zod.nullable(zod.string()),
          code: zod.nullable(zod.string()),
          description: zod.nullable(zod.string()),
          uom: zod.string({
            required_error: "obligatoire",
          }),
          alert_stock: zod.number(),
          optimal_stock: zod.number(),
          real_quantity: zod.string({
            required_error: "obligatoire",
          }),
          virtual_quantity: zod.string({
            required_error: "obligatoire",
          }),
          unit_price: zod.string({
            required_error: "obligatoire",
          }),
          unit_cost: zod.string({
            required_error: "obligatoire",
          }),
          created_at: zod.string({
            required_error: "obligatoire",
          }),
          created_by: zod.number(),
          modified_at: zod.string({
            required_error: "obligatoire",
          }),
          modified_by: zod.number(),
          getUom: zod.string({
            required_error: "obligatoire",
          }),
        }),
        quantity: zod
          .number({
            required_error: "champ obligatoire",
            invalid_type_error: "la quantité doit etre un nombre réel positif",
          })
          .gte(1),
        unit: zod.string(),
      })
      .array()
      .nonempty({
        message: "Can't be empty!",
      }),
  })
);

// Create a form context with the validation schema
const { handleSubmit } = useForm({
  validationSchema: validationSchema,
});

const { value } = useField("contact");
const { remove, push, fields } = useFieldArray("items");

function addItem() {
  push({ article: {}, quantity: 1, unit: "pcs" });
}
function removeItem(id) {
  remove(id);
}

const onSubmit = handleSubmit((values) => {
  toast.info(JSON.stringify(values, null, 2));
});
onMounted(() => {
  pageStore.updatePageName("Ecran de test");
});
</script>

<template>
  <div>
    <form>
      <div>
        <input
          type="text"
          v-model="value"
          placeholder="Contact"
          class="bg-kPrimaryColor/25"
        />
      </div>
      <div
        v-for="(item, idx) in fields"
        :key="item.key"
        class="flex flex-row items-center gap-x-4 space-y-4"
      >
        <Combobox :v-model="`items[${idx}].article`">
          <div class="relative mt-1">
            <div
              class="relative w-full cursor-default overflow-hidden rounded-lg bg-white text-left shadow-md focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-teal-300 sm:text-sm"
            >
              <ComboboxInput
                class="w-full border-none py-2 pl-3 pr-10 text-sm leading-5 text-gray-900 focus:ring-0"
                :displayValue="
                  (item) => {
                    return item ? item.name : 'Veillez choisir un produit';
                  }
                "
                @change="query = $event.target.value"
              />
              <ComboboxButton
                class="absolute inset-y-0 right-0 flex items-center pr-2"
              >
                <SelectorIcon
                  class="h-5 w-5 text-gray-400"
                  aria-hidden="true"
                />
              </ComboboxButton>
            </div>
            <TransitionRoot
              leave="transition ease-in duration-100"
              leaveFrom="opacity-100"
              leaveTo="opacity-0"
              @after-leave="query = ''"
            >
              <ComboboxOptions
                class="absolute mt-1 max-h-60 w-full overflow-auto rounded-md bg-white py-1 text-base shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none sm:text-sm"
              >
                <div
                  v-if="filteredPeople.length === 0 && query !== ''"
                  class="relative cursor-default select-none py-2 px-4 text-gray-700"
                >
                  Nothing found.
                </div>

                <ComboboxOption
                  v-for="person in filteredPeople"
                  as="template"
                  :key="person.id"
                  :value="person"
                  v-slot="{ selected, active }"
                >
                  <li
                    class="relative cursor-default select-none py-2 pl-10 pr-4"
                    :class="{
                      'bg-teal-600 text-white': active,
                      'text-gray-900': !active,
                    }"
                  >
                    <span
                      class="block truncate"
                      :class="{
                        'font-medium': selected,
                        'font-normal': !selected,
                      }"
                    >
                      {{ person.name }}
                    </span>
                    <span
                      v-if="selected"
                      class="absolute inset-y-0 left-0 flex items-center pl-3"
                      :class="{
                        'text-white': active,
                        'text-teal-600': !active,
                      }"
                    >
                      <CheckIcon class="h-5 w-5" aria-hidden="true" />
                    </span>
                  </li>
                </ComboboxOption>
              </ComboboxOptions>
            </TransitionRoot>
          </div>
        </Combobox>
        <input
          type="number"
          :v-model="`items[${idx}].quantity`"
          placeholder="Qté"
          class="bg-kPrimaryColor/25"
        />
        <input
          type="text"
          :v-model="`items[${idx}].unit`"
          placeholder="uom"
          class="bg-kPrimaryColor/25"
        />
        <div
          @click="removeItem"
          class="cursor-pointer rounded-full text-red-600 hover:bg-red-600 hover:text-white"
        >
          <XIcon
            class="h-5 w-5 cursor-pointer rounded-full text-red-600 hover:bg-red-600 hover:text-white"
          />
        </div>
      </div>
    </form>

    <div class="flex flex-row items-center justify-between">
      <button
        @click="onSubmit"
        class="mt-64 rounded-lg bg-blue-600 px-3 py-2 text-white"
      >
        Submit
      </button>
      <button @click="addItem" class="mt-64">+ item</button>
    </div>
  </div>
</template>
