useProducts
<script setup>
import moment from "moment/min/moment-with-locales";
import { FilterMatchMode, FilterOperator } from "primevue/api";
import Calendar from "primevue/calendar";
import Column from "primevue/column";
import DataTable from "primevue/datatable";
import InputNumber from "primevue/inputnumber";
import { ref } from "vue-demi";
import { useRouter } from "vue-router";
import { useProducts } from "../../composables";

moment.locale("fr");

const router = useRouter();

const { products, isLoading } = useProducts();
const dt = ref();
const selectedArticles = ref();

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  code: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }],
  },
  name: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.CONTAINS }],
  },
  get_category: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }],
  },
  providers: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }],
  },
  real_quantity: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }],
  },
  uom: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.STARTS_WITH }],
  },
  unit_cost: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }],
  },
  unit_price: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }],
  },
  modified_at: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }],
  },
  created_by: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }],
  },
  modified_by: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }],
  },
});

const timePast = (date) => {
  let newDate = moment(date).startOf("day").fromNow();

  return newDate;
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
</script>

<template>
  <div>
    <DataTable
      ref="dt"
      :value="products"
      :paginator="true"
      scrollable
      :rows="50"
      dataKey="id"
      :rowHover="true"
      v-model:selection="selectedArticles"
      filterDisplay="menu"
      v-model:filters="filters"
      :loading="isLoading"
      @row-click="goToSingleProduct($event.data.id)"
      paginatorTemplate="FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
      currentPageReportTemplate="({last} sur {totalRecords})"
      :globalFilterFields="['code', 'name', 'get_category', 'providers']"
      class="cursor-pointer"
      scrollHeight="68vh"
    >
      <template #header>
        <div class="flex justify-between items-center">
          <PrimeButton
            label="Créer"
            icon="pi pi-plus"
            class="p-button-success"
          />
          <div>
            <PrimeButton
              icon="pi pi-upload"
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

      <!-- <Column selectionMode="multiple" headerStyle="width: 2rem"></Column> -->

      <Column field="name" header="Article" class="text-sm truncate w-3/12">
        <template #body="{ data }">
          {{ data.name }}
        </template>

        <template #filter="{ filterModel }">
          <PrimeInputText
            type="text"
            v-model="filterModel.value"
            class="p-column-filter"
            placeholder="Chercher par nom"
          />
        </template>
      </Column>

      <Column
        field="get_category"
        header="Catégorie"
        filterMatchMode="starts_with"
        class="text-sm truncate w-1/12 text-center"
      >
        <template #filter="{ filterModel }">
          <PrimeInputText
            type="text"
            v-model="filterModel.value"
            class="p-column-filter"
            placeholder="Chercher par catégorie"
          />
        </template>
      </Column>

      <Column
        field="providers"
        header="Fournisseurs"
        filterMatchMode="starts_with"
        class="text-sm truncate w-1/12 text-center"
      >
        <template #filter="{ filterModel }">
          <PrimeInputText
            type="text"
            v-model="filterModel.value"
            class="p-column-filter"
            placeholder="Chercher par fournisseur"
          />
        </template>
      </Column>

      <Column
        field="real_quantity"
        header="En Stock"
        dataType="numeric"
        class="text-sm truncate w-1/12 text-right"
      >
        <template #body="{ data }">
          {{ data.real_quantity.toLocaleString() }}
        </template>
        <template #filter="{ filterModel }">
          <InputNumber v-model="filterModel.value" />
        </template>
      </Column>

      <Column
        field="uom"
        header="Unité"
        class="text-sm truncate w-1/12 text-center"
      >
        <template #filter="{ filterModel }">
          <PrimeInputText
            type="text"
            v-model="filterModel.value"
            class="p-column-filter"
            placeholder="Chercher par unité   "
          />
        </template>
      </Column>

      <Column
        field="unit_cost"
        header="Cout d'achat"
        dataType="numeric"
        class="text-sm truncate w-1/12 text-right"
      >
        <template #body="{ data }">
          {{ formatCurrency(data.unit_cost) }}
        </template>
        <template #filter="{ filterModel }">
          <InputNumber v-model="filterModel.value" />
        </template>
      </Column>

      <Column
        field="unit_price"
        header="Prix de vente"
        dataType="numeric"
        class="text-sm truncate w-1/12"
      >
        <template #body="{ data }">
          {{ formatCurrency(data.unit_price) }}
        </template>
        <template #filter="{ filterModel }">
          <InputNumber v-model="filterModel.value" />
        </template>
      </Column>

      <Column
        field="created_at"
        header="Créer"
        dataType="date"
        :sortable="true"
        class="text-sm truncate w-1/12"
      >
        <template #body="{ data }">
          {{ timePast(data.created_at) }}
        </template>
        <template #filter="{ filterModel }">
          <Calendar
            v-model="filterModel.value"
            dateFormat="dd/mm/yy"
            placeholder="dd/mm/yyyy"
          />
        </template>
      </Column>

      <Column
        field="modified_at"
        header="Modifier"
        dataType="date"
        :sortable="true"
        class="text-sm truncate w-1/12"
      >
        <template #body="{ data }">
          {{ timePast(data.modified_at) }}
        </template>
        <template #filter="{ filterModel }">
          <Calendar
            v-model="filterModel.value"
            dateFormat="dd/mm/yy"
            placeholder="dd/mm/yyyy"
          />
        </template>
      </Column>
    </DataTable>
  </div>
</template>
