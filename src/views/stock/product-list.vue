<script setup>
import axios from "axios";
import { FilterMatchMode } from "primevue/api";
import TriStateCheckbox from "primevue/tristatecheckbox";
import { onMounted, ref } from "vue-demi";
import { useRouter } from "vue-router";
import { useProducts } from "../../composables";

const router = useRouter();
const { products, isLoading } = useProducts();

const dt = ref();
const selectAll = ref();
const contacts = ref([]);
const selectedArticles = ref();
const skProducts = ref(new Array(50));
const totalRecords = ref();
const providers = [
  "QUALITEC",
  "INGCO",
  "INGELEC",
  "C2CI",
  "DMD",
  "SIPPEC",
  "KAFARAMI",
  "SODISMADCI SUCCURSALE 6",
  "GOODWEEL",
  "NEGOCIE",
  "HABIB",
  "DROCOLOR",
  "SEPR",
  "FIMA",
  "HASSAN ATTIE",
  "37-100",
  "BAKAYOKO",
  "FERO",
  "ASSAN ATTIE",
  "GEBACO",
  "MACACI",
];

function goToCreatePage() {
  router.push({ name: "CreateProduct" });
}

const onSelectAllChange = (event) => {
  const selectAllClick = event.checked;

  if (selectAllClick) {
    selectAll.value = true;
    selectedArticles.value = products.value;
  } else {
    selectAll.value = false;
    selectedArticles.value = [];
  }
};

const onRowSelect = () => {
  selectAll.value = selectedArticles.value.length === totalRecords.value;
};

const onRowUnselect = () => {
  selectAll.value = false;
};

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  code: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
  name: { value: null, matchMode: FilterMatchMode.CONTAINS },
  get_category: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
  providers: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
  isAlert: { value: null, matchMode: FilterMatchMode.EQUALS },
  real_quantity: { value: null, matchMode: FilterMatchMode.EQUALS },
  uom: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
  unit_cost: { value: null, matchMode: FilterMatchMode.EQUALS },
  unit_price: { value: null, matchMode: FilterMatchMode.EQUALS },
  created_at: { value: null, matchMode: FilterMatchMode.IN },
  created_by: { value: null, matchMode: FilterMatchMode.EQUALS },
  modified_at: { value: null, matchMode: FilterMatchMode.DATE_IS },
  modified_by: { value: null, matchMode: FilterMatchMode.EQUALS },
});

