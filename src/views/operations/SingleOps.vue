<script setup>
import { DownloadIcon, RefreshIcon } from "@heroicons/vue/solid";
import axios from "axios";
import moment from "moment";
import { onMounted, ref } from "vue-demi";
import { useRoute, useRouter } from "vue-router";
import Card from "../../components/shared/card-component.vue";
import MyButton from "../../components/shared/my-action.vue";
import Table from "../../components/shared/table-component.vue";
import { useOperation, useProducts } from "../../composables";
import { useOperationStore } from "../../stores/operation";
import { useProductStore } from "../../stores/product";
import { useTempStore } from "../../stores/temp";

const { refetch: prodRefetch } = useProducts();
const route = useRoute();
const router = useRouter();
const pageStore = useTempStore();
const productStore = useProductStore();
const operationStore = useOperationStore();

const operationID = route.params.id;

const {
  isLoading: opsLoad,
  operation,
  refetch: refetchOps,
} = useOperation(operationID);

const onApplyProcess = ref(false);
const onEditingProcess = ref(false);
const onPdfDownloadProcess = ref(false);
const canValide = ref(true);

const label = [
  { label: "Article", isClass: "uppercase text-left" },
  { label: "Qté dmd", isClass: "uppercase text-right" },
  { label: "Unité", isClass: "uppercase text-center" },
  { label: "Qté dispo", isClass: "uppercase text-right" },
];

// return the real label of operation type
const trueLabel = (label) => {
  switch (label) {
    case "in":
      return "Entrées";

    case "out":
      return "Sortie";

    case "rtn":
      return "Retour";

    default:
      break;
  }
};

// update stock quantity
async function validateOps() {
  onApplyProcess.value = true;

  await axios
    .get(`/api/v1/operations/${operationID}/update__stock_qty/`)
    .then(() => {
      prodRefetch.value();
      refetchOps.value();
    })
    .catch((error) => {
      console.log(JSON.stringify(error));
    });

  onApplyProcess.value = false;
}

async function downloadPDF() {
  onPdfDownloadProcess.value = true;

  await axios.get(`api/v1/operations/${operationID}/generate_pdf`, {
    responseType: "blob",
  });

  onPdfDownloadProcess.value = false;
}

async function goToEditPage() {
  onEditingProcess.value = true;

  await productStore.getProducts();
  await operationStore.getOperation(operationID);

  router.push({ name: "EditOps", params: { id: operationID } });

  onEditingProcess.value = false;
}

function setValidate() {
  canValide.value = false;
}

const formatedDate = (date) => {
  return moment(date).format("DD-MM-YYYY");
};

onMounted(async () => {
  pageStore.updatePageName("Entrées - Sorties");
});
</script>

<template>
  <div>
    <p v-if="opsLoad">Loading...</p>

    <div v-else>
      <!-- Header -->
      <div class="mx-auto w-full px-4 print:hidden">
        <div class="flex flex-col">
          <div class="flex w-full flex-row items-center justify-between">
            <div>
              <MyButton
                label="Créer"
                v-if="operation.state != 'done'"
                to="CreateOps"
              />

              <MyButton label="Créer" v-else to="CreateOps" />

              <MyButton label="Retour" to="Operations" :isOutlined="true" />
            </div>

            <div>
              <button
                v-if="onPdfDownloadProcess"
                class="rounded-full p-1 text-kPrimaryColor hover:bg-kPrimaryColor hover:text-kWhiteColor"
              >
                <RefreshIcon class="h-5 w-5 animate-spin" />
              </button>

              <div
                v-else
                class="rounded-full p-1 text-kPrimaryColor hover:bg-kPrimaryColor hover:text-kWhiteColor"
              >
                <DownloadIcon
                  @click="downloadPDF"
                  class="h-5 w-5 cursor-pointer"
                />
              </div>
            </div>
          </div>

          <div
            v-if="operation.state != 'done'"
            class="flex flex-row items-center gap-x-4 pt-1"
          >
            <div>
              <div v-if="canValide">
                <button
                  v-if="onApplyProcess"
                  class="rounded-full p-1 text-kPrimaryColor hover:bg-kPrimaryColor hover:text-kWhiteColor"
                >
                  <RefreshIcon class="h-5 w-5 animate-spin" />
                </button>

                <button
                  v-else
                  @click="validateOps"
                  class="border-2 border-transparent text-slate-600 duration-300 ease-in-out hover:font-bold hover:underline"
                >
                  Valider
                </button>
              </div>

              <span
                v-else
                class="cursor-zoom-in border-2 border-transparent px-3 text-sm text-orange-700 duration-300 ease-in-out hover:underline"
                >Vérifier votre stock</span
              >
            </div>

            <div>
              <button
                v-if="onEditingProcess"
                class="rounded-full p-1 text-kPrimaryColor hover:bg-kPrimaryColor hover:text-kWhiteColor"
              >
                <RefreshIcon class="h-5 w-5 animate-spin" />
              </button>

              <button
                v-else
                @click="goToEditPage"
                class="border-2 border-transparent text-slate-600 duration-300 ease-in-out hover:font-bold hover:underline"
              >
                Modifier
              </button>
            </div>
          </div>
        </div>
      </div>

      <Card>
        <template #content>
          <div class="block w-full overflow-x-auto p-4">
            <!-- order main info -->

            <div
              class="mx-auto flex flex-row justify-between gap-4 rounded-lg border-2 p-4 py-4"
            >
              <!-- contact -->
              <div class="w-full">
                <span class="mb-1 block text-sm font-medium text-slate-500">
                  Contact
                </span>
                <div
                  class="truncate border-b p-1 text-sm font-semibold text-slate-600"
                >
                  {{ operation.getContactName }}
                </div>
              </div>

              <!-- operation type -->
              <div class="w-full">
                <span class="mb-1 block text-sm font-medium text-slate-500">
                  Type d'opération
                </span>
                <div
                  class="truncate border-b p-1 text-sm font-semibold text-slate-600"
                >
                  {{ trueLabel(operation.m_type) }}
                </div>
              </div>

              <!-- operation date -->
              <div class="w-full">
                <span class="mb-1 block text-sm font-medium text-slate-500">
                  Date de l'opération
                </span>
                <div
                  class="truncate border-b p-1 text-sm font-semibold text-slate-600"
                >
                  {{ formatedDate(operation.date) }}
                </div>
              </div>
            </div>
          </div>

          <!-- order items info -->
          <Table
            what_data="singleOps"
            :state="operation.state"
            :m_type="operation.m_type"
            :label_with_filter_name_and_class="label"
            :data_list="operation.items"
            @inQuantity="setValidate"
          />
        </template>
      </Card>
    </div>
  </div>
</template>
