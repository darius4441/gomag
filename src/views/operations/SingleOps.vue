<script setup>
import { ref, onMounted } from "vue-demi";
import { useTempStore } from "../../stores/temp";
import { useOperationStore } from "../../stores/operation";
import { useRoute } from "vue-router";

import axios from "axios";
import moment from "moment";
import fileDownload from "js-file-download";
import { DownloadIcon, RefreshIcon } from "@heroicons/vue/solid";

import Card from "../../components/shared/card-component.vue";
import Table from "../../components/shared/table-component.vue";
import MyButton from "../../components/shared/my-action.vue";
import router from "../../router";
import { useProductStore } from "../../stores/product";

const pageStore = useTempStore();
const productStore = useProductStore();
const operationStore = useOperationStore();
const route = useRoute();

const operationID = route.params.id;

const onApplyProcess = ref(false);
const onEditingProcess = ref(false);
const onPdfDownloadProcess = ref(false);
const canValide = ref(true);
const operation = ref({});

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

// get single operation
async function getOperation() {
  await axios
    .get(`/api/v1/operations/${operationID}`)
    .then((response) => {
      operation.value = response.data;
    })
    .catch((error) => {
      console.log(JSON.stringify(error));
    });
}

// update stock quantity
async function validateOps() {
  onApplyProcess.value = true;

  await axios
    .get(`/api/v1/operations/${operationID}/update__stock_qty/`)
    .then(() => {
      getOperation();
    })
    .catch((error) => {
      console.log(JSON.stringify(error));
    });

  onApplyProcess.value = false;
}

async function downloadPDF() {
  onPdfDownloadProcess.value = true;

  await axios
    .get(`api/v1/operations/${operationID}/generate_pdf`, {
      responseType: "blob",
    })
    .then((res) => {
      fileDownload(res.data, `operation_${operationID}.pdf`);
    })
    .catch((err) => {
      console.log(err);
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

  await getOperation();
});
</script>

<template>
  <div>
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
</template>
