<script setup>
import axios from "axios";
import { reset } from "@formkit/core";
import { onMounted, ref } from "vue-demi";
import { useRouter } from "vue-router";
import { useToast } from "vue-toast-notification";
import Card from "../../components/shared/card-component.vue";
import MyButton from "../../components/shared/my-action.vue";
import { useTempStore } from "../../stores/temp";

// init utils composables to variables
const pageStore = useTempStore();
const router = useRouter();
const toast = useToast();

// Define vars / const
const productFormDataRef = ref(null);
const productFormData = ref({});
const categories = ref([]);

const uomList = ref([
  { label: "pcs", value: "pcs" },
  { label: "m", value: "m" },
  { label: "kg", value: "kg" },
  { label: "barre", value: "barre" },
  { label: "pot", value: "pot" },
  { label: "crt", value: "crt" },
  { label: "pqt", value: "pqt" },
  { label: "feuille", value: "feuille" },
  { label: "colie", value: "colie" },
  { label: "paire", value: "paire" },
  { label: "rlx", value: "rlx" },
  { label: "sac", value: "sac" },
]);

function submitForm() {
  const node = productFormDataRef.value.node;

  node.submit();
}

async function submitHandler() {
  try {
    await axios
      .post("/api/v1/stock/products/", productFormData.value)
      .then((res) => {
        reset("productFormData");

        toast.success("Article créer avec succes", {
          position: "top-right",
        });

        router.push({
          name: "SingleProduct",
          params: { id: res.data.id },
        });
      })
      .catch((e) => {
        throw e;
      });
  } catch (error) {
    toast.error(error.message, {
      position: "top-right",
    });
  }
}

async function getCategories() {
  try {
    await axios
      .get("/api/v1/stock/categories")
      .then((response) => {
        categories.value = [];

        for (let i = 0; i < response.data.length; i++) {
          const cat = response.data[i];
          categories.value.push({ label: cat.name, value: cat.id });
        }
      })
      .catch((e) => {
        throw e;
      });
  } catch (error) {
    toast.error(error.message, {
      position: "top-right",
    });
  }
}

onMounted(async () => {
  pageStore.updatePageName("Stock");

  await getCategories();
});
</script>

<template>
  <div>
    <!-- Header -->
    <div class="mx-auto w-full px-4">
      <div class="flex w-full flex-row items-center">
        <MyButton label="Sauver" @click="submitForm" />
        <MyButton label="Annuler" to="Products" :isOutlined="true" />
      </div>
    </div>

    <Card>
      <template #title>
        <h3 class="text-sm">Nouvel article</h3>
      </template>

      <template #content>
        <FormKit
          type="form"
          ref="productFormDataRef"
          v-model="productFormData"
          :actions="false"
          @submit="submitHandler"
          class="py-3"
        >
          <div class="flex flex-col">
            <FormKit
              type="text"
              name="name"
              validation="required|length:3"
              label="Nom de l'article"
            />
            <div class="flex flex-row gap-x-4">
              <div class="flex w-full flex-col">
                <FormKit
                  type="select"
                  name="category"
                  label="Catégorie"
                  :options="categories"
                />

                <FormKit type="text" name="providers" label="Fournisseur" />

                <FormKit type="text" name="code" label="Code" />
              </div>

              <div class="flex w-full flex-col">
                <FormKit
                  type="select"
                  name="uom"
                  label="Unité de mesure"
                  :options="uomList"
                  validation="required"
                />
                <div class="flex flex-row gap-x-4">
                  <FormKit
                    type="number"
                    name="unit_cost"
                    label="Cout d'achat"
                    value="1"
                    validation="required|number|min:0"
                  />

                  <FormKit
                    type="number"
                    name="unit_price"
                    label="Prix de vente"
                    value="1"
                    validation="required|number|min:0"
                  />
                </div>

                <div class="flex flex-row gap-x-4">
                  <FormKit
                    type="number"
                    name="alert_stock"
                    label="Stock alerte"
                    value="1"
                    validation="required|number|min:0"
                  />

                  <FormKit
                    type="number"
                    name="optimal_stock"
                    label="Stock idéal"
                    value="1"
                    validation="required|number|min:0"
                  />
                </div>
              </div>
            </div>

            <FormKit type="textarea" name="description" label="Description" />
          </div>
        </FormKit>
      </template>
    </Card>
  </div>
</template>
