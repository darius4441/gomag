<script setup>
import { PlusCircleIcon, RefreshIcon, XIcon } from "@heroicons/vue/solid";
import { toFormValidator } from "@vee-validate/zod";
import axios from "axios";
import Calendar from "primevue/calendar";
import Dropdown from "primevue/dropdown";
import { useField, useFieldArray, useForm } from "vee-validate";
import { onMounted, ref } from "vue-demi";
import { useRouter } from "vue-router";
import { useToast } from "vue-toast-notification";
import * as zod from "zod";
import NestedArray from "../../components/operations/creation-item-form.vue";
import Card from "../../components/shared/card-component.vue";
import MyButton from "../../components/shared/my-action.vue";
import { useTempStore } from "../../stores/temp";

// init utils composables to variables
const pageStore = useTempStore();
const router = useRouter();
const toast = useToast();

// Define vars / const
const isLoading = ref(false);
const products = ref([]);
const contactOptions = ref([]);
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
    contact: 1,
    m_type: "out",
  },
});

const { value: contact } = useField("contact");
const { value: m_type } = useField("m_type");
const { value: date } = useField("date");
const { remove, push, fields } = useFieldArray("items"); // nested array fields

// Define functions
const addItemWatcher = handleSubmit(() => {
  push({ article: null, quantity: 1, unit: "pcs" });
}, onInvalidSubmit);

function addItem() {
  fields.value.length == 0
    ? push({
        article: null,
        quantity: 1,
        unit: "pcs",
      })
    : addItemWatcher();
}

async function getProducts() {
  await axios
    .get("/api/v1/stock/products")
    .then((response) => {
      products.value = response.data;
    })
    .catch((error) => {
      toast.error(JSON.stringify(error));
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
      toast.error(JSON.stringify(error));
    });
}

function onInvalidSubmit({ errors }) {
  let i = 1;
  Object.entries(errors).forEach((item) => {
    if (item[0].includes("items")) {
      if (i != 0) {
        i--;
        toast.error(
          "Veillez ajouter un article avec une quantité de 1 au minimum",
          {
            position: "top-right",
          }
        );
      }
    } else {
      toast.error(`Le champs ${item[0]} est ${item[1]}`, {
        position: "top-right",
      });
    }
  });
}

const onSubmit =
  isLoading.value === true
    ? null
    : handleSubmit(async (values) => {
        isLoading.value = true;
        values.items.forEach((el) => {
          const article = el.article;

          delete el.article;
          el.article = article.id;
          el.unit = article.uom;
        });

        await axios
          .post("/api/v1/operations/", values)
          .then((res) => {
            router.push({ name: "SingleOps", params: { id: res.data.id } });
          })
          .catch((error) => {
            toast.error(error.message, {
              position: "top-right",
            });
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
                  <Dropdown
                    id="contact"
                    v-model="contact"
                    :options="contactOptions"
                    optionLabel="label"
                    optionValue="value"
                    placeholder="Choisissez le contact"
                    class="w-72"
                    inputClass="w-full"
                  />

                  <label for="contact" class="text-md text-slate-700">
                    Contact
                  </label>
                </span>

                <span class="p-float-label text-md text-slate-700">
                  <Dropdown
                    id="m_type"
                    v-model="m_type"
                    :options="typeList"
                    optionLabel="label"
                    optionValue="value"
                    placeholder="Choisissez le type"
                    class="w-36"
                    inputClass="w-full"
                  />

                  <label for="m_type" class="text-md text-slate-700">
                    Type d'opération
                  </label>
                </span>

                <div>
                  <span class="p-float-label text-md text-slate-700">
                    <Calendar
                      id="date"
                      v-model="date"
                      class="w-32"
                      inputClass="w-full"
                    />
                    <label for="date" class="text-md text-slate-700">
                      Date
                    </label>
                  </span>
                </div>
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
                      v-for="(item, idx) in fields"
                      :key="item.key"
                      class="rounded-lg focus-within:border-b-2 focus-within:border-kPrimaryColor hover:border-b"
                    >
                      <NestedArray
                        :idx="idx"
                        :checkType="m_type"
                        :products="products"
                        @addItem="addItem"
                      />

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
