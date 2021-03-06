<script setup>
import { toFormValidator } from "@vee-validate/zod";
import axios from "axios";
import { useToast } from "primevue/usetoast";
import { useField, useForm } from "vee-validate";
import { computed, onMounted, onUnmounted, ref } from "vue-demi";
import { useRouter } from "vue-router";
import * as zod from "zod";
import { useProducts } from "../../composables";
import { useTempStore } from "../../stores/temp";

// init utils composables to variables
const pageStore = useTempStore();
const { refetch } = useProducts();
const router = useRouter();
const toast = useToast();

// Define vars / const
const oldProduct = JSON.parse(localStorage.getItem("vueUseLastProduct"));

const categories = ref([]);
const isLoading = ref(false);
const uomList = ref([
  { label: "pcs", value: "pcs" },
  { label: "m", value: "m" },
  { label: "kg", value: "kg" },
  { label: "barre", value: "barre" },
  { label: "pot", value: "pot" },
  { label: "feuille", value: "feuille" },
  { label: "crt", value: "crt" },
  { label: "pqt", value: "pqt" },
  { label: "rlx", value: "rlx" },
  { label: "sac", value: "sac" },
]);
const breadcrumb = ref({
  home: {
    icon: "pi pi-home",
    to: "/stock/products",
  },
  items: oldProduct
    ? [
        {
          label: computed(() => oldProduct.name),
          to: `/stock/products/${oldProduct.id}`,
        },
        {
          label: "création",
        },
      ]
    : [
        {
          label: "création",
        },
      ],
});

const validationSchema = toFormValidator(
  zod.object({
    name: zod
      .string({
        required_error: "nom de l'article est obligatoire",
      })
      .min(3, { message: "nom de l'article doit avoir 3 charactère minimum" }),
    category: zod.number().nullish(),
    code: zod.string().nullish(),
    description: zod.string().nullish(),
    uom: zod.string({
      required_error: "unité de mesure est obligatoire",
    }),
    providers: zod.string().nullish(),
    alert_stock: zod
      .number({
        required_error: "stock alerte est obligatoire",
        invalid_type_error: "stock alerte doit etre un nombre",
      })
      .gte(0, { message: "stock alerte doit avoir minimum 0" }),
    optimal_stock: zod
      .number({
        required_error: "stock idéal est obligatoire",
        invalid_type_error: "stock idéal doit etre un nombre",
      })
      .gte(0, { message: "stock idéal doit avoir minimum 0" }),
    unit_price: zod
      .number({
        required_error: "prix de vente est obligatoire",
        invalid_type_error: "prix de vente doit etre un nombre",
      })
      .gte(0, { message: "prix de vente doit avoir minimum 0" }),
    unit_cost: zod
      .number({
        required_error: "cout d'achat est obligatoire",
        invalid_type_error: "cout d'achat doit etre un nombre",
      })
      .gte(0, { message: "cout d'achat doit avoir minimum 0" }),
  })
);

// Create a form context with the validation schema
const { handleSubmit, resetForm } = useForm({
  validationSchema: validationSchema,

  initialValues: {
    prod_type: "storable",
    category: 1,
    uom: uomList.value[0].value,
    alert_stock: 0,
    optimal_stock: 0,
    unit_price: 1,
    unit_cost: 1,
  },
});

const { value: name, errorMessage: nameError } = useField("name");
const { value: category, errorMessage: categoryError } = useField("category");
const { value: code, errorMessage: codeError } = useField("code");
const { value: description, errorMessage: descriptionError } =
  useField("description");
const { value: uom, errorMessage: uomError } = useField("uom");
const { value: providers, errorMessage: providersError } =
  useField("providers");
const { value: alert_stock, errorMessage: alert_stockError } =
  useField("alert_stock");
const { value: optimal_stock, errorMessage: optimal_stockError } =
  useField("optimal_stock");
const { value: unit_price, errorMessage: unit_priceError } =
  useField("unit_price");
const { value: unit_cost, errorMessage: unit_costError } =
  useField("unit_cost");

// Define functions
function goToOldPage() {
  const hasOldPage = oldProduct !== null;
  hasOldPage === true
    ? router.push({
        name: "SingleProduct",
        params: { id: oldProduct.id },
      })
    : router.push({ name: "Products" });
}

function onInvalidSubmit({ errors }) {
  Object.entries(errors).forEach((item) => {
    toast.add({
      severity: "error",
      summary: "Donnée invalide",
      detail: "Le champ " + item[1],
      life: 3000,
    });
  });
}

