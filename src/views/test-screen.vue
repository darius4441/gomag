<script setup>
import { ref } from "vue-demi";
import { token } from "@formkit/utils";
import { getNode, createMessage } from "@formkit/core";
import { createInput } from "@formkit/vue";
import MyCombobox from "../components/shared/forms/BaseFormKitInput.vue";
import MyCombobox2 from "../components/shared/forms/FormKitExample.vue";

const combobox = createInput(MyCombobox, { props: ["options"] });
const combobox2 = createInput(MyCombobox2);

const products = ref([
  {
    id: 353,
    name: "CHAMPION 4KG JAUNE SIPPEC",
    prod_type: "storable",
    category: 4,
    code: null,
    description: null,
    providers: "SIPPEC",
    uom: "pot",
    slug: "champion-4kg-jaune-sippec",
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 6,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 7000,
    created_at: "2022-05-17T17:57:58.398252Z",
    created_by: 1,
    modified_at: "2022-06-01T15:12:08.226502Z",
    modified_by: 1,
    getReplenish: 0,
    getUom: "pot",
    get_category: "Peinture",
  },
  {
    id: 348,
    name: "CHAMPION 4KG MARRON CLAIR SIPPEC",
    prod_type: "storable",
    category: 4,
    code: null,
    description: null,
    providers: "SIPPEC",
    uom: "pot",
    slug: "champion-4kg-marron-clair-sippec",
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 90,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 7000,
    created_at: "2022-05-17T17:57:58.369595Z",
    created_by: 1,
    modified_at: "2022-06-01T15:12:08.257177Z",
    modified_by: 1,
    getReplenish: 0,
    getUom: "pot",
    get_category: "Peinture",
  },
  {
    id: 347,
    name: "CHAMPION 4KG MARRON FONCE SIPPEC",
    prod_type: "storable",
    category: 4,
    code: null,
    description: null,
    providers: "SIPPEC",
    uom: "pot",
    slug: "champion-4kg-marron-fonce-sippec",
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 49,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 7000,
    created_at: "2022-05-17T17:57:58.364811Z",
    created_by: 1,
    modified_at: "2022-06-01T15:12:08.265970Z",
    modified_by: 1,
    getReplenish: 0,
    getUom: "pot",
    get_category: "Peinture",
  },
  {
    id: 354,
    name: "CHAMPION 4KG NOIR SIPPEC",
    prod_type: "storable",
    category: 4,
    code: null,
    description: null,
    providers: "SIPPEC",
    uom: "pot",
    slug: "champion-4kg-noir-sippec",
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 3,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 7000,
    created_at: "2022-05-17T17:57:58.402869Z",
    created_by: 1,
    modified_at: "2022-06-01T17:56:53.029731Z",
    modified_by: 1,
    getReplenish: 0,
    getUom: "pot",
    get_category: "Peinture",
  },
  {
    id: 350,
    name: "CHAMPION 4KG ROUGE SIPPEC",
    prod_type: "storable",
    category: 4,
    code: null,
    description: null,
    providers: "SIPPEC",
    uom: "pot",
    slug: "champion-4kg-rouge-sippec",
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 34,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 7000,
    created_at: "2022-05-17T17:57:58.383443Z",
    created_by: 1,
    modified_at: "2022-06-01T15:12:08.246049Z",
    modified_by: 1,
    getReplenish: 0,
    getUom: "pot",
    get_category: "Peinture",
  },
  {
    id: 352,
    name: "CHAMPION 4KG VERT SIPPEC",
    prod_type: "storable",
    category: 4,
    code: null,
    description: null,
    providers: "SIPPEC",
    uom: "pot",
    slug: "champion-4kg-vert-sippec",
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 0,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 7000,
    created_at: "2022-05-17T17:57:58.393254Z",
    created_by: 1,
    modified_at: "2022-06-01T17:56:53.105186Z",
    modified_by: 1,
    getReplenish: 0,
    getUom: "pot",
    get_category: "Peinture",
  },
  {
    id: 289,
    name: "CHAMPION 5KG SIPPEC",
    prod_type: "storable",
    category: 4,
    code: null,
    description: null,
    providers: "SIPPEC",
    uom: "pot",
    slug: "champion-5kg-sippec",
    alert_stock: 90,
    optimal_stock: 300,
    real_quantity: 387,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 2500,
    created_at: "2022-05-14T14:06:48.040985Z",
    created_by: 1,
    modified_at: "2022-06-01T15:12:08.301169Z",
    modified_by: 1,
    getReplenish: -87,
    getUom: "pot",
    get_category: "Peinture",
  },
  {
    id: 303,
    name: "CHAPE 40",
    prod_type: "storable",
    category: 7,
    code: null,
    description: null,
    providers: null,
    uom: "rlx",
    slug: "chape-40",
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 17,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 1,
    created_at: "2022-05-16T18:04:12.259645Z",
    created_by: 1,
    modified_at: "2022-06-01T15:09:30.442180Z",
    modified_by: 1,
    getReplenish: 0,
    getUom: "rlx",
    get_category: "Etanchéité",
  },
  {
    id: 324,
    name: "CHAUSSURE SECURITE 40 INGCO",
    prod_type: "storable",
    category: 2,
    code: "SSH08S1P",
    description: null,
    providers: "INGCO",
    uom: "paire",
    slug: "chaussure-securite-40-ingco",
    alert_stock: 12,
    optimal_stock: 24,
    real_quantity: 7,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 1,
    created_at: "2022-05-17T17:57:58.239020Z",
    created_by: 1,
    modified_at: "2022-06-01T15:21:07.254756Z",
    modified_by: 1,
    getReplenish: 17,
    getUom: "paire",
    get_category: "Divers",
  },
  {
    id: 325,
    name: "CHAUSSURE SECURITE 41 INGCO",
    prod_type: "storable",
    category: 2,
    code: "SSH08S1P",
    description: null,
    providers: "INGCO",
    uom: "paire",
    slug: "chaussure-securite-41-ingco",
    alert_stock: 12,
    optimal_stock: 24,
    real_quantity: 3,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 1,
    created_at: "2022-05-17T17:57:58.244614Z",
    created_by: 1,
    modified_at: "2022-06-01T15:21:07.251002Z",
    modified_by: 1,
    getReplenish: 21,
    getUom: "paire",
    get_category: "Divers",
  },
  {
    id: 337,
    name: "CHAUSSURE SECURITE 42 INGCO",
    prod_type: "storable",
    category: 2,
    code: "SSH04SB",
    description: null,
    providers: "INGCO",
    uom: "paire",
    slug: "chaussure-securite-42-ingco",
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 7,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 1,
    created_at: "2022-05-17T17:57:58.311718Z",
    created_by: 1,
    modified_at: "2022-06-01T15:21:07.218556Z",
    modified_by: 1,
    getReplenish: 0,
    getUom: "paire",
    get_category: "Divers",
  },
  {
    id: 323,
    name: "CHAUSSURE SECURITE 43 INGCO",
    prod_type: "storable",
    category: 2,
    code: "SSH04SB",
    description: null,
    providers: "INGCO",
    uom: "paire",
    slug: "chaussure-securite-43-ingco",
    alert_stock: 12,
    optimal_stock: 24,
    real_quantity: 5,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 1,
    created_at: "2022-05-17T17:57:58.229537Z",
    created_by: 1,
    modified_at: "2022-06-01T15:21:07.259648Z",
    modified_by: 1,
    getReplenish: 19,
    getUom: "paire",
    get_category: "Divers",
  },
  {
    id: 326,
    name: "CHAUSSURE SECURITE 43 INGCO",
    prod_type: "storable",
    category: 2,
    code: "SSH08S1P",
    description: null,
    providers: "INGCO",
    uom: "paire",
    slug: "chaussure-securite-43-ingco-328412",
    alert_stock: 12,
    optimal_stock: 24,
    real_quantity: 6,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 1,
    created_at: "2022-05-17T17:57:58.252670Z",
    created_by: 1,
    modified_at: "2022-06-01T15:21:07.245967Z",
    modified_by: 1,
    getReplenish: 18,
    getUom: "paire",
    get_category: "Divers",
  },
  {
    id: 327,
    name: "CHAUSSURE SECURITE 44 INGCO",
    prod_type: "storable",
    category: 2,
    code: "SSH08S1P",
    description: null,
    providers: "INGCO",
    uom: "paire",
    slug: "chaussure-securite-44-ingco",
    alert_stock: 12,
    optimal_stock: 24,
    real_quantity: 0,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 1,
    created_at: "2022-05-17T17:57:58.257813Z",
    created_by: 1,
    modified_at: "2022-06-01T15:21:07.242343Z",
    modified_by: 1,
    getReplenish: 24,
    getUom: "paire",
    get_category: "Divers",
  },
  {
    id: 328,
    name: "CHAUSSURE SECURITE 45 INGCO",
    prod_type: "storable",
    category: 2,
    code: "SSH08S1P",
    description: null,
    providers: "INGCO",
    uom: "paire",
    slug: "chaussure-securite-45-ingco",
    alert_stock: 12,
    optimal_stock: 24,
    real_quantity: 3,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 1,
    created_at: "2022-05-17T17:57:58.262472Z",
    created_by: 1,
    modified_at: "2022-06-01T15:21:07.238713Z",
    modified_by: 1,
    getReplenish: 21,
    getUom: "paire",
    get_category: "Divers",
  },
  {
    id: 91,
    name: "CIMENT BLANC 25KG",
    prod_type: "storable",
    category: 14,
    code: null,
    description: null,
    providers: null,
    uom: "sac",
    slug: "ciment-blanc-25kg",
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 40,
    virtual_quantity: 0,
    unit_price: 1,
    unit_cost: 7000,
    created_at: "2022-05-07T17:00:19Z",
    created_by: 1,
    modified_at: "2022-06-01T15:17:25.602128Z",
    modified_by: 1,
    getReplenish: 0,
    getUom: "sac",
    get_category: "Carrelage",
  },
  {
    id: 57,
    name: "CIMENT BLANC 50KG",
    prod_type: "storable",
    category: 14,
    code: null,
    description: null,
    providers: "SODISMADCI SUCCURSALE 6",
    uom: "sac",
    slug: "ciment-blanc",
    alert_stock: 0,
    optimal_stock: 0,
    real_quantity: 1,
    virtual_quantity: 0,
    unit_price: 0,
    unit_cost: 15000,
    created_at: "2022-05-06T17:35:29Z",
    created_by: 1,
    modified_at: "2022-06-01T15:17:25.622928Z",
    modified_by: 1,
    getReplenish: 0,
    getUom: "sac",
    get_category: "Carrelage",
  },
]);

