<script setup>
import { toFormValidator } from "@vee-validate/zod";
import axios from "axios";
import { useForm } from "vee-validate";
import { onMounted, ref } from "vue-demi";
import { useRouter } from "vue-router";
import { useToast } from "vue-toast-notification";
import * as zod from "zod";
import Card from "../../components/shared/card-component.vue";
import MyInput from "../../components/shared/forms/BaseInput.vue";
import MyButton from "../../components/shared/my-action.vue";
import { useTempStore } from "../../stores/temp";

// init utils composables to variables
const pageStore = useTempStore();
const router = useRouter();
const toast = useToast();

// Define vars / const
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

function onInvalidSubmit({ errors }) {
  Object.entries(errors).forEach((item) => {
    toast.error("Le champ " + item[1], {
      position: "top-right",
    });
  });
}

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

// auto call by node when submitForm was called
const onSubmit = handleSubmit(async (values) => {
  try {
    await axios
      .post("/api/v1/stock/products/", values)
      .then((res) => {
        resetForm();

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
        <MyButton label="Sauver" @click="onSubmit" />
        <MyButton label="Annuler" to="Products" :isOutlined="true" />
      </div>
    </div>

    <Card>
      <template #title>
        <h3 class="text-sm">Nouvel article</h3>
      </template>

      <template #content>
        <form class="py-6">
          <div class="flex flex-col gap-y-4">
            <MyInput type="text" name="name" label="Nom de l'article" />
            <div class="flex flex-row gap-x-4">
              <div class="flex w-full flex-col gap-y-4">
                <MyInput
                  type="select"
                  name="category"
                  label="Catégorie"
                  :options="categories"
                />

                <MyInput type="text" name="providers" label="Fournisseur" />

                <MyInput type="text" name="code" label="Code" />
              </div>

              <div class="flex w-full flex-col gap-y-4">
                <MyInput
                  type="select"
                  name="uom"
                  label="Unité de mesure"
                  :options="uomList"
                />
                <div class="flex flex-row gap-x-4">
                  <MyInput
                    type="number"
                    name="unit_cost"
                    label="Cout d'achat"
                  />

                  <MyInput
                    type="number"
                    name="unit_price"
                    label="Prix de vente"
                  />
                </div>

                <div class="flex flex-row gap-x-4">
                  <MyInput
                    type="number"
                    name="alert_stock"
                    label="Stock alerte"
                  />

                  <MyInput
                    type="number"
                    name="optimal_stock"
                    label="Stock idéal"
                  />
                </div>
              </div>
            </div>

            <MyInput type="textarea" name="description" label="Description" />
          </div>
        </form>
      </template>
    </Card>
  </div>
</template>
