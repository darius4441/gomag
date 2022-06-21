<script setup>
import { useRouter } from "vue-router";
import { useProducts } from "../../composables";

const router = useRouter();
const { isLoading, products } = useProducts();

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
  <PrimeCard>
    <template #content>
      <PrimeDataTable
        ref="dt"
        :rows="50"
        :scrollable="true"
        scrollDirection="vertical"
        dataKey="id"
        :rowHover="true"
        :value="products"
        :paginator="true"
        :loading="isLoading"
        scrollHeight="20vh"
        filterDisplay="menu"
        @row-click="goToSingleProduct($event.data.id, true)"
        currentPageReportTemplate="({last} sur {totalRecords})"
        paginatorTemplate="PrevPageLink NextPageLink"
        class="cursor-pointer h-56 p-datatable-sm"
      >
        <template #header>
          <h3>Produits en alerte</h3>
        </template>

        <template #empty> Aucun produits en alerte. </template>

        <template #loading>
          Chargement des produits. Veillez patienter.
        </template>

        <PrimeColumn
          field="name"
          style="min-width: 15rem"
          header="Article"
          class="text-sm truncate"
        />

        <PrimeColumn
          field="alert_stock"
          header="Alerte"
          dataType="numeric"
          class="text-sm truncate text-right"
          style="min-width: 1rem"
        >
          <template #body="{ data }">
            {{ data.alert_stock.toLocaleString() }} {{ data.uom }}
          </template>
        </PrimeColumn>

        <PrimeColumn
          field="real_quantity"
          header="En Stock"
          dataType="numeric"
          class="text-sm truncate text-right"
          style="min-width: 1rem"
        >
          <template #body="{ data }">
            {{ data.real_quantity.toLocaleString() }} {{ data.uom }}
          </template>
        </PrimeColumn>
      </PrimeDataTable>
    </template>
  </PrimeCard>
</template>
