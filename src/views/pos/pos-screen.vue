<script setup>
import articlePhoto from "@/assets/images/default/article-default-img.png";
import { reset } from "@formkit/core";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@headlessui/vue";
import axios from "axios";
import { computed, onMounted, ref } from "vue-demi";
import MyButton from "../../components/shared/my-action.vue";
import { useTempStore } from "../../stores/temp";
// ? Define composables
const pageStore = useTempStore();

// ? Define vars - consts
const products = ref([]);
const search = ref("");
const order = ref([]);
const addItemFormRef = ref(null);

const addItemFormData = ref({});

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

// ? Declare functions
function addItem() {
  const node = addItemFormRef.value.node;

  node.submit();
}

function addItemHandler() {
  order.value.push(addItemFormData.value);

  reset("addItemFormID");
}

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
  <div class="flex h-[86vh] flex-row gap-x-4 p-4">
    <!-- add item area -->
    <div class="relative basis-3/4">
      <div class="m-4 flex flex-wrap gap-4">
        <button
          v-for="(item, idx) in products"
          :key="idx"
          @dblclick="
            () => {
              addItemFormData.articleID = item.id;
              addItemFormData.article = item.name;
              addItemFormData.quantity = 1;
              addItemFormData.unit = item.uom;
              addItemFormData.unit_price = item.unit_price;
            }
          "
          class="w-32 cursor-pointer rounded bg-white shadow-lg duration-300 hover:-translate-y-2"
        >
          <div class="relative">
            <img :src="getCorrectPhoto(item)" alt="image" />
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
        </button>
      </div>

      <div
        class="absolute bottom-0 flex flex-col items-center py-4 shadow shadow-indigo-400"
      >
        <FormKit
          ref="addItemFormRef"
          id="addItemFormID"
          v-model="addItemFormData"
          type="form"
          :actions="false"
          @submit="addItemHandler"
        >
          <div
            class="flex flex-row items-center justify-between rounded-lg bg-kPrimaryColor/50 py-2 px-4"
          >
            <div class="flex space-x-4">
              <FormKit
                type="text"
                label="Article"
                name="article"
                validation="required"
              />

              <FormKit
                type="number"
                label="Quantité"
                name="quantity"
                validation="required|min(1)"
              />

              <FormKit
                type="text"
                label="Unité"
                name="unit"
                validation="required"
              />

              <FormKit
                type="number"
                label="Prix u."
                name="unit_price"
                validation="required|min(5)"
              />
            </div>

            <MyButton
              type="button"
              @click="addItem"
              :isOutlined="true"
              label="Ajouter"
              class="ml-4"
            />
          </div>
        </FormKit>

        <div
          class="flex w-3/5 justify-center rounded-b-lg bg-kPrimaryColor/50 pt-4 shadow-inner shadow-indigo-300"
        >
          <FormKit
            type="search"
            v-model="search"
            placeholder="Trouver ..."
            @input="getProducts()"
          />
        </div>
      </div>
    </div>

    <!-- order area -->
    <div class="relative basis-1/4 bg-kPrimaryColor text-kWhiteColor">
      <div class="mb-1 h-12 bg-kWhiteColor/20">
        <h1 class="text-center text-lg font-bold">Votre panier</h1>
      </div>

      <div v-if="order.length" class="w-full px-4">
        <div class="overflow-y-auto">
          <div
            v-for="(item, idx) in order"
            :key="idx"
            v-auto-animate
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

        <MyButton label="Paiement" class="w-full" />
      </div>
    </div>
  </div>
</template>
