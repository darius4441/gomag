<script setup>
import { ref, watch, onMounted } from "vue-demi";

import { useField } from "vee-validate";
import { CheckIcon, SelectorIcon } from "@heroicons/vue/solid";
import {
  Combobox,
  ComboboxInput,
  ComboboxButton,
  ComboboxOptions,
  ComboboxOption,
  TransitionRoot,
} from "@headlessui/vue";

import axios from "axios";
import moment from "moment";

const props = defineProps({
  name: String,
  type: String,
  label: String,
  defaultValue: String,
  placeholder: String,
  options: Array,
  wrapperclass: String,
  myclass: String,
  newErrorPath: String,
  todayShortcut: { type: Boolean, default: false },
  isRequired: { type: Boolean, default: false },
});

const emits = defineEmits(["addNewLineOne", "updateUom"]);

let errorMessage = "";

let defaultStyle =
  "bg-kPrimaryColor/25 text-slate-800 placeholder:text-slate-500 dark:text-kWhiteColor dark:placeholder:text-kWhiteColor/50";

// combobox filter part
const query = ref("");

const products = ref([]);

async function getProducts() {
  if (props.type === "combobox") {
    await axios
      .get(`/api/v1/stock/products/?page=${1}&search=${query.value}`)
      .then((response) => {
        products.value = response.data.results;
      })
      .catch((error) => {
        console.log(JSON.stringify(error));
      });
  }
}

function getNewData(val) {
  query.value = val;

  getProducts();
}

const { value } = useField(props.name);

// ! next line was importaint
props.type == "combobox"
  ? watch(value, () => {
      if (value.value) {
        value.value.getUom ? emits("updateUom", value.value) : null;
      }
    })
  : null;

function emitSomething(label, val) {
  val ? emits(label, val) : emits(label);
}

function setToday() {
  value.value = moment().format("YYYY-MM-DD");
}

onMounted(() => {
  getProducts();
});
</script>

<template>
  <!-- select -->
  <div v-if="type == 'select'" :class="wrapperclass">
    <label :for="name" v-show="label">{{ label }}</label>
    <select
      v-model="value"
      :class="[
        { requiredStyle: isRequired, errorStyle: errorMessage | newErrorPath },
        `${defaultStyle} ${props.myclass}`,
      ]"
    >
      <option v-for="(opt, idx) in options" :key="idx" :value="opt.value">
        {{ opt.label }}
      </option>
    </select>
  </div>

  <!-- combobox -->
  <div v-else-if="type == 'combobox'" :class="wrapperclass">
    <label :for="name" v-show="label">{{ label }}</label>
    <Combobox
      v-model="value"
      @keyup.enter="emitSomething('addNewLineOne')"
      class="h-6 w-full basis-9/12 text-left focus:border-b"
    >
      <div class="relative">
        <div
          class="relative h-6 w-full cursor-default overflow-hidden rounded-lg bg-white text-left focus:outline-none focus-visible:ring-2 focus-visible:ring-white focus-visible:ring-opacity-75 focus-visible:ring-offset-2 focus-visible:ring-offset-teal-300 sm:text-sm"
        >
          <ComboboxInput
            :class="[
              {
                requiredStyle: isRequired,
                errorStyle: errorMessage | newErrorPath,
              },
              `${defaultStyle} ${props.myclass}`,
            ]"
            :displayValue="
              (item) => {
                return item ? item.name : 'Veillez choisir un produit';
              }
            "
            @change="getNewData($event.target.value)"
          />
          <ComboboxButton
            class="absolute inset-y-0 right-0 flex items-center pr-2"
          >
            <SelectorIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
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
              v-if="products.length === 0 && query !== ''"
              class="relative cursor-default select-none py-2 px-4 text-gray-700"
            >
              Aucun article trouvé.
            </div>

            <ComboboxOption
              v-for="item in products"
              as="template"
              :key="item.id"
              :value="item"
              v-slot="{ selected, active }"
            >
              <li
                class="relative cursor-default select-none py-2 pl-10 pr-4"
                :class="{
                  ' bg-kPrimaryColor text-white': active,
                  'text-gray-900': !active,
                }"
              >
                <span
                  class="block truncate"
                  :class="{
                    'font-medium': value,
                    'font-normal': !value,
                  }"
                >
                  {{ item.name }}
                </span>
                <span
                  v-if="selected"
                  class="absolute inset-y-0 left-0 flex items-center pl-3 hover:text-white"
                >
                  <CheckIcon class="h-5 w-5" aria-hidden="true" />
                </span>
              </li>
            </ComboboxOption>
          </ComboboxOptions>
        </TransitionRoot>
      </div>
    </Combobox>
  </div>

  <!-- textarea -->
  <div v-else-if="type == 'textarea'" :class="wrapperclass">
    <label :for="name" v-show="label">{{ label }}</label>
    <textarea
      v-model="value"
      :name="name"
      :id="name"
      cols="30"
      rows="4"
      :class="[
        { requiredStyle: isRequired, errorStyle: errorMessage | newErrorPath },
        `${defaultStyle} ${props.myclass}`,
      ]"
    ></textarea>
  </div>

  <!-- date -->
  <div v-else-if="type == 'date'" :class="wrapperclass">
    <label :for="name" v-show="label">{{ label }}</label>
    <input
      type="date"
      v-model="value"
      :name="name"
      :class="[
        { requiredStyle: isRequired, errorStyle: errorMessage | newErrorPath },
        `${defaultStyle} ${props.myclass}`,
      ]"
    />

    <h6
      v-if="todayShortcut"
      @click="setToday"
      class="cursor-pointer text-right text-xs font-light text-slate-500 hover:font-bold dark:text-kWhiteColor/50"
    >
      aujourd'hui
    </h6>
  </div>

  <div v-else :class="wrapperclass">
    <label :for="name" v-show="label">{{ label }}</label>
    <input
      :type="type"
      v-model="value"
      :placeholder="placeholder ? placeholder : null"
      :class="[
        { requiredStyle: isRequired, errorStyle: errorMessage | newErrorPath },
        `${defaultStyle} ${props.myclass}`,
      ]"
    />
  </div>
</template>
