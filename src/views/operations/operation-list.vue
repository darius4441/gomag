<script setup>
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
  PopoverButton,
} from "@headlessui/vue";
import {
  ArrowSmLeftIcon,
  ArrowSmRightIcon,
  ChevronUpIcon,
  FilterIcon,
} from "@heroicons/vue/solid";
import Multiselect from "@suadelabs/vue3-multiselect";
import axios from "axios";
import { computed, onMounted, ref } from "vue-demi";
import Card from "../../components/shared/card-component.vue";
import AlertItemModal from "../../components/shared/modals/products/items-to-be-counted-modal.vue";
import MyButton from "../../components/shared/my-action.vue";
import MyPopover from "../../components/shared/popover-component.vue";
import Table from "../../components/shared/table-component.vue";
import { useTempStore } from "../../stores/temp";

const pageStore = useTempStore();
const label = [
  { label: "Reférence", isClass: "uppercase text-left" },
  { label: "Contact", isClass: "uppercase text-left" },
  { label: "Date", isClass: "uppercase text-center" },
  { label: "Etat", isClass: "uppercase text-left" },
];
const operations = ref({});
const contacts = ref([]);
const search = ref("");
const options = ref([]);
const currentPage = ref(1);
const alertProducts = ref([]);
const isShowAlertItemModal = ref(false);

const filterInfo = ref([
  { name: "à compter", filterBy: "" },
  { name: "contact", filterOption: computed(() => contacts.value) },
  {
    name: "Etat",
    filterOption: [
      { label: "brouillon", filterBy: "state=draft" },
      { label: "en attente", filterBy: "state=pending" },
      { label: "fait", filterBy: "state=done" },
    ],
  },
  {
    name: "Type",
    filterOption: [
      { label: "entrée", filterBy: "m_type=in" },
      { label: "sortie", filterBy: "m_type=out" },
      { label: "retour", filterBy: "m_type=rtn" },
    ],
  },
]);

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

function addFilter(newQuery) {
  search.value.trim()
    ? (search.value = `${search.value}&${newQuery.filterBy}`)
    : (search.value = `&${newQuery.filterBy}`);

  options.value.push({
    id: options.value.length,
    name: newQuery.label,
  });

  getOperations();
  // console.log(search.value);
}

async function getContacts() {
  await axios.get("api/v1/contacts/").then((res) => {
    contacts.value = [];

    for (let i = 0; i < res.data.length; i++) {
      const contact = res.data[i];
      contacts.value.push({
        label: contact.name,
        filterBy: `contact__id=${contact.id}`,
      });
    }
  });
}

async function getOperations() {
  asPreviousPage.value = false;
  asNextPage.value = false;

  await axios
    .get(`/api/v1/operations/?page=${currentPage.value}${search.value}`)
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

async function getAlertProducts() {
  await axios
    .get("/api/v1/items/items_to_be_counted")
    .then((response) => {
      alertProducts.value = response.data.items_to_be_counted;
      isShowAlertItemModal.value = true;
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

  await getContacts();
  await getOperations();
});
</script>

<template>
  <div>
    <!-- Header -->
    <div class="mx-auto w-full px-4">
      <div class="flex w-full flex-row items-end justify-between">
        <MyButton label="Créer une opération" to="CreateOps" />
        <div class="flex gap-x-4 items-center">
          <MyPopover menuItemsWidthClass="w-64 left-0">
            <template #button>
              <PopoverButton
                class="flex flex-row items-center rounded px-2 py-1 text-xs font-bold uppercase text-kPrimaryColor shadow outline-none ring-1 ring-kPrimaryColor transition-all duration-150 ease-linear hover:shadow-md hover:ring-2 focus:outline-none dark:text-kWhiteColor sm:mr-2"
              >
                <FilterIcon class="mr-1 h-3 w-3" />
                <span class="font-bold">Filtrer</span>
              </PopoverButton>
            </template>
            <template #content>
              <div v-for="(filter, idx) in filterInfo" :key="idx">
                <Disclosure v-if="'filterOption' in filter" v-slot="{ open }">
                  <DisclosureButton
                    class="mt-3 flex w-full justify-between rounded bg-kPrimaryColor px-4 py-2 text-xs font-bold uppercase text-kWhiteColor shadow outline-none ring-1 ring-kPrimaryColor transition-all duration-150 ease-linear hover:bg-kSecondaryColor hover:shadow-md focus:outline-none dark:bg-kWhiteColor dark:text-kPrimaryColor sm:mr-2"
                  >
                    <span>{{ filter.name }}</span>
                    <ChevronUpIcon
                      :class="open ? 'rotate-180 transform' : ''"
                      class="h-5 w-5"
                    />
                  </DisclosureButton>
                  <DisclosurePanel
                    class="max-h-64 overflow-y-auto px-4 text-sm"
                  >
                    <div v-for="(opt, i) in filter.filterOption" :key="i">
                      <MyButton
                        :label="opt.label"
                        :isOutlined="true"
                        @click="addFilter(opt)"
                        class="mx-auto mt-2 w-11/12"
                      />
                    </div>
                  </DisclosurePanel>
                </Disclosure>

                <MyButton
                  v-else
                  :label="filter.name"
                  :isOutlined="true"
                  @click="
                    filter.name == 'à compter' ? getAlertProducts() : null
                  "
                  class="mt-2 w-full"
                />
              </div>
            </template>
          </MyPopover>

          <multiselect
            v-model="options"
            :options="options"
            :custom-label="customLabel"
            :multiple="true"
            placeholder="Filtrer"
            label="name"
            selectLabel="appliquer ce filtre"
            selectedLabel="déjà appliqué"
            deselectLabel="supprimer le filtre"
            track-by="name"
            :showNoResults="false"
          >
            <template v-slot:noOptions>...</template>
          </multiselect>
        </div>
      </div>
    </div>

    <!-- Alert item modal -->
    <AlertItemModal
      :isOpen="isShowAlertItemModal"
      :product="alertProducts"
      @closeModal="isShowAlertItemModal = false"
    />

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
