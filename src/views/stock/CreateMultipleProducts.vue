<script setup>
import { TrashIcon } from "@heroicons/vue/solid";
import { toFormValidator } from "@vee-validate/zod";
import { useToast } from "primevue/usetoast";
import { useFieldArray, useForm } from "vee-validate";
import { onMounted, ref } from "vue-demi";
import { useRouter } from "vue-router";
import * as zod from "zod";
import MyInput from "../../components/shared/forms/BaseInput.vue";
import MyButton from "../../components/shared/my-action.vue";
import { useTempStore } from "../../stores/temp";

// init utils composables to variables
const pageStore = useTempStore();
const router = useRouter();
const toast = useToast();

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

const dateSchema = zod.preprocess((arg) => {
  if (typeof arg == "string" || arg instanceof Date) return new Date(arg);
}, zod.date({ required_error: "la date est obligatoire" }));

const validationSchema = toFormValidator(
  zod.object({
    tag: zod
      .string({
        required_error: "libellé est obligatoire",
      })
      .min(3, { message: "contact doit avoir 3 charactère minimum" }),

    date: dateSchema,
    items: zod
      .object({
        name: zod.string({
          required_error: "nom de l'article obligatoire",
        }),
        providers: zod.string().nullish(),
        category: zod.string().nullish(),
        uom: zod.string({
          required_error: "unité de mesure obligatoire",
        }),
        alert_stock: zod.number().min(0),
        optimal_stock: zod.number().min(0),
        real_quantity: zod
          .number({
            required_error: "quantité initial obligatoire",
          })
          .min(0, "le nombre compté doit etre de 0 minimum"),
        unit_price: zod
          .number({
            required_error: "obligatoire",
          })
          .min(0, "le prix doit etre de 0 minimum"),
        unit_cost: zod
          .number({
            required_error: "obligatoire",
          })
          .min(0, "le cout doit etre de 0 minimum"),
      })
      .array()
      .nonempty("Veillez enregistrer les nouveaux articles"),
  })
);

// Create a form context with the validation schema
const { handleSubmit } = useForm({
  validationSchema: validationSchema,
});

// define array fields
const { remove, push, fields } = useFieldArray("items");

// define functions
const addItemWatcher = handleSubmit(() => {
  push({
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 0,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 1,
  });
}, onInvalidSubmit);

function addItem() {
  fields.value.length == 0
    ? push({
        alert_stock: 0,
        optimal_stock: 0,
        real_quantity: 0,
        virtual_quantity: 0,
        unit_price: 1,
        unit_cost: 1,
      })
    : addItemWatcher();
}

function removeItem(id) {
  remove(id);
}

function onInvalidSubmit({ errors }) {
  Object.entries(errors).forEach((item) => {
    let itemMsg = item[1] == "Required" ? "obligatoire" : item[1];

    toast.add({
      severity: "error",
      summary: "Donnée invalide",
      detail: itemMsg,
      life: 3000,
    });
  });
}

const onSubmit = handleSubmit(async (values) => {
  console.log(JSON.stringify(values, null, 2));
}, onInvalidSubmit);

onMounted(() => {
  pageStore.updatePageName("Entrées - Sorties");
});
</script>

