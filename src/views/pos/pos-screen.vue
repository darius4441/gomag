<script setup>
import articlePhoto from "@/assets/images/default/article-default-img.png";
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
  MenuButton,
  MenuItem,
} from "@headlessui/vue";
import { toFormValidator } from "@vee-validate/zod";
import axios from "axios";
import { useField, useForm } from "vee-validate";
import { computed, onMounted, ref } from "vue-demi";
import * as zod from "zod";
import ConfirmOrderModal from "../../components/pos/confirm_order_modal.vue";
import MyButton from "../../components/shared/my-action.vue";
import MyMenu from "../../components/shared/my-menu.vue";
import { useTempStore } from "../../stores/temp";
// ? Define composables
const pageStore = useTempStore();

// ? Define vars - consts
const product = ref({});
const products = ref([]);
const search = ref("");
const order = ref([]);
const isConfirmOrderModal = ref(false);

const discount = ref("");
const subTotal = computed(() => {
  let tot = order.value.reduce((total, currentVal) => {
    return total + currentVal.quantity * currentVal.unit_price;
  }, 0);
  return tot;
});

const totalAmount = computed(
  () => subTotal.value - Number(discount.value ?? 0)
);

const validationSchema = toFormValidator(
  zod.object({
    id: zod.number({
      required_error: "cet article n'est pas valable",
    }),

    article: zod.string({
      required_error: "article est obligatoire",
    }),

    unit: zod.string({
      required_error: "unité de mesure est obligatoire",
    }),

    quantity: zod
      .number({
        required_error: "la quantité est obligatoire",
        invalid_type_error: "la quantité doit etre un nombre",
      })
      .gte(1, { message: "la quantité doit avoir minimum 1" }),

    unit_price: zod
      .number({
        required_error: "prix de vente est obligatoire",
        invalid_type_error: "prix de vente doit etre un nombre",
      })
      .gte(0, { message: "prix de vente doit avoir minimum 0" }),
  })
);

// Create a form context with the validation schema
const { handleSubmit, resetForm } = useForm({
  validationSchema: validationSchema,

  initialValues: {
    quantity: 1,
  },
});

const { value: id } = useField("id");
const { value: article, errorMessage: articleError } = useField("article");
const { value: unit, errorMessage: unitError } = useField("unit");
const { value: quantity, errorMessage: quantityError } = useField("quantity");
const { value: unit_price, errorMessage: unit_priceError } =
  useField("unit_price");

// ? Declare functions

const addItem = handleSubmit((values) => {
  order.value.push(values);

  resetForm();
});

async function getProducts() {
  await axios
    .get(`api/v1/stock/pos/?search=${search.value ?? ""}`)
    .then((response) => {
      products.value = response.data.results;
    })
    .catch((error) => {
      console.log(JSON.stringify(error));
    });
}

async function resetSearch() {
  search.value = "";
  await getProducts();
}

async function getProduct(id) {
  await axios
    .get(`api/v1/stock/products/${id}`)
    .then((response) => {
      product.value = response.data;
    })
    .catch((error) => {
      console.log(JSON.stringify(error));
    });
}

const getCorrectPhoto = (item) => {
  item;
  return articlePhoto;
};

onMounted(async () => {
  pageStore.updatePageName("Point de vente");

  await getProducts();
});
</script>

