<script setup>
import { ArrowSmDownIcon, CheckIcon, XIcon } from "@heroicons/vue/solid";
import { useRouter } from "vue-router";

const props = defineProps({
  what_data: String,
  label_with_filter_name_and_class: Array,
  data_list: Array,
  state: String,
  m_type: String,
});

const emits = defineEmits(["inQuantity"]);

const router = useRouter();

async function goToSingleProduct(id) {
  router.push({ name: "SingleProduct", params: { id: id } });
}

async function goToSingleOps(id) {
  router.push({ name: "SingleOps", params: { id: id } });
}

const trueLabel = (label) => {
  switch (label) {
    case "draft":
      return "brouillon";

    case "pending":
      return "en attente";

    case "done":
      return "fait";

    default:
      return "brouillon";
  }
};

function currencyFormater(val) {
  return new Intl.NumberFormat("fr-CI", {
    style: "currency",
    currency: "XOF",
  }).format(Number(val));
}

const formatDate = (dateString) => {
  const date = new Date(dateString);
  // Then specify how you want your dates to be formatted
  return new Intl.DateTimeFormat("fr-FR", { dateStyle: "medium" }).format(date);
};

const emitUnvalid = () => {
  emits("inQuantity");
};

localStorage.removeItem("vueUseOperation");
localStorage.removeItem("vueUseProduct");
localStorage.removeItem("vueUseProducts");
localStorage.removeItem("vueUseContact");
</script>

<template>
  <table class="relative w-full">
    <thead>
      <tr>
        <template
          v-for="(item, idx) in props.label_with_filter_name_and_class"
          :key="idx"
        >
          <template v-if="item.label == 'Qté dispo'">
            <th
              v-if="props.state != 'done'"
              class="sticky top-0 whitespace-nowrap bg-kWhiteColor py-3 align-middle text-xs font-semibold dark:bg-kDarkColor"
              :class="item.isClass"
            >
              {{ item.label }}
            </th>
          </template>
          <th
            v-else
            class="sticky top-0 whitespace-nowrap bg-kWhiteColor py-3 align-middle text-xs font-semibold dark:bg-kDarkColor"
            :class="item.isClass"
          >
            {{ item.label }}
          </th>
        </template>
      </tr>
    </thead>
    <tbody>
      <template v-if="props.what_data == 'product'">
        <tr
          v-for="(item, idx) in data_list"
          :key="idx"
          @click="goToSingleProduct(item.id)"
          class="cursor-pointer py-1 hover:bg-kPrimaryColor hover:text-kWhiteColor"
        >
          <th class="whitespace-nowrap py-2.5 text-left align-middle text-xs">
            {{ item.name }}
          </th>
          <td class="whitespace-nowrap py-2.5 text-left align-middle text-xs">
            {{ item.get_category }}
          </td>
          <td class="whitespace-nowrap py-2.5 text-center align-middle text-xs">
            {{ item.providers }}
          </td>
          <td class="whitespace-nowrap py-2.5 text-right align-middle text-xs">
            {{ item.real_quantity }}
          </td>
          <td class="whitespace-nowrap py-2.5 text-center align-middle text-xs">
            {{ item.uom }}
          </td>
          <td class="whitespace-nowrap py-2.5 text-right align-middle text-xs">
            {{ currencyFormater(item.unit_cost) }}
          </td>
          <td class="whitespace-nowrap py-2.5 text-right align-middle text-xs">
            {{ currencyFormater(item.unit_price) }}
          </td>
        </tr>
      </template>

      <template v-else-if="props.what_data == 'operation'">
        <tr
          v-for="(ops, idx) in data_list"
          :key="idx"
          @click="goToSingleOps(ops.id)"
          class="cursor-pointer hover:bg-kPrimaryColor hover:text-kWhiteColor"
        >
          <th
            class="block cursor-pointer whitespace-nowrap py-2.5 text-left align-middle text-xs"
          >
            <div class="gap-x-3 text-left">
              dpt1/{{ ops.m_type }}{{ ops.id }}

              <ArrowSmDownIcon
                v-if="ops.m_type == 'in'"
                class="inline-block h-4 w-4 text-emerald-500"
              />
            </div>
          </th>
          <td class="whitespace-nowrap py-2.5 text-left align-middle text-xs">
            {{ ops.getContactName }}
          </td>
          <td class="whitespace-nowrap py-2.5 text-center align-middle text-xs">
            {{ formatDate(ops.date) }}
          </td>
          <td
            class="flex flex-row items-center whitespace-nowrap py-2.5 text-left align-middle text-xs"
          >
            <div
              class="mr-2 inline-flex h-3 w-3 rounded-full"
              :class="[
                {
                  ' bg-gray-500': ops.state == 'draft',
                  ' bg-orange-500': ops.state == 'pending',
                  ' bg-emerald-500': ops.state == 'done',
                },
              ]"
            ></div>
            <span>{{ trueLabel(ops.state) }}</span>
          </td>
        </tr>
      </template>

      <template v-else-if="props.what_data == 'singleOps'">
        <tr
          v-for="(item, idx) in data_list"
          :key="idx"
          class="py-1 hover:bg-kPrimaryColor hover:text-kWhiteColor"
        >
          <th
            class="cursor-pointer whitespace-nowrap py-2 text-left align-middle text-xs"
          >
            <div class="flex gap-x-2">
              <template v-if="props.state != 'done'">
                <template v-if="props.m_type === 'out'">
                  <CheckIcon
                    v-if="item.get_article_available_qty - item.quantity >= 0"
                    class="h-5 w-5 text-emerald-600"
                  />
                  <XIcon
                    v-else
                    class="h-5 w-5 text-orange-700"
                    @vnode-before-mount="emitUnvalid"
                  />
                </template>
              </template>
              {{ item.get_article_name }}
            </div>
          </th>
          <td class="whitespace-nowrap py-1 text-right align-middle text-xs">
            {{ item.quantity }}
          </td>
          <td class="whitespace-nowrap py-1 text-center align-middle text-xs">
            {{ item.unit }}
          </td>
          <td
            v-if="props.state != 'done'"
            class="whitespace-nowrap py-1 text-right align-middle text-xs"
          >
            {{ parseFloat(item.get_article_available_qty) }}
          </td>
        </tr>
      </template>
    </tbody>
  </table>
</template>
