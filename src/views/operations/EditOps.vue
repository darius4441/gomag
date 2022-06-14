<script setup>
import { RefreshIcon, XIcon } from "@heroicons/vue/solid";
import { toFormValidator } from "@vee-validate/zod";
import axios from "axios";
import { useToast } from "primevue/usetoast";
import { useFieldArray, useForm } from "vee-validate";
import { onMounted, ref } from "vue-demi";
import { useRouter } from "vue-router";
import * as zod from "zod";
import NestedArray from "../../components/operations/creation-item-form.vue";
import Card from "../../components/shared/card-component.vue";
import MyInput from "../../components/shared/forms/BaseInput.vue";
import MyButton from "../../components/shared/my-action.vue";
import { useTempStore } from "../../stores/temp";

// init utils composables to variables
const pageStore = useTempStore();
const router = useRouter();
const toast = useToast();

// Define vars / const
const isLoading = ref(false);
const operation = JSON.parse(localStorage.getItem("vueUseOperation"));
const products = JSON.parse(localStorage.getItem("vueUseProducts"));

operation.items.forEach((el) => {
  const elCopy = el;
  let newArticle = {};

  products.forEach((item) => {
    if (item.id == elCopy.article) {
      newArticle = item;
      return;
    }
  });

  delete el.get_article_available_qty;
  delete el.get_article_name;

  el.article = newArticle;
});

const typeList = ref([
  {
    value: "out",
    label: "Sortie",
  },
  {
    value: "in",
    label: "Entrée",
  },
  {
    value: "return",
    label: "Retour de commande",
  },
]);

const contactOptions = ref([]);

const validationSchema = toFormValidator(
  zod.object({
    contact: zod.number({
      required_error: "contact est obligatoire",
    }),
    m_type: zod.string({
      required_error: "obligatoire",
    }),
    date: zod.string({
      required_error: "obligatoire",
    }),
    items: zod
      .object({
        article: zod.object({
          id: zod.number(),
          name: zod.string({
            required_error: "obligatoire",
          }),
          prod_type: zod.string({
            required_error: "obligatoire",
          }),
          category: zod.nullable(zod.number()),
          code: zod.nullable(zod.string()),
          description: zod.nullable(zod.string()),
          uom: zod.string({
            required_error: "obligatoire",
          }),
          alert_stock: zod.number(),
          optimal_stock: zod.number(),
          real_quantity: zod.number({
            required_error: "obligatoire",
          }),
          virtual_quantity: zod.number({
            required_error: "obligatoire",
          }),
          unit_price: zod.number({
            required_error: "obligatoire",
          }),
          unit_cost: zod.number({
            required_error: "obligatoire",
          }),
          created_at: zod.string({
            required_error: "obligatoire",
          }),
          created_by: zod.number(),
          modified_at: zod.string({
            required_error: "obligatoire",
          }),
          modified_by: zod.number(),
          getUom: zod.string({
            required_error: "obligatoire",
          }),
        }),
        quantity: zod
          .number({
            required_error: "champ obligatoire",
            invalid_type_error: "la quantité doit etre un nombre réel positif",
          })
          .gte(1),
      })
      .array()
      .nonempty({
        message: "Can't be empty!",
      }),
  })
);

// Create a form context with the validation schema
const { handleSubmit } = useForm({
  validationSchema: validationSchema,

  initialValues: {
    contact: operation.contact,
    m_type: operation.m_type,
    date: operation.date,
    items: operation.items,
  },
});

// define array fields
const { remove, push, fields } = useFieldArray("items");

// define functions
const addItemWatcher = handleSubmit(() => {
  push({ article: {}, quantity: 1, unit: "pcs" });
}, onInvalidSubmit);

function addItem() {
  fields.value.length == 0
    ? push({
        article: {},
        quantity: 1,
        unit: "pcs",
      })
    : addItemWatcher();
}

// define functions
async function getContact() {
  await axios
    .get("/api/v1/contacts")
    .then((response) => {
      for (let i = 0; i < response.data.length; i++) {
        const element = {
          value: response.data[i].id,
          label: response.data[i].name,
        };
        contactOptions.value.push(element);
      }
    })
    .catch((error) => {
      toast.add({
        severity: "error",
        summary: "Une erreur s'est produite",
        detail: JSON.stringify(error),
        life: 3000,
      });
    });
}

function onInvalidSubmit({ errors }) {
  let i = 1;
  Object.entries(errors).forEach((item) => {
    if (item[0].includes("items")) {
      if (i != 0) {
        i--;

        toast.add({
          severity: "error",
          summary: "Donnée invalide",
          detail:
            "Veillez ajouter un article avec une quantité de 1 au minimum",

          life: 3000,
        });
      }
    } else {
      toast.add({
        severity: "error",
        summary: "Donnée invalide",
        detail: `Le champs ${item[0]} est ${item[1]}`,
        life: 3000,
      });
    }
  });
}

