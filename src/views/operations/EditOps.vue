<script setup>
import { PlusCircleIcon, RefreshIcon, XIcon } from "@heroicons/vue/solid";
import { toFormValidator } from "@vee-validate/zod";
import axios from "axios";
import moment from "moment";
import { useToast } from "primevue/usetoast";
import { useField, useFieldArray, useForm } from "vee-validate";
import { onMounted, ref } from "vue-demi";
import { useRouter } from "vue-router";
import * as zod from "zod";
import NestedArray from "../../components/operations/creation-item-form.vue";
import Card from "../../components/shared/card-component.vue";
import MyButton from "../../components/shared/my-action.vue";
import { useTempStore } from "../../stores/temp";

// init utils composables to variables
const pageStore = useTempStore();
const router = useRouter();
const toast = useToast();

const operation = JSON.parse(localStorage.getItem("vueUseOperation"));
const products = JSON.parse(localStorage.getItem("vueUseProducts"));

// Define vars / const
const isLoading = ref(false);
const contactOptions = ref([]);

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

const validationSchema = toFormValidator(
  zod.object({
    contact: zod.number({
      required_error: "contact est obligatoire",
    }),
    m_type: zod.string({
      required_error: "obligatoire",
    }),
    date: zod.date({
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
        unit: zod.string().nullish(),
        cost: zod.number().nullish(),
      })
      .array()
      .nonempty({
        message: "Can't be empty!",
      }),
    unit: zod.string().nullish(),
    cost: zod.number().nullish(),
  })
);

// Create a form context with the validation schema
const { handleSubmit } = useForm({
  validationSchema: validationSchema,

  initialValues: {
    contact: operation.contact,
    m_type: operation.m_type,
    date: new Date(operation.date),
    items: operation.items,
  },
});

const { value: contact, errorMessage: contactError } = useField("contact");
const { value: m_type, errorMessage: m_typeError } = useField("m_type");
const { value: date, errorMessage: dateError } = useField("date");
const {
  replace: replaceItem,
  push: newItem,
  fields: items,
} = useFieldArray("items"); // nested items array

// Define functions
const addItemWatcher = handleSubmit(() => {
  newItem({ article: null, quantity: 1, unit: "pcs" });
}, onInvalidSubmit);

function addItem() {
  items.value.length == 0
    ? newItem({
        article: null,
        quantity: 1,
        unit: "pcs",
      })
    : addItemWatcher();
}

const removeItem = (index) => {
  const shallowCopy = [];

  for (const item of items.value) {
    shallowCopy.push({
      article: item.value.article,
      quantity: item.value.quantity,
      unit: item.value.unit,
    });
  }

  shallowCopy.splice(index, 1);
  replaceItem(shallowCopy);
};