const formatDate = (value) => {
  return value.toLocaleDateString("fr-FR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  });
};

const formatCurrency = (value) => {
  return value.toLocaleString("fr", {
    style: "currency",
    currency: "XOF",
  });
};

const exportCSV = () => {
  dt.value.exportCSV();
};

function goToSingleProduct(id, isNewTab) {
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

async function getContacts() {
  await axios.get("api/v1/contacts/").then((res) => {
    contacts.value = [];

    for (let i = 0; i < res.data.length; i++) {
      const contact = res.data[i];
      contacts.value.push(contact.name);
    }
  });
}

onMounted(async () => {
  await getContacts();
});
</script>

<template>
  <div>
    <PrimeCard v-if="isLoading" class="p-4">
      <template #content>
        <div class="flex justify-between mb-4">
          <PrimeSkeleton width="9rem" height="3rem" />
          <div class="flex">
            <PrimeSkeleton width="3rem" height="3rem" class="mr-2" />
            <PrimeSkeleton width="20rem" height="3rem" />
          </div>
        </div>

        <PrimeDataTable
          :value="skProducts"
          responsiveLayout="scroll"
          paginatorTemplate="FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
          currentPageReportTemplate="({last} sur {totalRecords})"
          class="cursor-pointer h-[60vh] p-datatable-sm"
          scrollHeight="50vh"
          :rowHover="true"
          :scrollable="true"
          filterDisplay="menu"
        >
          <PrimeColumn
            :exportable="false"
            :sortable="true"
            field="name"
            header="Article"
            style="min-width: 15rem"
            class="text-sm truncate"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            :exportable="false"
            :sortable="true"
            field="category"
            header="Catégorie"
            style="flex: 0 0 14rem"
            class="text-sm truncate"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            :exportable="false"
            :sortable="true"
            field="providers"
            header="Fournisseur"
            style="flex: 0 0 14rem"
            class="text-sm truncate"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            :exportable="false"
            :sortable="true"
            field="real_quantity"
            header="En Stock"
            style="flex: 0 0 14rem"
            class="text-sm truncate"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            :exportable="false"
            :sortable="true"
            field="uom"
            header="Unité"
            style="flex: 0 0 14rem"
            class="text-sm truncate"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            :exportable="true"
            :sortable="true"
            field="unit"
            header="Unité"
            style="flex: 0 0 14rem"
            class="text-sm truncate"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            :exportable="false"
            :sortable="true"
            field="unit_cost"
            header="Cout d'achat"
            style="flex: 0 0 14rem"
            class="text-sm truncate"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            :exportable="false"
            :sortable="true"
            field="unit_price"
            header="Prix de vente"
            style="flex: 0 0 14rem"
            class="text-sm truncate"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            :exportable="false"
            :sortable="true"
            field="created_at"
            header="Créer"
            style="flex: 0 0 14rem"
            class="text-sm truncate"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            :exportable="false"
            :sortable="true"
            field="modified_at"
            header="Modifier"
            style="flex: 0 0 14rem"
            class="text-sm truncate"
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
          :rows="50"
          scrollable
          dataKey="id"
          removableSort
          :rowHover="true"
          :value="products"
          :paginator="true"
          scrollHeight="60vh"
          sortMode="multiple"
          filterDisplay="row"
          exportFilename="Stock"
          :selectAll="selectAll"
          stateStorage="session"
          stateKey="products-state"
          v-model:filters="filters"
          responsiveLayout="scroll"
          @row-select="onRowSelect"
          @row-unselect="onRowUnselect"
          v-model:selection="selectedArticles"
          @select-all-change="onSelectAllChange"
          @row-click="goToSingleProduct($event.data.id)"
          currentPageReportTemplate="({last} sur {totalRecords})"
          :globalFilterFields="['code', 'name', 'get_category', 'providers']"
          paginatorTemplate="FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
          class="cursor-pointer h-[72vh] p-datatable-sm"
        >
          <template #header>
            <div class="flex justify-between items-center">
              <PrimeButton
                label="Créer"
                class="p-button-info mr-4 p-button-sm"
                @click="goToCreatePage"
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

          <template #empty> Aucun produits trouvé. </template>

          <template #loading>
            Chargement des produits. Veillez patienter.
          </template>

          <PrimeColumn
            :exportable="false"
            selectionMode="multiple"
            headerStyle="width: 2rem"
          ></PrimeColumn>

          <PrimeColumn
            :sortable="true"
            field="name"
            style="min-width: 15rem"
            header="Article"
            class="text-sm truncate"
          >
            <template #body="{ data }">
              {{ data.name }}
            </template>

            <template #filter="{ filterModel, filterCallback }">
              <PrimeInputText
                type="text"
                v-model="filterModel.value"
                @keydown.enter="filterCallback()"
                class="p-column-filter"
                :placeholder="`Chercher par nom - `"
                v-tooltip.top.focus="'Appuyer sur une touche pour filter'"
              />
            </template>
          </PrimeColumn>

          <PrimeColumn
            :sortable="true"
            field="get_category"
            header="Catégorie"
            filterMatchMode="starts_with"
            style="flex: 0 0 14rem"
            class="text-sm truncate text-center"
          >
            <template #filter="{ filterModel }">
              <PrimeInputText
                type="text"
                v-model="filterModel.value"
                class="p-column-filter"
                style="flex: 0 0 14rem"
                placeholder="Chercher par catégorie"
              />
            </template>
          </PrimeColumn>

          <PrimeColumn
            :sortable="true"
            field="providers"
            header="Fournisseurs"
            filterMatchMode="starts_with"
            style="flex: 0 0 14rem"
            class="text-sm truncate text-center"
          >
            <template #filter="{ filterModel, filterCallback }">
              <PrimeDropdown
                v-model="filterModel.value"
                @change="filterCallback()"
                :options="providers"
                placeholder="Tout"
                inputClass="w-full"
                class="p-column-filter"
              >
                <template #value="slotProps">
                  <span
                    :class="'customer-badge status-' + slotProps.value"
                    v-if="slotProps.value"
                    >{{ slotProps.value }}</span
                  >
                  <span v-else>{{ slotProps.placeholder }}</span>
                </template>
                <template #option="slotProps">
                  <span :class="'customer-badge status-' + slotProps.option">{{
                    slotProps.option
                  }}</span>
                </template>
              </PrimeDropdown>
            </template>
          </PrimeColumn>

          <PrimeColumn
            :exportable="false"
            :sortable="true"
            field="isAlert"
            header="Alerte"
            dataType="boolean"
            style="min-width: 6rem"
          >
            <template #body="{ data }">
              <i
                class="pi"
                :class="{
                  'text-red-600 pi-times-circle': data.isAlert,
                  'text-emerald-600 pi-check-circle': !data.isAlert,
                }"
              ></i>
            </template>
            <template #filter="{ filterModel, filterCallback }">
              <TriStateCheckbox
                v-model="filterModel.value"
                @change="filterCallback()"
              />
            </template>
          </PrimeColumn>

          <PrimeColumn
            :sortable="true"
            field="real_quantity"
            header="En Stock"
            dataType="numeric"
            class="text-sm truncate text-right"
            style="flex: 0 0 14rem"
          >
            <template #body="{ data }">
              {{ data.real_quantity.toLocaleString() }} {{ data.uom }}
            </template>
            <template #filter="{ filterModel }">
              <PrimeInputNumber v-model="filterModel.value" />
            </template>
          </PrimeColumn>

          <PrimeColumn
            field="uom"
            header="Unité"
            :hidden="true"
            dataType="string"
            class="text-sm truncate text-right"
            style="flex: 0 0 14rem"
          >
            <template #body="{ data }">
              {{ data.uom }}
            </template>
            <template #filter="{ filterModel }">
              <PrimeInputNumber v-model="filterModel.value" />
            </template>
          </PrimeColumn>

          <PrimeColumn
            :exportable="false"
            :sortable="true"
            field="unit_cost"
            header="Cout d'achat"
            dataType="numeric"
            style="flex: 0 0 14rem"
            class="text-sm truncate text-right"
          >
            <template #body="{ data }">
              {{ formatCurrency(data.unit_cost) }}
            </template>

            <template #filter="{ filterModel, filterCallback }">
              <PrimeCalendar
                v-model="filterModel.value"
                @change="filterCallback()"
                placeholder="Date"
                inputClass="w-full"
                dateFormat="dd/mm/yy"
                class="p-column-filter"
              >
                <template #value="slotProps">
                  <span
                    :class="'customer-badge status-' + slotProps.value"
                    v-if="slotProps.value"
                    >{{ slotProps.value }}</span
                  >
                  <span v-else>{{ slotProps.placeholder }}</span>
                </template>

                <template #option="slotProps">
                  <span :class="'customer-badge status-' + slotProps.option">{{
                    slotProps.option
                  }}</span>
                </template>
              </PrimeCalendar>
            </template>
          </PrimeColumn>

          <PrimeColumn
            :exportable="false"
            :sortable="true"
            field="unit_price"
            header="Prix de vente"
            dataType="numeric"
            style="flex: 0 0 14rem"
            class="text-sm truncate"
          >
            <template #body="{ data }">
              {{ formatCurrency(data.unit_price) }}
            </template>
            <template #filter="{ filterModel }">
              <PrimeInputNumber v-model="filterModel.value" />
            </template>
          </PrimeColumn>

          <PrimeColumn
            :exportable="false"
            field="created_at"
            header="Créer"
            dataType="date"
            :sortable="true"
            style="flex: 0 0 14rem"
            class="text-sm truncate"
          >
            <template #body="{ data }">
              {{ formatDate(data.created_at) }}
            </template>

            <template #filter="{ filterModel, filterCallback }">
              <PrimeCalendar
                v-model="filterModel.value"
                @change="filterCallback()"
                placeholder="Tout"
                inputClass="w-full"
                class="p-column-filter"
              >
                <template #value="slotProps">
                  <span
                    :class="'customer-badge status-' + slotProps.value"
                    v-if="slotProps.value"
                    >{{ slotProps.value }}</span
                  >
                  <span v-else>{{ slotProps.placeholder }}</span>
                </template>

                <template #option="slotProps">
                  <span :class="'customer-badge status-' + slotProps.option">{{
                    slotProps.option
                  }}</span>
                </template>
              </PrimeCalendar>
            </template>
          </PrimeColumn>

          <PrimeColumn
            :exportable="false"
            field="modified_at"
            header="Modifier"
            dataType="date"
            :sortable="true"
            style="flex: 0 0 14rem"
            class="text-sm truncate"
          >
            <template #body="{ data }">
              {{ formatDate(data.modified_at) }}
            </template>
            <template #filter="{ filterModel }">
              <PrimeCalendar
                v-model="filterModel.value"
                dateFormat="dd/mm/yy"
                placeholder="dd/mm/yyyy"
              />
            </template>
          </PrimeColumn>
        </PrimeDataTable>
      </template>
    </PrimeCard>
  </div>
</template>