const onSubmit = handleSubmit(async (values) => {
  isLoading.value = true;

  values.items.forEach((el) => {
    const article = el.article;

    delete el.article;
    el.article = article.id;
    el.unit = article.uom;
  });

  await axios
    .put(`/api/v1/operations/${operation.id}/`, values)
    .then(() => {
      toast.add({
        severity: "error",
        summary: "Donnée invalide",
        detail: `La facture dpt1/${operation.m_type}${operation.id} a été modifié avec succès`,
        life: 3000,
      });

      router.push({ name: "SingleOps", params: { id: operation.id } });
    })
    .catch((error) => {
      toast.add({
        severity: "error",
        summary: "Une erreur s'est produite",
        detail: JSON.stringify(error.message),
        life: 3000,
      });
    });

  isLoading.value = false;
}, onInvalidSubmit);

onMounted(async () => {
  pageStore.updatePageName("Entrées - Sorties");

  await getContact();
});
</script>

<template>
  <div>
    <!-- Header -->
    <div class="mx-auto w-full px-4">
      <div class="flex w-full flex-row items-center">
        <div>
          <button
            v-if="isLoading"
            class="mb-1 rounded bg-kPrimaryColor px-8 py-2 text-xs font-bold uppercase text-kWhiteColor shadow outline-none ring-1 ring-kPrimaryColor transition-all duration-150 ease-linear hover:bg-kSecondaryColor hover:shadow-md focus:outline-none sm:mr-2"
          >
            <RefreshIcon class="h-4 w-4 animate-spin" />
          </button>
          <MyButton v-else label="Sauver" @click="onSubmit" />
        </div>

        <MyButton
          label="Retour"
          to="SingleOps"
          :params="String(operation.id)"
          :isOutlined="true"
        />
      </div>
    </div>

    <Card>
      <template #title>
        <h1>
          Modification de l'opération
          <span class="underline"
            >dpt1/{{ operation.m_type }}{{ operation.id }}</span
          >
        </h1>
      </template>
      <template #content>
        <div class="block w-full overflow-x-auto p-4">
          <!-- Edit  form -->
          <form>
            <div class="flex flex-col">
              <!-- order main info -->
              <div
                class="mx-auto flex flex-row justify-between gap-4 rounded-lg border-2 border-kPrimaryColor p-4 py-4 dark:border-kWhiteColor"
              >
                <MyInput
                  type="select"
                  name="contact"
                  :options="contactOptions"
                />

                <MyInput type="select" name="m_type" :options="typeList" />

                <MyInput type="date" name="date" :todayShortcut="true" />
              </div>

              <!-- order items info -->

              <div
                class="my-4 h-80 gap-y-4 space-y-2 overflow-y-auto rounded-lg border-2 border-kPrimaryColor p-4 dark:border-kWhiteColor"
              >
                <table class="relative w-full table-fixed">
                  <thead>
                    <tr>
                      <th
                        class="sticky top-0 w-1/12 whitespace-nowrap bg-kWhiteColor p-3 text-right align-middle text-xs font-semibold dark:bg-kDarkColor"
                      >
                        N°
                      </th>
                      <th
                        class="sticky top-0 whitespace-nowrap bg-kWhiteColor p-3 text-left align-middle text-xs font-semibold dark:bg-kDarkColor"
                      >
                        Article
                      </th>
                      <th
                        class="sticky top-0 w-2/12 whitespace-nowrap bg-kWhiteColor p-3 text-right align-middle text-xs font-semibold dark:bg-kDarkColor"
                      >
                        Quantité
                      </th>
                      <th
                        class="sticky top-0 w-2/12 whitespace-nowrap bg-kWhiteColor p-3 align-middle text-xs font-semibold dark:bg-kDarkColor"
                      >
                        Unité
                      </th>
                      <th
                        class="sticky top-0 w-1/12 whitespace-nowrap bg-kWhiteColor p-3 align-middle text-xs font-semibold dark:bg-kDarkColor"
                      ></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="(item, idx) in fields"
                      :key="item.key"
                      class="rounded-lg focus-within:border-b-2 focus-within:border-kPrimaryColor hover:border-b"
                    >
                      <NestedArray :idx="idx" @addItem="addItem" />
                      <td
                        class="w-1/12 whitespace-nowrap py-1 px-1.5 text-center align-middle text-xs"
                      >
                        <div
                          @click="remove(idx)"
                          class="cursor-pointer rounded-full py-1 px-1.5 text-red-600 hover:bg-red-600 hover:text-white"
                        >
                          <XIcon class="mx-auto h-5 w-5" />
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <button
                  type="button"
                  @click="addItem"
                  class="mt-1 w-32 rounded-lg px-3 py-1 text-xs underline hover:bg-kPrimaryColor hover:text-white dark:text-kWhiteColor/50 dark:hover:text-kWhiteColor"
                >
                  Ajouter une ligne
                </button>
              </div>
            </div>
          </form>
        </div>
      </template>
    </Card>
  </div>
</template>
