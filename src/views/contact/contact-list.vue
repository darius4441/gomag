<script setup>
import axios from "axios";
import { ref, onMounted } from "vue-demi";
import { useTempStore } from "../../stores/temp";

import companyPic from "@/assets/images/default/company_default.png";
import deliverPic from "@/assets/images/default/deliver.png";
import malePic from "@/assets/images/default/male.png";
import femalePic from "@/assets/images/default/female.png";

import MyCard from "../../components/shared/card-component.vue";

// init utils composables to variables
const pageStore = useTempStore();

// declare vars/consts
const contacts = ref("");

// declare functions
async function getContacts() {
  await axios.get("api/v1/contacts/").then((res) => {
    contacts.value = res.data;
  });
}

const getCorrectPhoto = (contact) => {
  switch (contact.c_type) {
    case "company":
      return companyPic;

    case "deliver":
      return deliverPic;

    case "client":
      return contact.gender === "mr" ? malePic : femalePic;

    default:
      return malePic;
  }
};

onMounted(async () => {
  pageStore.updatePageName("Contacts");

  await getContacts();
});
</script>

<template>
  <div>
    <MyCard>
      <template #title>
        <h1 class="basis-1/2 text-sm">Liste des contacts</h1>
      </template>

      <template #content>
        <div class="m-4 flex flex-wrap gap-4">
          <router-link
            v-for="(contact, idx) in contacts"
            :key="idx"
            :to="{ name: 'SingleContact', params: { id: contact.id } }"
            class="relative h-32 w-32 cursor-pointer rounded bg-white shadow-lg ring-1 ring-kPrimaryColor duration-300 hover:-translate-y-2"
          >
            <img :src="getCorrectPhoto(contact)" alt="person" />
            <div
              class="absolute bottom-0 w-full bg-white p-1 shadow-inner shadow-kPrimaryColor"
            >
              <p class="truncate">{{ contact.name }}</p>
            </div>
          </router-link>
        </div>
      </template>
    </MyCard>
  </div>
</template>