<template>
  <ConfirmOrderModal
    :order="{
      items: order,
      resumeInfo: {
        subTotal: subTotal,
        discount: discount,
        totalAmount: totalAmount,
      },
    }"
    :isOpen="isConfirmOrderModal"
    @closeModal="isConfirmOrderModal = false"
  />

  <div class="flex h-[85vh] flex-row gap-x-4 mb-2">
    <!-- add item area -->
    <div class="w-full relative">
      <div
        class="grid p-1 h-[60vh] gap-2 overflow-y-auto grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6"
      >
        <MyMenu
          v-for="(item, idx) in products"
          :key="idx"
          v-motion-pop-visible-once
          menuItemsWidthClass="top-0"
          class="mx-auto"
        >
          <template #menu_button>
            <MenuButton
              @click="getProduct(item.id)"
              @dblclick="
                () => {
                  id = item.id;
                  article = item.name;
                  quantity = 1;
                  unit = item.uom;
                  unit_price = item.unit_price;
                }
              "
              class="cursor-pointer w-40 sm:w-36 md:w-32 lg:w-36 rounded bg-white shadow-lg duration-300 hover:ring-2 ring-kPrimaryColor"
            >
              <div class="relative">
                <img :src="getCorrectPhoto(item)" alt="image" class="w-full" />
                <div
                  class="absolute top-2 right-2 rounded bg-kPrimaryColor text-kWhiteColor"
                >
                  <span class="px-2 text-sm">
                    {{ Number(item.unit_price).toLocaleString() }} F</span
                  >
                </div>
              </div>
              <div class="h-12 w-full overflow-y-hidden bg-white p-1 shadow-lg">
                <p class="text-left text-xs dark:text-kPrimaryColor">
                  {{ item.name }}
                </p>
              </div>
            </MenuButton>
          </template>

          <template #menu_content>
            <MenuItem as="div" class="truncate text-xs"
              >Dispo :
              <span class="font-bold">{{ product.real_quantity }}</span>
              <span class="font-bold ml-1">{{ product.uom }}</span>
            </MenuItem>
            <MenuItem as="div" class="truncate text-xs"
              >Détail :
              <span class="font-bold">{{ product.unit_price }} F</span>
            </MenuItem>
            <MenuItem as="div" class="truncate text-xs"
              >½ gros :
              <span class="font-bold"
                >{{ product.semi_wholesale_price }} F</span
              >
            </MenuItem>
            <MenuItem as="div" class="truncate text-xs"
              >Gros :
              <span class="font-bold">{{ product.wholesale_price }} F</span>
            </MenuItem>
          </template>
        </MyMenu>
      </div>

      <div
        class="absolute bottom-0 flex flex-col items-center p-1 shadow shadow-indigo-400"
      >
        <form class="w-full">
          <div class="grid grid-cols-6 gap-x-2">
            <div class="col-span-2">
              <span class="p-float-label mt-6 text-md text-slate-700">
                <PrimeInputText
                  type="text"
                  id="article"
                  v-model:model-value="article"
                  class="w-full"
                  :class="{ 'p-invalid': articleError }"
                />

                <label for="article" class="text-md text-slate-700"
                  >Article</label
                >
              </span>
            </div>

            <div class="col-span-1">
              <span class="p-float-label mt-6 text-md text-slate-700">
                <PrimeInputNumber
                  id="quantity"
                  v-model:model-value="quantity"
                  class="w-full"
                  inputClass="w-full"
                  :min="1"
                  :class="{ 'p-invalid': quantityError }"
                />

                <label for="quantity" class="text-md text-slate-700"
                  >Quantité</label
                >
              </span>
            </div>

            <div class="col-span-1">
              <span class="p-float-label mt-6 text-md text-slate-700">
                <PrimeInputText
                  type="text"
                  id="unit"
                  v-model:model-value="unit"
                  class="w-full"
                  :class="{ 'p-invalid': unitError }"
                />

                <label for="unit" class="text-md text-slate-700">Unité</label>
              </span>
            </div>

            <div class="col-span-1">
              <span class="p-float-label mt-6 text-md text-slate-700">
                <PrimeInputNumber
                  id="unit_price"
                  v-model:model-value="unit_price"
                  class="w-full"
                  inputClass="w-full"
                  :min="1"
                  :class="{ 'p-invalid': unit_priceError }"
                />

                <label for="unit_price" class="text-md text-slate-700"
                  >Prix unitaire</label
                >
              </span>
            </div>

            <div class="h-10 mt-6">
              <PrimeButton
                label="Ajouter"
                @click="addItem"
                class="p-button-info p-button-sm p-button-outlined"
              />
            </div>
          </div>
        </form>

        <div
          class="flex w-3/5 justify-center border-2 rounded-b-lg border-kPrimaryColor/50 py-2 mt-2"
        >
          <div class="col-12 md:col-4">
            <div class="p-inputgroup">
              <PrimeInputText
                type="text"
                v-model="search"
                placeholder="Trouver ..."
                @input="getProducts()"
              />
              <PrimeButton
                icon="pi pi-times"
                @click="resetSearch"
                class="p-button-secondary p-button-sm"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- order area -->
    <div class="relative w-[65vh] bg-kPrimaryColor text-kWhiteColor">
      <div class="mb-1 h-12 bg-kWhiteColor/20">
        <h1 class="text-center text-lg font-bold">Votre panier</h1>
      </div>

      <div v-if="order.length" class="w-full px-4">
        <div class="overflow-y-auto">
          <div
            v-for="(item, idx) in order"
            :key="idx"
            v-motion-slide-bottom
            class="mx-auto mt-2 w-full rounded-lg bg-white"
          >
            <Disclosure>
              <DisclosureButton class="w-full text-xs">
                <div
                  class="rounded-md bg-kPrimaryColor/90 px-4 py-2 hover:bg-kPrimaryColor/75"
                >
                  <div class="flex justify-between gap-x-2">
                    <span class="w-2/3 truncate">{{ item.article }}</span>
                    <span class="w-1/3 truncate text-right"
                      >{{ item.quantity }} x
                      {{ item.unit_price.toLocaleString() }}F
                    </span>
                  </div>
                  <p class="text-right font-bold">
                    {{ (item.quantity * item.unit_price).toLocaleString() }}F
                  </p>
                </div>
              </DisclosureButton>
              <DisclosurePanel
                class="max-h-64 overflow-y-auto px-4 pt-4 pb-2 text-sm"
              >
                <div>Roch Arthur on the beat</div>
              </DisclosurePanel>
            </Disclosure>
          </div>
        </div>
      </div>

      <div
        v-if="order.length"
        class="absolute bottom-0 mt-1 bg-kWhiteColor/20 px-4"
      >
        <div class="grid grid-cols-2">
          <div class="mb-3">Sous total</div>
          <div class="text-right">{{ subTotal.toLocaleString() }}F</div>

          <div class="mb-3">Reduction</div>
          <div class="w-full">
            <input
              type="text"
              v-model="discount"
              name="discount"
              class="w-full self-end border-b border-white bg-white/10 text-right"
            />
          </div>

          <div class="mb-3">Total</div>
          <div class="text-right font-bold">{{ totalAmount }}F</div>
        </div>

        <MyButton
          label="Paiement"
          @click="isConfirmOrderModal = true"
          class="w-full"
        />
      </div>
    </div>
  </div>
</template>