// auto call by node when submitForm was called
const onSubmit = handleSubmit(async () => {
  isLoading.value = true;

  const formData = {
    name: name.value,
    category: category.value,
    code: code.value,
    description: description.value,
    uom: uom.value,
    providers: providers.value,
    alert_stock: alert_stock.value,
    optimal_stock: optimal_stock.value,
    unit_price: unit_price.value,
    unit_cost: unit_cost.value,
  };
  try {
    await axios
      .post("/api/v1/stock/products/", formData)
      .then((res) => {
        refetch.value();

        resetForm();

        toast.add({
          severity: "success",
          summary: "Création",
          detail: "Article créer avec succès",
          life: 3000,
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
    toast.add({
      severity: "error",
      summary: "Une erreur s'est produite",
      detail: JSON.stringify(error.message),
      life: 3000,
    });
  }

  isLoading.value = false;
}, onInvalidSubmit);

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
    toast.add({
      severity: "error",
      summary: "Une erreur s'est produite",
      detail: JSON.stringify(error.message),
      life: 3000,
    });
  }
}

onMounted(async () => {
  pageStore.updatePageName("Stock");

  await getCategories();
});

onUnmounted(async () => {
  localStorage.removeItem("vueUseLastProduct");
});
</script>

<template>
  <div>
    <PrimeToast />

    <!-- Header -->
    <PrimeBreadcrumb :home="breadcrumb.home" :model="breadcrumb.items" />

    <PrimeToolbar p-toolbar="">
      <template #start>
        <PrimeButton v-if="isLoading" class="p-button-info mr-4 p-button-sm">
          <div>
            <i class="pi pi-spinner animate-spin"></i>
            <span class="ml-1.5">Sauver</span>
          </div>
        </PrimeButton>

        <PrimeButton
          v-else
          label="Sauver"
          class="p-button-info mr-4 p-button-sm"
          @click="onSubmit"
        />

        <PrimeButton
          label="Retour"
          @click="goToOldPage"
          class="p-button-info p-button-sm p-button-outlined"
        >
        </PrimeButton>
      </template>
    </PrimeToolbar>

    <PrimeCard>
      <template #title>
        <h3 class="text-sm">Nouvel article</h3>
      </template>

      <template #content>
        <form class="py-6">
          <div class="flex flex-col gap-y-4">
            <span class="p-float-label mt-6 text-md text-slate-700">
              <PrimeInputText
                type="text"
                id="name"
                v-model:model-value="name"
                class="w-full"
                :class="{ 'p-invalid': nameError }"
              />

              <label for="name" class="text-md text-slate-700"
                >Nom de l'article</label
              >
            </span>

            <div class="flex flex-row gap-x-4 my-6">
              <div class="flex w-full flex-col gap-y-4">
                <span class="p-float-label text-md text-slate-700">
                  <PrimeDropdown
                    id="category"
                    v-model="category"
                    :options="categories"
                    optionLabel="label"
                    optionValue="value"
                    class="w-full"
                    :inputClass="[categoryError ? 'p-invalid' : '', 'w-full']"
                  />

                  <label for="category" class="text-md text-slate-700">
                    Catégorie
                  </label>
                </span>

                <span class="p-float-label mt-10 text-md text-slate-700">
                  <PrimeInputText
                    type="text"
                    id="providers"
                    v-model:model-value="providers"
                    class="w-full"
                    :class="{ 'p-invalid': providersError }"
                  />

                  <label for="providers" class="text-md text-slate-700"
                    >Fournisseurs</label
                  >
                </span>

                <span class="p-float-label mt-10 text-md text-slate-700">
                  <PrimeInputText
                    type="text"
                    id="code"
                    v-model:model-value="code"
                    class="w-full"
                    :class="{ 'p-invalid': codeError }"
                  />

                  <label for="code" class="text-md text-slate-700">Code</label>
                </span>
              </div>

              <div class="flex w-full flex-col gap-y-4">
                <span class="p-float-label text-md text-slate-700">
                  <PrimeDropdown
                    id="uom"
                    v-model="uom"
                    :options="uomList"
                    optionLabel="label"
                    optionValue="value"
                    class="w-full"
                    :inputClass="[uomError ? 'p-invalid' : '', 'w-full']"
                  />

                  <label for="uom" class="text-md text-slate-700">
                    Unité de mesure
                  </label>
                </span>

                <div class="flex flex-row gap-x-4">
                  <span class="p-float-label mt-10 text-md text-slate-700">
                    <PrimeInputNumber
                      id="unit_cost"
                      v-model:model-value="unit_cost"
                      class="w-full"
                      :min="0"
                      :class="{ 'p-invalid': unit_costError }"
                    />

                    <label for="unit_cost" class="text-md text-slate-700"
                      >Cout d'achat</label
                    >
                  </span>

                  <span class="p-float-label mt-10 text-md text-slate-700">
                    <PrimeInputNumber
                      id="unit_price"
                      v-model:model-value="unit_price"
                      class="w-full"
                      :min="0"
                      :class="{ 'p-invalid': unit_priceError }"
                    />

                    <label for="unit_price" class="text-md text-slate-700"
                      >Prix de vente</label
                    >
                  </span>
                </div>

                <div class="flex flex-row gap-x-4">
                  <span class="p-float-label mt-10 text-md text-slate-700">
                    <PrimeInputNumber
                      id="alert_stock"
                      v-model:model-value="alert_stock"
                      class="w-full"
                      :min="0"
                      :class="{ 'p-invalid': alert_stockError }"
                    />

                    <label for="alert_stock" class="text-md text-slate-700"
                      >Stock alerte</label
                    >
                  </span>

                  <span class="p-float-label mt-10 text-md text-slate-700">
                    <PrimeInputNumber
                      id="optimal_stock"
                      v-model:model-value="optimal_stock"
                      class="w-full"
                      :min="0"
                      :class="{ 'p-invalid': optimal_stockError }"
                    />

                    <label for="optimal_stock" class="text-md text-slate-700"
                      >Stock idéal</label
                    >
                  </span>
                </div>
              </div>
            </div>

            <PrimeTextarea
              v-model:model-value="description"
              name="description"
              placeholder="Description"
              rows="5"
              cols="30"
              :class="{ 'p-invalid': descriptionError }"
            />
          </div>
        </form>
      </template>
    </PrimeCard>
  </div>
</template>
