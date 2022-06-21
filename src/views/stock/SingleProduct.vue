<script setup>
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import {
  ArrowDownIcon,
  CheckCircleIcon,
  ChevronUpIcon,
} from "@heroicons/vue/solid";
import { useLocalStorage } from "@vueuse/core";
import axios from "axios";
import moment from "moment";
import { useToast } from "primevue/usetoast";
import { computed, onMounted, ref } from "vue-demi";
import { useRoute, useRouter } from "vue-router";
import HeadInfo from "../../components/products/SingleProductTopInfo.vue";
import BaseModal from "../../components/shared/modals/BaseModal.vue";
import InitialQty from "../../components/shared/modals/products/initial-qty.vue";
import MyButton from "../../components/shared/my-action.vue";
import { useProduct } from "../../composables";
import { useTempStore } from "../../stores/temp";

//? declare composables
const route = useRoute();
const router = useRouter();
const storePage = useTempStore();
const toast = useToast();

//? declare vars / consts
const productID = route.params.id;
const { product, isLoading, refetch } = useProduct(productID);
const { refetch: refetchP } = useProduct(productID);
const optMenu = ref();

const productHistory = ref([]);
const isShowModal = ref(false);
const isShowArchiveDeletionModal = ref(false);
const archiveDeletionModalTitle = ref("");
const breadcrumb = ref({
  home: {
    icon: "pi pi-home",
    to: "/stock/products",
  },
  items: [{ label: computed(() => product.value.name) }],
});
const optionsMenu = ref([
  {
    label: "Options",

    items: [
      {
        label: "Archiver",
        icon: "pi pi-eye-slash",
        command: () => enableArchiveDeletionModal("archiver"),
      },
      {
        label: "Dupliquer",
        icon: "pi pi-copy",
        command: () => goToDuplicatePage(),
      },
      {
        label: "Supprimer",
        icon: "pi pi-trash",
        command: () => enableArchiveDeletionModal("supprimer"),
      },
    ],
  },
]);

//? declare functions
function openModal() {
  isShowModal.value = true;
}

const trueProductTypeLabel = (label) => {
  switch (label) {
    case "storable":
      return "Produit stockable";

    case "service":
      return "Service";

    case "consumable":
      return "Consommable";

    default:
      break;
  }
};

const toggleOptMenu = (event) => {
  optMenu.value.toggle(event);
};

async function getProductHistory() {
  await axios
    .get(`/api/v1/operations/?items__article=${productID}`)
    .then((response) => {
      productHistory.value = response.data;
    })
    .catch((error) => {
      console.log(JSON.stringify(error));
    });
}

function goToEditPage() {
  useLocalStorage("vueUseEditProduct", product.value);
  router.push({ name: "EditProduct", params: { id: productID } });
}

function goToDuplicatePage() {
  localStorage.setItem("vueUseDuplicateProduct", JSON.stringify(product.value));

  router.push({ name: "DuplicateProduct" });
}

function goToCreatePage() {
  localStorage.setItem(
    "vueUseLastProduct",
    JSON.stringify({ id: product.value.id, name: product.value.name })
  );

  router.push({ name: "CreateProduct" });
}

function goToHistorySingleProduct(id, isNewTab) {
  if (isNewTab ?? false) {
    const routeData = router.resolve({
      name: "SingleProduct",
      params: { id: id },
    });

    window.open(routeData.href, "blank");
  } else {
    router.push({ name: "SingleProduct", params: { id: id } });
  }
}

async function archiveProduct() {
  try {
    await axios
      .patch(`api/v1/stock/products/${productID}/`, { isArchived: true })
      .then(() => {
        toast.add({
          severity: "success",
          summary: "Archivage",
          detail: "Article archivé avec succès",
          life: 3000,
        });
        router.push({ name: "Products" });
      })
      .catch((e) => {
        throw e;
      });
  } catch (error) {
    let displayMessage;

    switch (error.message) {
      case "Network Error":
        displayMessage = "Problème de connexion avec la base de donnée";
        break;

      default:
        displayMessage = error.message;
        break;
    }

    toast.add({
      severity: "error",
      summary: "Une erreur s'est produite",
      detail: displayMessage,
      life: 3000,
    });
  }
}

async function deleteProduct() {
  try {
    await axios
      .delete(`api/v1/stock/products/${productID}/`)
      .then(() => {
        toast.add({
          severity: "success",
          summary: "Suppression",
          detail: "Article supprimé avec succès",
          life: 3000,
        });

        router.push({ name: "Products" });
      })
      .catch((e) => {
        throw e;
      });
  } catch (error) {
    let displayMessage;

    switch (error.message) {
      case "Network Error":
        displayMessage = "Problème de connexion avec la base de donnée";
        break;

      case "Request failed with status code 500":
        displayMessage =
          "Impossible de supprimer cet article, veillez l'archiver";
        break;

      default:
        displayMessage = error.message;
        break;
    }

    toast.add({
      severity: "error",
      summary: "Une erreur s'est produite",
      detail: displayMessage,
      life: 3000,
    });
  }
}

