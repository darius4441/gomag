<script setup>
import axios from "axios";
import { FilterMatchMode } from "primevue/api";
import { useToast } from "primevue/usetoast";
import { onMounted, ref } from "vue-demi";
import { useRouter } from "vue-router";
import AlertItemModal from "../../components/shared/modals/products/items-to-be-counted-modal.vue";
import { useOperations } from "../../composables";
import { useTempStore } from "../../stores/temp";
const toast = useToast();

const pageStore = useTempStore();
const router = useRouter();
const { isLoading, operations } = useOperations();

const dt = ref();
const selectedOperations = ref();
const skOperations = ref(new Array(50));

const contacts = ref([]);
const alertProducts = ref([]);
const isShowAlertItemModal = ref(false);

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  getContactName: { value: null, matchMode: FilterMatchMode.CONTAINS },
  "items.get_article_name": {
    value: null,
    matchMode: FilterMatchMode.CONTAINS,
  },
  m_type: { value: null, matchMode: FilterMatchMode.CONTAINS },
  state: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
  date: { value: null, matchMode: FilterMatchMode.DATE_AFTER },
});

const formatDate = (value) => {
  const dateF = new Date(value);
  return dateF.toLocaleDateString("fr-FR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
};

function goToCreatePage() {
  router.push({ name: "CreateOps" });
}

function goToSingleOps(id, isNewTab) {
  if (isNewTab ?? false) {
    const routeData = router.resolve({
      name: "SingleOps",
      params: { id: id },
    });

    window.open(routeData.href, "blank");
  } else {
    router.push({ name: "SingleOps", params: { id: id } });
  }
}

const exportCSV = () => {
  dt.value.exportCSV();
};

async function getContacts() {
  await axios.get("api/v1/contacts/").then((res) => {
    contacts.value = [];

    for (let i = 0; i < res.data.length; i++) {
      const contact = res.data[i];
      contacts.value.push(contact.name);
    }
  });
}

async function getAlertProducts() {
  await axios
    .get("/api/v1/items/items_to_be_counted")
    .then((response) => {
      alertProducts.value = response.data.items_to_be_counted;
    })
    .catch((error) => {
      toast.add({
        severity: "error",
        summary: "Une erreur s'est produite",
        detail: JSON.stringify(error.message),
        life: 3000,
      });
    });
}

const formatState = (state) => {
  switch (state) {
    case "done":
      return "fait";

    case "pending":
      return "en cours";

    case "draft":
      return "brouillon";

    default:
      return "brouillon";
  }
};

const formatType = (theType) => {
  switch (theType) {
    case "in":
      return "entrée";

    case "out":
      return "sortie";

    case "rtn":
      return "retour";

    default:
      return "retour";
  }
};

const states = ref([
  { label: "Fait", value: "done" },
  { label: "En cours", value: "pending" },
  { label: "Brouillon", value: "draft" },
]);

const opsTypes = ref([
  { label: "Entrée", value: "in" },
  { label: "Sortie", value: "out" },
  { label: "Retour", value: "rtn" },
]);

onMounted(async () => {
  pageStore.updatePageName("Entrées - Sorties");

  await getContacts();
  await getAlertProducts();
});
</script>

<template>
  <div>
    <PrimeToast />

    <!-- Alert item modal -->
    <AlertItemModal
      :isOpen="isShowAlertItemModal"
      :product="alertProducts"
      @closeModal="isShowAlertItemModal = false"
    />

    <PrimeCard v-if="isLoading" class="p-4">
      <template #content>
        <div class="flex justi22-between mb-4">
          <PrimeSkeleton width="5rem" height="3rem" />

          <PrimeSkeleton width="9rem" height="3rem" class="mr-2" />

          <div class="flex">
            <PrimeSkeleton width="3rem" height="3rem" class="mr-2" />
            <PrimeSkeleton width="20rem" height="3rem" />
          </div>
        </div>

        <PrimeDataTable
          :value="skOperations"
          responsiveLayout="scroll"
          paginatorTemplate="FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
          currentPageReportTemplate="({last} sur {totalRecords})"
          class="cursor-pointer h-[60vh] p-datatable-sm"
          scrollHeight="56vh"
          :rowHover="true"
          :scrollable="true"
          filterDisplay="menu"
        >
          <PrimeColumn header="Reférence" class="text-sm truncate">
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            field="getContactName"
            header="Contact"
            class="text-sm truncate w-3/12"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            field="date"
            header="Date"
            class="text-sm truncate w-1/12"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            field="state"
            header="Etat"
            class="text-sm truncate w-1/12"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>
        </PrimeDataTable>
      </template>
    </PrimeCard>

    <PrimeCard v-else>
      <template #content>
        <PrimeDataTable
          ref="dt"
          scrollable
          :rows="50"
          dataKey="id"
          :rowHover="true"
          :paginator="true"
          scrollHeight="60vh"
          stateStorage="session"
          stateKey="operations-state"
          :value="operations"
          filterDisplay="row"
          v-model:filters="filters"
          v-model:selection="selectedOperations"
          @row-click="goToSingleOps($event.data.id)"
          class="cursor-pointer h-[72vh] p-datatable-sm"
          currentPageReportTemplate="({last} sur {totalRecords})"
          :globalFilterFields="['getContactName', 'items.get_article_name']"
          paginatorTemplate="FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
        >
          <template #header>
            <div class="flex justify-between items-center">
              <PrimeButton
                label="Créer"
                class="p-button-info mr-4 p-button-sm"
                @click="goToCreatePage"
              />

              <PrimeButton
                v-if="alertProducts.length > 0"
                label="Produit à vérifier"
                class="p-button-info p-button-outlined p-button-sm"
                @click="isShowAlertItemModal = true"
              />

              <div>
                <PrimeButton
                  icon="pi pi-upload p-button-sm p-button-help"
                  class="p-button-text mr-3"
                  @click="exportCSV($event)"
                />

                <span class="p-input-icon-left">
                  <i class="pi pi-search" />
                  <PrimeInputText
                    v-model="filters['global'].value"
                    placeholder="Recherche rapide"
                  />
                </span>
              </div>
            </div>
          </template>

          <template #empty> Aucune opération trouvé. </template>

          <template #loading>
            Chargement des opérations. Veillez patienter.
          </template>

          <!-- <PrimeColumn selectionMode="multiple" headerStyle="width: 2rem"></PrimeColumn> -->

          <PrimeColumn
            header="Reférence"
            :sortable="false"
            style="flex: 0 0 16rem"
            class="text-sm truncate"
          >
            <template #body="{ data }">
              <span class="font-bold">
                dpt1/{{ data.m_type }}{{ data.id }}
              </span>
            </template>
          </PrimeColumn>

          <PrimeColumn
            field="m_type"
            header="Type d'opération"
            sortable
            inputClass="w-full"
            class="p-column-filter"
            style="flex: 0 0 18rem"
            :filterMenuStyle="{ width: '18rem' }"
          >
            <template #body="{ data }">
              <i
                v-if="data.m_type == 'in'"
                class="pi pi-arrow-circle-down text-orange-500 mr-2"
              >
              </i>
              <i
                v-else-if="data.m_type == 'out'"
                class="pi pi-arrow-circle-up text-green-500 mr-2"
              >
              </i>
              <i v-else class="pi pi-undo text-red-500 mr-2"> </i>
              <span class="w-full">
                {{ formatType(data.m_type) }}
              </span>
            </template>

            <template #filter="{ filterModel, filterCallback }">
              <PrimeDropdown
                v-model="filterModel.value"
                @change="filterCallback()"
                :options="opsTypes"
                optionLabel="label"
                optionValue="value"
                placeholder="Tout"
                class="p-column-filter"
              >
                <template #value="slotProps">
                  <span class="w-full" v-if="slotProps.value">
                    {{ formatType(slotProps.value) }}
                  </span>
                  <span v-else>{{ slotProps.placeholder }}</span>
                </template>
                <template #option="slotProps">
                  <span class="w-full">
                    {{ slotProps.option.label }}
                  </span>
                </template>
              </PrimeDropdown>
            </template>
          </PrimeColumn>

          <PrimeColumn
            field="getContactName"
            header="Contact"
            style="min-width: 30vh"
            class="text-sm truncate text-center"
          >
            <template #filter="{ filterModel, filterCallback }">
              <PrimeDropdown
                v-model="filterModel.value"
                @change="filterCallback()"
                :options="contacts"
                placeholder="Tout"
                inputClass="w-full"
                class="p-column-filter"
              />
            </template>
          </PrimeColumn>

          <PrimeColumn
            field="date"
            header="Date"
            dataType="date"
            dateFormat="dd/mm/yy"
            :sortable="true"
            style="flex: 0 0 22rem"
            class="text-sm truncate"
          >
            <template #body="{ data }">
              {{ formatDate(data.date) }}
            </template>

            <template #filter="{ filterModel, filterCallback }">
              <PrimeCalendar
                v-model="filterModel.value"
                @change="filterCallback()"
                placeholder="Tout"
                inputClass="w-full"
                dateFormat="dd/mm/yy"
                class="p-column-filter"
              >
              </PrimeCalendar>
            </template>
          </PrimeColumn>

          <PrimeColumn
            field="state"
            header="Etat"
            sortable
            inputClass="w-full"
            class="p-column-filter"
            style="flex: 0 0 14rem"
            :filterMenuStyle="{ width: '14rem' }"
          >
            <template #body="{ data }">
              <span :class="'mx-auto customer-badge state-' + data.state">
                {{ formatState(data.state) }}
              </span>
            </template>

            <template #filter="{ filterModel, filterCallback }">
              <PrimeDropdown
                v-model="filterModel.value"
                @change="filterCallback()"
                :options="states"
                optionLabel="label"
                optionValue="value"
                placeholder="Tout"
                class="p-column-filter"
              >
                <template #value="slotProps">
                  <span
                    :class="
                      'w-full inset-0 customer-badge state-' + slotProps.value
                    "
                    v-if="slotProps.value"
                  >
                    {{ formatState(slotProps.value) }}
                  </span>
                  <span v-else>{{ slotProps.placeholder }}</span>
                </template>
                <template #option="slotProps">
                  <span
                    :class="
                      'w-full inset-0 customer-badge state-' +
                      slotProps.option.value
                    "
                  >
                    {{ slotProps.option.label }}
                  </span>
                </template>
              </PrimeDropdown>
            </template>
          </PrimeColumn>
        </PrimeDataTable>
      </template>
    </PrimeCard>
  </div>
</template>

<style scoped>
.customer-badge {
  padding: 0.05rem 1rem 0.05rem 1rem;
  border-radius: 0.2rem;
  text-transform: uppercase;
  font-weight: 700;
  font-size: 0.7rem;
}

.state-done {
  color: hsl(120, 70%, 20%);
  background-color: hsla(120, 70%, 90%, 1);
}

.state-pending {
  color: hsl(45, 70%, 20%);
  background-color: hsla(45, 70%, 90%, 1);
}

.state-draft {
  color: hsl(290, 70%, 20%);
  background-color: hsla(290, 70%, 90%, 1);
}
</style>
