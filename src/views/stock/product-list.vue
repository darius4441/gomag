<script setup>
import { FilterMatchMode, FilterOperator } from "primevue/api";
import { ref } from "vue-demi";
import { useRouter } from "vue-router";
import { useProducts } from "../../composables";

const router = useRouter();
const { products, isLoading } = useProducts();

const dt = ref();
const selectedArticles = ref();
const skProducts = ref(new Array(50));

function goToCreatePage() {
  router.push({ name: "CreateProduct" });
}

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
  created_at: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }],
  },
  created_by: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }],
  },
  modified_at: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.DATE_IS }],
  },
  modified_by: {
    operator: FilterOperator.AND,
    constraints: [{ value: null, matchMode: FilterMatchMode.EQUALS }],
  },
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
          <PrimeColumn field="name" header="Article" class="text-sm truncate">
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            field="category"
            header="Catégorie"
            style="flex: 0 0 9rem"
            class="text-sm truncate"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            field="providers"
            header="Fournisseur"
            style="flex: 0 0 9rem"
            class="text-sm truncate"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            field="real_quantity"
            header="En Stock"
            style="flex: 0 0 9rem"
            class="text-sm truncate"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            field="unit"
            header="Unité"
            style="flex: 0 0 9rem"
            class="text-sm truncate"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            field="unit_cost"
            header="Cout d'achat"
            style="flex: 0 0 9rem"
            class="text-sm truncate"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            field="unit_price"
            header="Prix de vente"
            style="flex: 0 0 9rem"
            class="text-sm truncate"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            field="created_at"
            header="Créer"
            style="flex: 0 0 9rem"
            class="text-sm truncate"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>

          <PrimeColumn
            field="modified_at"
            header="Modifier"
            style="flex: 0 0 9rem"
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
          :rowHover="true"
          :value="products"
          :paginator="true"
          scrollHeight="60vh"
          filterDisplay="menu"
          v-model:filters="filters"
          v-model:selection="selectedArticles"
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

          <!-- <PrimeColumn selectionMode="multiple" headerStyle="width: 2rem"></PrimeColumn> -->

          <PrimeColumn field="name" header="Article" class="text-sm truncate">
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
          </PrimeColumn>

          <PrimeColumn
            field="get_category"
            header="Catégorie"
            filterMatchMode="starts_with"
            style="flex: 0 0 9rem"
            class="text-sm truncate text-center"
          >
            <template #filter="{ filterModel }">
              <PrimeInputText
                type="text"
                v-model="filterModel.value"
                class="p-column-filter"
                style="flex: 0 0 9rem"
                placeholder="Chercher par catégorie"
              />
            </template>
          </PrimeColumn>

          <PrimeColumn
            field="providers"
            header="Fournisseurs"
            filterMatchMode="starts_with"
            style="flex: 0 0 9rem"
            class="text-sm truncate text-center"
          >
            <template #filter="{ filterModel }">
              <PrimeInputText
                type="text"
                v-model="filterModel.value"
                class="p-column-filter"
                placeholder="Chercher par fournisseur"
              />
            </template>
          </PrimeColumn>

          <PrimeColumn
            field="real_quantity"
            header="En Stock"
            dataType="numeric"
            class="text-sm truncate text-right"
            style="flex: 0 0 9rem"
          >
            <template #body="{ data }">
              {{ data.real_quantity.toLocaleString() }}
            </template>
            <template #filter="{ filterModel }">
              <PrimeInputNumber v-model="filterModel.value" />
            </template>
          </PrimeColumn>

          <PrimeColumn
            field="uom"
            header="Unité"
            class="text-sm truncate text-center"
            style="flex: 0 0 9rem"
          >
            <template #filter="{ filterModel }">
              <PrimeInputText
                type="text"
                v-model="filterModel.value"
                class="p-column-filter"
                placeholder="Chercher par unité"
              />
            </template>
          </PrimeColumn>

          <PrimeColumn
            field="unit_cost"
            header="Cout d'achat"
            dataType="numeric"
            style="flex: 0 0 9rem"
            class="text-sm truncate text-right"
          >
            <template #body="{ data }">
              {{ formatCurrency(data.unit_cost) }}
            </template>
            <template #filter="{ filterModel }">
              <PrimeInputNumber v-model="filterModel.value" />
            </template>
          </PrimeColumn>

          <PrimeColumn
            field="unit_price"
            header="Prix de vente"
            dataType="numeric"
            style="flex: 0 0 9rem"
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
            field="created_at"
            header="Créer"
            dataType="date"
            :sortable="true"
            style="flex: 0 0 9rem"
            class="text-sm truncate"
          >
            <template #body="{ data }">
              {{ formatDate(data.created_at) }}
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
            field="modified_at"
            header="Modifier"
            dataType="date"
            :sortable="true"
            style="flex: 0 0 9rem"
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