const initial = {
  items: [
    Object.defineProperty({}, "key", {
      value: token(),
    }),
  ],
};

async function addItem() {
  const group = getNode("myGroup");
  const form = getNode("myForm");
  group.walk((child) =>
    child.store.set(
      createMessage({
        key: "submitted",
        value: true,
        visible: false,
      })
    )
  );
  await group.settled;
  if (!group.ledger.value("blocking")) {
    const table = form.at("items");
    const row = {};
    group.each((child) => {
      row[child.name] = child.value;
    });
    table.input(table.value.concat([row]));
    group.reset();
  }
}
</script>

<template>
  <FormKit
    type="form"
    id="myForm"
    :value="initial"
    #default="{ value: formValues }"
  >
    <FormKit type="list" name="items" #default="{ value: rows }">
      <FormKit v-for="row in rows" :key="row.key" type="group">
        <div class="flex gap-x-4">
          <!-- <FormKit
            :type="combobox"
            name="article"
            label="Article"
            :options="products"
            validation="required"
            validation-visibility="submit"
          /> -->

          <FormKit
            :type="combobox2"
            name="article"
            label="Article"
            :options="products"
            validation="required"
            validation-visibility="submit"
          />

          <FormKit
            type="number"
            name="quantity"
            label="Quantité"
            validation="required"
            validation-visibility="submit"
          />

          <FormKit
            type="text"
            name="uom"
            label="Unité"
            validation="required"
            validation-visibility="submit"
          />

          <FormKit
            type="number"
            name="unit_cost"
            label="Prix unitaire"
            validation="required"
            validation-visibility="submit"
          />
        </div>
      </FormKit>
    </FormKit>

    <FormKit type="group" id="myGroup" :ignore="true">
      <FormKit type="button" label="Add row" @click="addItem" />
    </FormKit>

    <pre>{{ formValues }}</pre>
  </FormKit>
</template>
