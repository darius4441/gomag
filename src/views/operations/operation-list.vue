<script setup>
import axios from "axios";
import { FilterMatchMode, FilterOperator } from "primevue/api";
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
  getContactName: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }],
  },
  m_type: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }],
  },
  state: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }],
  },
  date: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }],
  },
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
      contacts.value.push({
        label: contact.name,
        filterBy: `contact__id=${contact.id}`,
      });
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

onMounted(async () => {
  pageStore.updatePageName("Entrées - Sorties");

  await getContacts();
  await getAlertProducts();
});
</script>

<template>
  <div>
    <!-- Alert item modal -->
    <AlertItemModal
      :isOpen="isShowAlertItemModal"
      :product="alertProducts"
      @closeModal="isShowAlertItemModal = false"
    />

    <PrimeCard v-if="isLoading" class="p-4">
      <template #content>
        <div class="flex justify-between mb-4">
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
          class="cursor-pointer h-[60vh]"
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
          :value="operations"
          filterDisplay="menu"
          v-model:filters="filters"
          class="cursor-pointer h-[72vh]"
          v-model:selection="selectedOperations"
          @row-click="goToSingleOps($event.data.id)"
          currentPageReportTemplate="({last} sur {totalRecords})"
          :globalFilterFields="['getContactName', 'state', 'date', 'm_type']"
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
            class="text-sm truncate"
          >
            <template #body="{ data }">
              <span class="font-bold">
                dpt1/{{ data.m_type }}{{ data.id }}
              </span>
            </template>

            <template #filter="{ filterModel }">
              <PrimeInputText
                type="text"
                v-model="filterModel.value"
                class="p-column-filter"
                placeholder="Chercher par contact"
              />
            </template>
          </PrimeColumn>

          <PrimeColumn
            field="getContactName"
            header="Contact"
            class="text-sm truncate w-3/12"
          >
            <template #body="{ data }">
              {{ data.getContactName }}
            </template>

            <template #filter="{ filterModel }">
              <PrimeInputText
                type="text"
                v-model="filterModel.value"
                class="p-column-filter"
                placeholder="Chercher par contact"
              />
            </template>
          </PrimeColumn>

          <PrimeColumn
            field="date"
            header="Date"
            dataType="date"
            :sortable="true"
            class="text-sm truncate w-1/12"
          >
            <template #body="{ data }">
              {{ formatDate(data.date) }}
            </template>
            <template #filter="{ filterModel }">
              <PrimeCalendar
                v-model="filterModel.value"
                dateFormat="dd/mm/yy"
                placeholder="dd/mm/yyyy"
              />
            </template>
          </PrimeColumn>

          <PrimeColumn
            field="state"
            header="Status"
            sortable
            :filterMenuStyle="{ width: '14rem' }"
            style="min-width: 10rem"
          >
            <template #body="{ data }">
              <span :class="'customer-badge state-' + data.state">{{
                data.state
              }}</span>
            </template>
            <template #filter="{ filterModel }">
              <PrimeDropdown
                v-model="filterModel.value"
                :options="statees"
                placeholder="Any"
                class="p-column-filter"
                :showClear="true"
              >
                <template #value="slotProps">
                  <span :class="'customer-badge state-' + slotProps.value">{{
                    slotProps.value
                  }}</span>
                </template>
                <template #option="slotProps">
                  <span :class="'customer-badge state-' + slotProps.option">{{
                    slotProps.option
                  }}</span>
                </template>
              </PrimeDropdown>
            </template>
          </PrimeColumn>
        </PrimeDataTable>
      </template>
    </PrimeCard>
  </div>
</template>
