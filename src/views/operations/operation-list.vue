<script setup>
import { ref, onMounted, watch, computed } from "vue-demi";
import { useTempStore } from "../../stores/temp";

import axios from "axios";
import Multiselect from "@suadelabs/vue3-multiselect";
import { MenuButton, MenuItem } from "@headlessui/vue";
import {
  ArrowSmLeftIcon,
  ArrowSmRightIcon,
  FilterIcon,
} from "@heroicons/vue/solid";

import MyButton from "../../components/shared/my-action.vue";
import MyMenu from "../../components/shared/my-menu.vue";
import MyInput from "../../components/shared/forms/BaseInput.vue";
import Card from "../../components/shared/card-component.vue";
import Table from "../../components/shared/table-component.vue";

const pageStore = useTempStore();
const label = [
  { label: "Reférence", isClass: "uppercase text-left" },
  { label: "Contact", isClass: "uppercase text-left" },
  { label: "Date", isClass: "uppercase text-center" },
  { label: "Etat", isClass: "uppercase text-left" },
];
const operations = ref({});
const search = ref("");
const options = ref([]);

const currentPage = ref(1);

const filterInfo = ref({
  category: ["Quantité disponible", "Catégory", "Fournisseur"],
  property: [
    [
      { label: "inférieur à", value: "inférieur à" },
      { label: "inférieur ou égal à", value: "inférieur ou égal à" },
      { label: "égal à", value: "égal à" },
      { label: "différent de", value: "différent de" },
      { label: "suppérieur à", value: "suppérieur à" },
      { label: "supérieur ou égal à", value: "supérieur ou égal à" },
      { label: "compris entre", value: "compris entre" },
    ],
    [
      { label: "est", value: "est" },
      { label: "n'est pas", value: "n'est pas" },
      { label: "contient", value: "contient" },
      { label: "ne contient pas", value: "ne contient pas" },
      { label: "commence par", value: "commence par" },
      { label: "ne commence pas par", value: "ne commence pas par" },
      { label: "se termine par", value: "se termine par" },
      { label: "ne se termine pas par", value: "ne se termine pas par" },
    ],
  ],
});

// use to calculate visited item of operations
const resultLen = ref(0);
const visited = computed(() => {
  let res = 0;
  operations.value.next
    ? (res = (currentPage.value - 1) * resultLen.value + resultLen.value)
    : (res = operations.value.count);

  return `${res} sur ${operations.value.count}`;
});

// display pagination button
const asPreviousPage = ref([false]);
const asNextPage = ref([false]);

function customLabel({ name }) {
  return name;
}

function addTag(newTag) {
  const tag = {
    id: newTag.substring(0, 2) + Math.floor(Math.random() * 10000),
    name: newTag,
  };
  search.value = tag;
  options.value.push(tag);
}

watch(search, () => {
  getOperations();
});

async function getOperations() {
  asPreviousPage.value = false;
  asNextPage.value = false;

  await axios
    .get(
      `/api/v1/operations/?page=${currentPage.value}&search=${
        search.value.name ?? ""
      }`
    )
    .then((response) => {
      resultLen.value = response.data.results.length;
      operations.value = response.data;

      if (response.data.previous) {
        asPreviousPage.value = true;
      }

      if (response.data.next) {
        asNextPage.value = true;
      }
    })
    .catch((error) => {
      console.log(JSON.stringify(error));
    });
}

function goToPreviousPage() {
  currentPage.value -= 1;

  getOperations();
}

function goToNextPage() {
  currentPage.value += 1;

  getOperations();
}

onMounted(async () => {
  pageStore.updatePageName("Entrées - Sorties");

  await getOperations();
});
</script>

<template>
  <div>
    <!-- Header -->
    <div class="mx-auto w-full px-4">
      <div class="flex w-full flex-row items-end justify-between">
        <MyButton label="Créer une opération" to="CreateOps" />

        <MyMenu>
          <template #menu_button>
            <div class="flex flex-col">
              <multiselect
                v-model="search"
                :options="options"
                :custom-label="customLabel"
                :taggable="true"
                @tag="addTag"
                tagPlaceholder="ajouter ce filtre"
                placeholder="Filtrer"
                label="name"
                selectLabel="appliquer ce filtre"
                selectedLabel="déjà appliqué"
                deselectLabel="supprimer le filtre"
                track-by="name"
                :showNoResults="false"
                class="basis-1/2"
              >
                <template v-slot:noOptions>...</template>
              </multiselect>

              <div class="mt-3 flex">
                <div
                  class="flex flex-row items-center rounded px-2 py-1 text-xs font-bold uppercase text-kPrimaryColor shadow outline-none ring-1 ring-kPrimaryColor transition-all duration-150 ease-linear hover:shadow-md hover:ring-2 focus:outline-none dark:text-kWhiteColor sm:mr-2"
                >
                  <FilterIcon class="mr-1 h-3 w-3" />
                  <MenuButton class="font-bold">Filtrer</MenuButton>
                </div>
                <div
                  class="flex flex-row items-center rounded px-2 py-1 text-xs font-bold uppercase text-kPrimaryColor shadow outline-none ring-1 ring-kPrimaryColor transition-all duration-150 ease-linear hover:shadow-md hover:ring-2 focus:outline-none dark:text-kWhiteColor sm:mr-2"
                >
                  <FilterIcon class="mr-1 h-3 w-3" />
                  <MenuButton class="font-bold">Ordoner</MenuButton>
                </div>
              </div>
            </div>
          </template>

          <template #menu_content>
            <MenuItem as="div">
              <MyInput
                type="select"
                name="filterCat"
                :options="filterInfo.category"
              />
              <MyInput
                type="select"
                name="filterProps"
                :options="filterInfo.property"
              />

              <MyInput type="text" name="filterVal" />
            </MenuItem>
          </template>
        </MyMenu>
      </div>
    </div>

    <Card>
      <template #title>
        <h1 class="basis-1/2 text-sm">
          Liste des opérations -
          <span class="text-sm font-light">
            {{ visited }} resultat<span v-if="resultLen > 1">s</span>
          </span>
        </h1>
      </template>

      <template #content>
        <Table
          what_data="operation"
          :label_with_filter_name_and_class="label"
          :data_list="operations.results"
        />
      </template>

      <!-- pagination button -->
      <template #footer>
        <div
          v-if="currentPage >= 1"
          class="flex flex-row items-center justify-end gap-x-4 p-3"
        >
          <button
            v-if="asPreviousPage"
            @click="goToPreviousPage"
            class="mb-1 rounded px-6 py-1 text-xs font-bold uppercase text-kPrimaryColor shadow outline-none ring-1 ring-kPrimaryColor transition-all duration-150 ease-linear hover:shadow-md hover:ring-2 focus:outline-none dark:text-kWhiteColor dark:ring-kWhiteColor sm:mr-2"
          >
            <ArrowSmLeftIcon class="h-5 w-5" />
          </button>

          <button
            v-if="asNextPage"
            @click="goToNextPage"
            class="mb-1 rounded px-6 py-1 text-xs font-bold uppercase text-kPrimaryColor shadow outline-none ring-1 ring-kPrimaryColor transition-all duration-150 ease-linear hover:shadow-md hover:ring-2 focus:outline-none dark:text-kWhiteColor dark:ring-kWhiteColor sm:mr-2"
          >
            <ArrowSmRightIcon class="h-5 w-5" />
          </button>
        </div>
      </template>
    </Card>
  </div>
</template>