async function getProducts() {
  await axios
    .get("/api/v1/stock/products")
    .then((response) => {
      products.value = response.data;
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
        detail: JSON.stringify(error.message),
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

const submitForm =
  isLoading.value === true
    ? null
    : handleSubmit(async (values) => {
        isLoading.value = true;

        values.date = moment(values.date).format("YYYY-MM-DD");
        values.items.forEach((el) => {
          const article = el.article;

          delete el.article;
          el.article = article.id;
          el.unit = article.uom;
        });

        await axios
          .patch(`/api/v1/operations/${operation.id}/`, values)
          .then(() => {
            toast.add({
              severity: "succes",
              summary: "Modification",
              detail: `La facture dpt1/${operation.m_type}${operation.id} a été modifié avec succès`,
              life: 5000,
            });

            router.push({ name: "SingleOps", params: { id: operation.id } });
          });

        isLoading.value = false;
      }, onInvalidSubmit);

function goToCreateProduct() {
  const routeData = router.resolve({
    name: "CreateProduct",
  });

  window.open(routeData.href, "blank");
}

onMounted(async () => {
  pageStore.updatePageName("Entrées - Sorties");

  await getContact();
  await getProducts();
});
</script>

<template>
  <div>
    <PrimeToast />

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
          <MyButton v-else label="Sauver" @click="submitForm()" />
        </div>

        <MyButton label="Retour" to="Operations" :isOutlined="true" />
      </div>
    </div>

    <Card>
      <template #title>
        <h1 class="basis-1/2">Nouvelle opération</h1>
      </template>
      <template #content>
        <div class="block w-full overflow-x-auto p-4">
          <!-- Create form -->
          <form>
            <div class="flex flex-col">
              <!-- order main info -->
              <div
                class="mx-auto flex flex-row justify-between gap-4 rounded-lg border-2 border-kPrimaryColor px-4 py-7 dark:border-kWhiteColor"
              >
                <span class="p-float-label text-md text-slate-700">
                  <PrimeDropdown
                    id="contact"
                    v-model="contact"
                    :options="contactOptions"
                    optionLabel="label"
                    optionValue="value"
                    placeholder="Choisissez le contact"
                    class="w-72"
                    :inputClass="({ 'p-invalid': contactError }, 'w-full')"
                  />

                  <label for="contact" class="text-md text-slate-700">
                    Contact
                  </label>
                </span>

                <span class="p-float-label text-md text-slate-700">
                  <PrimeDropdown
                    id="m_type"
                    v-model="m_type"
                    :options="typeList"
                    optionLabel="label"
                    optionValue="value"
                    placeholder="Choisissez le type"
                    class="w-36"
                    :inputClass="{ 'p-invalid w-full': m_typeError }"
                  />

                  <label for="m_type" class="text-md text-slate-700">
                    Type d'opération
                  </label>
                </span>

                <div>
                  <span class="p-float-label text-md text-slate-700">
                    <PrimeCalendar
                      id="date"
                      v-model="date"
                      dateFormat="dd/mm/yy"
                      class="w-32"
                      :inputClass="{ 'p-invalid w-full': dateError }"
                    />
                    <label for="date" class="text-md text-slate-700">
                      Date
                    </label>
                  </span>
                </div>
              </div>

              <!-- order items info -->

              <div
                class="my-4 h-[45vh] gap-y-4 space-y-2 overflow-y-auto rounded-lg border-2 border-kPrimaryColor p-4 dark:border-kWhiteColor"
              >
                <table>
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
                        <div class="flex items-center">
                          <span>Article</span>
                          <PlusCircleIcon
                            @click="goToCreateProduct"
                            class="ml-3 h-4 w-4 cursor-pointer text-emerald-500 hover:text-emerald-700"
                          />
                        </div>
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
                        v-if="m_type == 'in'"
                        class="sticky top-0 w-2/12 whitespace-nowrap bg-kWhiteColor p-3 text-right align-middle text-xs font-semibold dark:bg-kDarkColor"
                      >
                        Cout d'achat
                      </th>
                      <th
                        class="sticky top-0 w-1/12 whitespace-nowrap bg-kWhiteColor p-3 align-middle text-xs font-semibold dark:bg-kDarkColor"
                      ></th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="(item, idx) in items"
                      :key="item.key"
                      class="rounded-lg focus-within:border-b-2 focus-within:border-kPrimaryColor hover:border-b"
                    >
                      <NestedArray
                        :idx="idx"
                        :checkType="m_type"
                        :products="products"
                        @addItem="addItem"
                        @saveOps="submitForm"
                      />

                      <td
                        class="w-1/12 whitespace-nowrap py-1 px-1.5 text-center align-middle text-xs"
                      >
                        <div
                          @click="removeItem(idx)"
                          class="cursor-pointer rounded-full py-1 px-1.5 text-red-600 hover:bg-red-600 hover:text-white"
                        >
                          <XIcon class="mx-auto h-5 w-5" />
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <PrimeButton
                  type="button"
                  label="Ajouter une ligne"
                  @click="addItem"
                  class="mt-1 w-32 h-1 truncate text-xs p-button-text p-button-info"
                />
              </div>
            </div>
          </form>
        </div>
      </template>
    </Card>
  </div>
</template>