function enableArchiveDeletionModal(title) {
  isShowArchiveDeletionModal.value = true;
  archiveDeletionModalTitle.value = title;
}

const getFormattedTime = (date) => {
  return moment(date).format("DD-MM-YYYY");
};

onMounted(async () => {
  storePage.updatePageName("Stock");

  await getProductHistory();
});
</script>

<template>
  <div class="flex flex-col md:flex-row">
    <PrimeToast />

    <div class="basis-3/5">
      <template v-if="!isLoading">
        <div class="flex flex-col">
          <!-- Header -->
          <div class="px-4">
            <PrimeBreadcrumb
              :home="breadcrumb.home"
              :model="breadcrumb.items"
            />

            <PrimeToolbar p-toolbar="">
              <template #start>
                <PrimeButton
                  label="Modifier"
                  class="p-button-info mr-4 p-button-sm"
                  @click="goToEditPage"
                />

                <PrimeButton
                  label="Créer"
                  class="p-button-info p-button-sm p-button-outlined"
                  @click="goToCreatePage"
                />
              </template>

              <template #end>
                <div>
                  <PrimeButton
                    type="button"
                    icon="pi pi-sliders-h"
                    class="p-button-help p-button-outlined p-button-sm"
                    @click="toggleOptMenu"
                    aria-haspopup="true"
                    aria-controls="overlay_menu"
                  />
                  <PrimeMenu
                    id="overlay_menu"
                    ref="optMenu"
                    :model="optionsMenu"
                    :popup="true"
                  />
                </div>
              </template>
            </PrimeToolbar>
          </div>

          <!-- modals conditional display -->
          <InitialQty
            :isOpen="isShowModal"
            :product="product"
            @refreshProduct="refetch"
            @refreshProducts="refetchP"
            @closeModal="isShowModal = false"
          />

          <BaseModal
            :isOpen="isShowArchiveDeletionModal"
            overlay_bg="bg-red-600/70"
            @closeModal="isShowArchiveDeletionModal = false"
          >
            <template #dialog_title>Confirmation</template>
            <template #dialog_content
              >Voulez vous réellement {{ archiveDeletionModalTitle }} cet
              article ?</template
            >
            <template #dialog_footer>
              <div class="flex flex-row">
                <MyButton
                  label="OUI"
                  :isOutlined="false"
                  @click="
                    archiveDeletionModalTitle === 'supprimer'
                      ? deleteProduct()
                      : archiveProduct()
                  "
                />
                <MyButton
                  label="NON"
                  :isOutlined="true"
                  @click="isShowArchiveDeletionModal = false"
                />
              </div>
            </template>
          </BaseModal>

          <PrimeCard>
            <template #title>
              <div class="mb-4 flex h-16 justify-end border-b-2">
                <HeadInfo
                  label="En stock"
                  :value="product.real_quantity"
                  icon="stock"
                  @dblclick="openModal()"
                />
                <HeadInfo
                  label="Tracabilité"
                  :value="product.real_quantity"
                  icon="tracability"
                />
                <HeadInfo
                  label="Réapprovisionner"
                  :value="product.real_quantity"
                  icon="replenishment"
                />
              </div>
            </template>

            <template #content>
              <!-- name and photo input -->
              <div class="mb-1 flex w-full flex-row items-end gap-x-12">
                <div class="w-5/6">
                  <span class="mb-2 block text-sm font-medium">
                    Nom du produit
                  </span>
                  <div
                    class="block w-full rounded-lg border bg-kPrimaryColor/25 p-1 text-sm font-bold tracking-wide"
                  >
                    {{ product.name }}
                  </div>
                </div>
                <div
                  class="dark:bg-kBgColor h-24 w-24 rounded-lg border border-gray-300 bg-kPrimaryColor/25"
                >
                  <span>photo</span>
                </div>
              </div>

              <!-- other input -->
              <div class="flex flex-row gap-x-32">
                <!-- left part -->
                <div class="flex w-full flex-col gap-y-3">
                  <div>
                    <span class="mb-2 block text-sm font-medium"> Type </span>

                    <div
                      class="block w-full rounded-lg border bg-kPrimaryColor/25 p-1 text-sm font-bold tracking-wide"
                    >
                      {{ trueProductTypeLabel(product.prod_type) }}
                    </div>
                  </div>
                  <div>
                    <span class="mb-2 block text-sm font-medium">
                      Categorie
                    </span>
                    <div
                      class="block w-full rounded-lg border bg-kPrimaryColor/25 p-1 text-sm font-bold tracking-wide"
                    >
                      {{ product.get_category }}
                    </div>
                  </div>

                  <div>
                    <span class="mb-2 block text-sm font-medium"> Code </span>
                    <div
                      class="block h-7 w-full rounded-lg border bg-kPrimaryColor/25 p-1 text-sm font-bold tracking-wide"
                    >
                      {{ product.code }}
                    </div>
                  </div>
                </div>

                <!-- right part -->
                <div class="flex w-full flex-col gap-y-2">
                  <div>
                    <span class="mb-2 block text-sm font-medium">
                      Unité de mesure
                    </span>
                    <div
                      class="block w-full rounded-lg border bg-kPrimaryColor/25 p-1 text-sm font-bold tracking-wide"
                    >
                      {{ product.uom }}
                    </div>
                  </div>

                  <div>
                    <span class="mb-2 block text-sm font-medium">
                      Société / Fournisseur
                    </span>
                    <div
                      class="block h-7 w-full truncate rounded-lg border bg-kPrimaryColor/25 p-1 text-sm font-bold tracking-wide"
                    >
                      {{ product.providers }}
                    </div>
                  </div>

                  <div class="flex flex-row gap-x-6 rounded-lg">
                    <div class="block w-full py-1">
                      <span class="mb-2 block truncate text-sm font-medium">
                        Stock alerte
                      </span>
                      <div
                        class="block w-full rounded-lg border bg-kPrimaryColor/25 p-1 text-sm font-bold tracking-wide"
                      >
                        {{ product.alert_stock }}
                      </div>
                    </div>
                    <div class="block w-full py-1">
                      <span class="mb-2 block truncate text-sm font-medium">
                        Stock idéal
                      </span>
                      <div
                        class="block w-full rounded-lg border bg-kPrimaryColor/25 p-1 text-sm font-bold tracking-wide"
                      >
                        {{ product.optimal_stock }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- bottom part -->
              <div class="mb-3">
                <span class="mb-2 block text-sm font-medium">
                  Description
                </span>
                <div
                  class="block h-28 w-full rounded-lg border bg-kPrimaryColor/25 p-1 text-sm font-bold tracking-wide"
                >
                  {{ product.description }}
                </div>
              </div>
            </template>
          </PrimeCard>
        </div>
      </template>
    </div>

    <div class="basis-2/5">
      <h3>Historique</h3>

      <div v-if="productHistory.length" class="w-full pt-5">
        <div
          v-for="(history, idx) in productHistory"
          :key="idx"
          class="mx-auto mt-2 w-full max-w-md rounded-2xl bg-white"
        >
          <Disclosure v-slot="{ open }">
            <DisclosureButton
              class="flex w-full justify-between rounded-lg bg-kPrimaryColor/30 px-4 py-2 text-left text-sm font-medium text-kPrimaryColor hover:bg-kPrimaryColor/50 focus:outline-none focus-visible:ring focus-visible:ring-purple-500 focus-visible:ring-opacity-75"
            >
              <div class="inline-flex">
                <span>
                  {{ getFormattedTime(history.date) }}
                </span>
                <ArrowDownIcon
                  v-if="history.m_type == 'in'"
                  class="ml-2 h-4 w-4 text-emerald-700"
                />

                <span class="ml-2">- {{ history.getContactName }}</span>
              </div>

              <ChevronUpIcon
                :class="open ? 'rotate-180 transform' : ''"
                class="h-5 w-5 text-kPrimaryColor"
              />
            </DisclosureButton>
            <DisclosurePanel
              class="max-h-64 overflow-y-auto px-4 pt-4 pb-2 text-sm"
            >
              <div
                v-for="(item, i) in history.items"
                :key="i"
                @click="goToHistorySingleProduct(item.article, true)"
                :class="[
                  item.article == productID ? '  rounded bg-pink-200 px-2' : '',
                  'flex cursor-pointer items-center hover:opacity-75',
                ]"
              >
                <CheckCircleIcon class="mr-2 h-3 w-3 text-emerald-600" />
                <span class="truncate">
                  <span class="font-bold">
                    {{
                      parseFloat(item.old_qty ?? item.get_article_available_qty)
                    }}
                  </span>
                  à
                  <span class="font-bold">
                    {{ parseFloat(item.get_article_available_qty) }}
                    {{ item.unit }}
                  </span>
                  de
                  {{ item.get_article_name }}
                </span>
              </div>
            </DisclosurePanel>
          </Disclosure>
        </div>
      </div>
    </div>
  </div>
</template>