<template>
  <div>
    <PrimeToast />

    <!-- Header -->
    <div class="mx-auto w-full px-4">
      <div class="flex w-full flex-row items-center">
        <MyButton label="Sauver" @click="onSubmit" />

        <MyButton label="Retour" to="Operations" :isOutlined="true" />
      </div>
    </div>

    <!-- card -->
    <div class="mt-4 flex flex-wrap">
      <div class="mb-12 w-full px-4">
        <div
          class="relative mb-6 flex w-full min-w-0 flex-col break-words rounded bg-white shadow-lg"
        >
          <div class="mb-0 rounded-t border-0 px-4 py-3">
            <div class="flex flex-wrap items-center">
              <div class="relative w-full max-w-full flex-1 flex-grow px-4">
                <h3 class="text-lg font-semibold text-slate-700">
                  Nouvelle opération
                </h3>
              </div>
            </div>
          </div>

          <div class="block w-full overflow-x-auto p-4">
            <!-- Create form -->
            <form>
              <div class="flex flex-col">
                <!-- order main info -->
                <div
                  class="mx-auto flex flex-row justify-between gap-4 rounded-lg border-2 p-4 py-4"
                >
                  <MyInput type="text" name="tag" placeholder="Libellé" />

                  <MyInput type="date" name="date" :todayShortcut="true" />
                </div>

                <!-- inventory items info -->
                <div
                  class="my-4 h-96 gap-y-4 space-y-2 overflow-y-auto rounded-lg border-2 p-4"
                >
                  <table
                    class="w-full table-fixed text-left text-sm text-gray-500 dark:text-gray-400"
                  >
                    <thead
                      class="bg-gray-50 text-xs uppercase text-gray-700 dark:bg-gray-700 dark:text-gray-400"
                    >
                      <tr>
                        <th
                          scope="col"
                          class="w-3/12 truncate py-3 px-1.5 text-center"
                        >
                          Article
                        </th>
                        <th
                          scope="col"
                          class="w-1/12 truncate border-r py-3 px-1.5 text-center"
                        >
                          Compté
                        </th>
                        <th
                          scope="col"
                          class="w-1/12 truncate py-3 px-1.5 text-center"
                        >
                          Unité
                        </th>
                        <th
                          scope="col"
                          class="w-1/12 truncate py-3 px-1.5 text-center"
                        >
                          Fournisseur
                        </th>
                        <th
                          scope="col"
                          class="w-1/12 truncate border-r py-3 px-1.5 text-center"
                        >
                          Catégorie
                        </th>
                        <th
                          scope="col"
                          class="w-1/12 truncate py-3 px-1.5 text-center"
                        >
                          Alerte
                        </th>
                        <th
                          scope="col"
                          class="w-1/12 truncate border-r py-3 px-1.5 text-center"
                        >
                          Idéal
                        </th>
                        <th
                          scope="col"
                          class="w-1/12 truncate py-3 px-1.5 text-center"
                        >
                          Cout
                        </th>
                        <th
                          scope="col"
                          class="w-1/12 truncate py-3 px-1.5 text-center"
                        >
                          Prix
                        </th>
                        <td class="w-1/12"></td>
                      </tr>
                    </thead>
                    <tbody>
                      <tr
                        v-for="(item, idx) in fields"
                        :key="item.key"
                        class="border-b bg-white dark:border-gray-700 dark:bg-gray-800"
                      >
                        <th
                          scope="row"
                          class="whitespace-nowrap px-6 py-4 font-medium text-gray-900 dark:text-white"
                        >
                          <MyInput
                            type="text"
                            :name="`items[${idx}].name`"
                            placeholder="article"
                          />
                        </th>
                        <td class="px-1.5">
                          <MyInput
                            type="number"
                            :name="`items[${idx}].real_quantity`"
                            placeholder="qté"
                          />
                        </td>
                        <td class="px-1.5">
                          <MyInput
                            type="select"
                            :name="`items[${idx}].uom`"
                            :options="uomList"
                            placeholder="unité"
                          />
                        </td>
                        <td class="px-1.5">
                          <MyInput
                            type="text"
                            :name="`items[${idx}].providers`"
                            placeholder="fournisseur"
                          />
                        </td>
                        <td class="border-r px-1.5">
                          <MyInput
                            type="select"
                            :name="`items[${idx}].category`"
                            :options="categories"
                            placeholder="categorie"
                          />
                        </td>
                        <td class="px-1.5">
                          <MyInput
                            type="number"
                            :name="`items[${idx}].alert_stock`"
                            placeholder="alert"
                          />
                        </td>
                        <td class="border-r px-1.5">
                          <MyInput
                            type="number"
                            :name="`items[${idx}].optimal_stock`"
                            placeholder="idéal"
                          />
                        </td>
                        <td class="px-1.5">
                          <MyInput
                            type="number"
                            :name="`items[${idx}].unit_cost`"
                            placeholder="cout"
                          />
                        </td>
                        <td class="px-1.5">
                          <MyInput
                            type="number"
                            :name="`items[${idx}].unit_price`"
                            placeholder="prix"
                          />
                        </td>
                        <td class="px-1.5">
                          <TrashIcon
                            @click="removeItem(idx)"
                            class="mx-auto mt-1 h-5 w-5 cursor-pointer text-red-500"
                          />
                        </td>
                      </tr>
                    </tbody>
                  </table>

                  <button
                    type="button"
                    @click="addItem"
                    class="mt-1 w-32 rounded-lg px-3 py-1 text-xs text-kPrimaryColor underline hover:bg-kPrimaryColor hover:font-semibold hover:text-white"
                  >
                    Ajouter une ligne
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
