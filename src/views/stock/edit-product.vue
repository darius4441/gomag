<script setup>
import { ref, onMounted } from "vue-demi";
import { useTempStore } from "../../stores/temp";
import { useRouter } from "vue-router";

import axios from "axios";
import * as zod from "zod";
import { toFormValidator } from "@vee-validate/zod";
import { useForm } from "vee-validate";
import { useToast } from "vue-toast-notification";

import MyButton from "../../components/shared/my-action.vue";
import MyInput from "../../components/shared/forms/BaseInput.vue";
import Card from "../../components/shared/card-component.vue";

// init utils composables to variables
const pageStore = useTempStore();
const router = useRouter();
const toast = useToast();

const product = JSON.parse(localStorage.getItem("vueUseProduct"));

// Define vars / const
const categories = ref([
  { label: "Carrelage", value: "Carrelage" },
  { label: "Divers", value: "Divers" },
  { label: "Electricité", value: "Electricité" },
  { label: "Etanchéité", value: "Etanchéité" },
  { label: "Maçonnerie", value: "Maçonnerie" },
  { label: "Menuiserie", value: "Menuiserie" },
  { label: "Peinture", value: "Peinture" },
  { label: "Plomberie", value: "Plomberie" },
  { label: "Sanitaire", value: "Sanitaire" },
  { label: "Serrure", value: "Serrure" },
  { label: "Tuyauterie", value: "Tuyauterie" },
]);

const uomList = ref([
  { label: "pcs", value: "pcs" },
  { label: "m", value: "m" },
  { label: "kg", value: "kg" },
  { label: "barre", value: "barre" },
  { label: "pot", value: "pot" },
  { label: "crt", value: "crt" },
  { label: "pqt", value: "pqt" },
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
    category: zod.string().nullish(),
    code: zod.string().nullish(),
    description: zod.string().nullish(),
    uom: zod.string({
      required_error: "unité de mesure est obligatoire",
    }),
    provider: zod.string().nullish(),
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

// Define functions

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
    name: product.name,
    category: product.category,
    code: product.code,
    description: product.description,
    uom: product.uom,
    provider: product.provider,
    alert_stock: parseInt(product.alert_stock),
    optimal_stock: parseInt(product.optimal_stock),
    unit_price: parseInt(product.unit_price),
    unit_cost: parseInt(product.unit_cost),
  },
});

// auto call by node when submitForm was called
const onSubmit = handleSubmit(async (values) => {
  try {
    await axios
      .patch(`/api/v1/stock/products/${product.id}/`, values)
      .then(() => {
        resetForm();

        toast.success(`L'article' ${product.name} a été modifié avec succes`, {
          position: "top-right",
        });

        router.push({ name: "SingleProduct", params: { id: product.id } });
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

onMounted(() => {
  pageStore.updatePageName("Stock");
});
</script>

<template>
  <div>
    <!-- Header -->
    <div class="mx-auto w-full px-4">
      <div class="flex w-full flex-row items-center">
        <MyButton label="Sauver" @click="onSubmit" />
        <MyButton
          label="Annuler"
          to="SingleProduct"
          :params="String(product.id)"
          :isOutlined="true"
        />
      </div>
    </div>

    <Card>
      <template #title>
        <h1 class="basis-1/2">
          Modification de l'article
          <span class="underline">{{ product.name }}</span>
        </h1>
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

                <MyInput type="text" name="provider" label="Fournisseur" />

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
