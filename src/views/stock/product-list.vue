<script setup>
import { MenuButton, MenuItem } from "@headlessui/vue";
import { ArrowSmLeftIcon, ArrowSmRightIcon } from "@heroicons/vue/solid";
import Multiselect from "@suadelabs/vue3-multiselect";
import { onLongPress } from "@vueuse/core";
import axios from "axios";
import { computed, onMounted, ref, watch } from "vue-demi";
import { useRouter } from "vue-router";
import Card from "../../components/shared/card-component.vue";
import MyButton from "../../components/shared/my-action.vue";
import MyMenu from "../../components/shared/my-menu.vue";
import Table from "../../components/shared/table-component.vue";
import { useTempStore } from "../../stores/temp";

// ? Define composables
const pageStore = useTempStore();
const router = useRouter();

const htmlRefHook = ref(null);

// ? Define vars - consts
const products = ref([]);
const search = ref("");
const options = ref([]);
const currentPage = ref(1);
const label = [
  { label: "Article", isClass: "uppercase text-left" },
  { label: "Catégorie", isClass: "uppercase text-left" },
  { label: "Fournisseur", isClass: "uppercase text-center" },
  { label: "En stock", isClass: "uppercase text-right" },
  { label: "Unité", isClass: "uppercase text-center" },
  { label: "Cout d'achat", isClass: "uppercase text-right" },
  { label: "Prix de vente", isClass: "uppercase text-right" },
];

// ? use to calculate visited item of products
const resultLen = ref(0);
const visited = computed(() => {
  var res = 0;
  products.value.next
    ? (res = (currentPage.value - 1) * resultLen.value + resultLen.value)
    : (res = products.value.count);

  return `${res} sur ${products.value.count}`;
});

// display pagination button
const asPreviousPage = ref([false]);
const asNextPage = ref([false]);

// ? Declare functions
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
  getProducts();
});

async function getProducts() {
  asPreviousPage.value = false;
  asNextPage.value = false;

  await axios
    .get(
      `/api/v1/stock/products/?page=${currentPage.value}&search=${
        search.value.name ?? ""
      }`
    )
    .then((response) => {
      resultLen.value = response.data.results.length;
      products.value = response.data;

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

  getProducts();
}

function goToNextPage() {
  currentPage.value += 1;

  getProducts();
}

function goToSingleProductsCreationPage() {
  router.push({ name: "CreateProduct" });
}

function goToMultipleProductsCreationPage() {
  router.push({ name: "CreateMultipleProducts" });
}

onLongPress(htmlRefHook, goToMultipleProductsCreationPage);

onMounted(async () => {
  pageStore.updatePageName("Stock");

  await getProducts();
});
</script>

<template>
  <div>
    <!-- Header -->
    <div class="flex w-full flex-row items-center justify-between px-4">
      <MyButton
        label="Créer produit"
        @dblclick="goToSingleProductsCreationPage"
        ref="htmlRefHook"
      />
      <MyButton label="Inventaire" to="Inventory" />
    </div>

    <!-- List of product display in table view -->
    <Card>
      <template #title>
        <div class="flex flex-row items-center justify-between">
          <h1 class="basis-1/2 text-sm">
            Liste des produits -
            <span class="text-sm font-light">
              {{ visited }} resultat<span v-if="resultLen > 1">s</span>
            </span>
          </h1>

          <MyMenu
            menuItemsWidthClass="left-0 top-8"
            menuItemsColorClass="bg-kPrimaryColor divide-gray-100"
            class="w-64 text-sm font-light text-white"
          >
            <template #menu_button>
              <MenuButton>
                <MyButton label="Filtrer" />
              </MenuButton>
            </template>

            <template #menu_content>
              <MenuItem
                as="div"
                class="cursor-pointer truncate py-1 hover:font-bold"
              >
                Produit fini
              </MenuItem>

              <MenuItem
                as="div"
                class="cursor-pointer truncate py-1 hover:font-bold"
              >
                Produit en alerte
              </MenuItem>

              <MenuItem
                as="div"
                class="cursor-pointer truncate py-1 hover:font-bold"
              >
                Non suivie
              </MenuItem>

              <MenuItem
                as="div"
                class="cursor-pointer truncate py-1 hover:font-bold"
              >
                Prix non traité
              </MenuItem>

              <MenuItem
                as="div"
                class="cursor-pointer truncate py-1 hover:font-bold"
              >
                Fournisseur
                <ul class="hidden">
                  <li>SODISMADCI</li>
                  <li>HASSAN ATTIE</li>
                </ul>
              </MenuItem>

              <MenuItem
                as="div"
                class="cursor-pointer truncate py-1 hover:font-bold"
              >
                <span>Catégorie</span>
                <ul class="hidden">
                  <li>Carrelage</li>
                  <li>Divers</li>
                  <li>Electricité</li>
                  <li>Etanchéité</li>
                  <li>Maçonnerie</li>
                  <li>Menuiserie</li>
                  <li>Peinture</li>
                  <li>Plomberie</li>
                  <li>Sanitaire</li>
                  <li>Serrure</li>
                  <li>Tuyauterie</li>
                </ul>
              </MenuItem>
            </template>
          </MyMenu>

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
        </div>
      </template>

      <template #content>
        <Table
          what_data="product"
          :label_with_filter_name_and_class="label"
          :data_list="products.results"
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
