<script setup>
import {
  Disclosure,
  DisclosureButton,
  DisclosurePanel,
  MenuButton,
  MenuItem,
} from "@headlessui/vue";
import {
  AdjustmentsIcon,
  CheckCircleIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  ChevronUpIcon,
} from "@heroicons/vue/solid";
import { useLocalStorage } from "@vueuse/core";
import axios from "axios";
import moment from "moment/min/moment-with-locales";
import { useToast } from "primevue/usetoast";
import { onMounted, ref } from "vue-demi";
import { useRoute, useRouter } from "vue-router";
import Card from "../../components/shared/card-component.vue";
import BaseModal from "../../components/shared/modals/BaseModal.vue";
import MyButton from "../../components/shared/my-action.vue";
import MyMenu from "../../components/shared/my-menu.vue";
import { useTempStore } from "../../stores/temp";

moment.locale("fr");

//? declare composables
const route = useRoute();
const router = useRouter();
const storePage = useTempStore();
const toast = useToast();

//? declare vars / consts
const contactID = route.params.id;
const contact = ref({});
const contactHistory = ref([]);
const archiveDeletionModalTitle = ref("");
const isShowArchiveDeletionModal = ref(false);

//? declare functions
async function getContact() {
  await axios
    .get(`/api/v1/contacts/${contactID}`)
    .then((response) => {
      contact.value = response.data;
    })
    .catch((error) => {
      console.log(JSON.stringify(error));
    });
}

async function getContactHistory() {
  await axios
    .get(`/api/v1/operations/?contact__id=${contactID}`)
    .then((response) => {
      contactHistory.value = response.data.results;
      // console.log(response.data);
    })
    .catch((error) => {
      console.log(JSON.stringify(error));
    });
}

async function goToEditPage() {
  useLocalStorage("vueUseContact", contact.value);
  router.push({ name: "EditContact", params: { id: contactID } });
}

function goToDuplicatePage() {
  localStorage.setItem("vueUseDuplicateContact", JSON.stringify(contact.value));

  router.push({ name: "DuplicateContact" });
}

async function archiveContact() {
  try {
    await axios
      .patch(`api/v1/contact/${contactID}/`, { isArchived: true })
      .then(() => {
        toast.add({
          severity: "success",
          summary: "Archivage",
          detail: "Contact archivé avec succès",
          life: 3000,
        });

        router.push({ name: "Contacts" });
      })
      .catch((e) => {
        throw e;
      });
  } catch (error) {
    let displayMessage;

    switch (error.message) {
      case "Network Error":
        displayMessage = "Problème de connexion avec la base de donnée";
        break;

      default:
        displayMessage = error.message;
        break;
    }

    toast.add({
      severity: "error",
      summary: "Une erreur s'est produite",
      detail: displayMessage,
      life: 3000,
    });
  }
}

async function deleteContact() {
  try {
    await axios
      .delete(`api/v1/contacts/${contactID}/`)
      .then(() => {
        toast.add({
          severity: "success",
          summary: "Suppression",
          detail: "Contact supprimer avec succès",
          life: 3000,
        });

        router.push({ name: "Contacts" });
      })
      .catch((e) => {
        throw e;
      });
  } catch (error) {
    let displayMessage;

    switch (error.message) {
      case "Network Error":
        displayMessage = "Problème de connexion avec la base de donnée";
        break;

      case "Request failed with status code 500":
        displayMessage =
          "Impossible de supprimer cet article, veillez l'archiver";
        break;

      default:
        displayMessage = error.message;
        break;
    }

    toast.add({
      severity: "error",
      summary: "Une erreur s'est produite",
      detail: displayMessage,
      life: 3000,
    });
  }
}

function enableArchiveDeletionModal(title) {
  isShowArchiveDeletionModal.value = true;
  archiveDeletionModalTitle.value = title;
}

const trueType = (val) => {
  switch (val) {
    case "company":
      return "Entreprise";

    case "deliver":
      return "Livreur";

    case "client":
      return "Client";

    default:
      return "Client";
  }
};

const getFormattedTime = (date) => {
  return moment(date).startOf("day").fromNow();
};

const trueGender = (val) => {
  switch (val) {
    case "mr":
      return "Monsieur";

    case "mme":
      return "Madame";

    default:
      return "Monsieur";
  }
};

onMounted(async () => {
  storePage.updatePageName("Contacts");

  await getContact();
  await getContactHistory();
});
</script>

<template>
  <div class="flex flex-row">
    <PrimeToast />

    <div class="basis-3/5">
      <div class="flex flex-col">
        <!-- Header -->
        <div
          class="mx-auto flex w-full flex-row items-end justify-between px-4"
        >
          <div>
            <div class="mb-1 flex flex-row items-end">
              <router-link
                :to="{ name: 'Contacts' }"
                class="cursor-pointer text-kSecondaryColor hover:underline"
                >Contacts</router-link
              >
              <span class="mx-1">/</span>
              <span class="text-sm">{{ contact.name }}</span>
            </div>
            <div class="flex flex-row items-center">
              <MyButton label="Modifier" @click="goToEditPage" />

              <MyButton label="Créer" to="CreateContact" :isOutlined="true" />
            </div>
          </div>

          <div class="flex flex-row items-center">
            <MyMenu>
              <template #menu_button>
                <MenuButton>
                  <div
                    class="rounded-lg px-2 py-1 hover:bg-kPrimaryColor hover:text-kWhiteColor"
                  >
                    <AdjustmentsIcon class="inline-block h-4 w-4" />
                    <span class="ml-2">option</span>
                  </div>
                </MenuButton>
              </template>

              <template #menu_content>
                <MenuItem>
                  <button
                    @click="enableArchiveDeletionModal('archiver')"
                    class="mt-1 cursor-pointer rounded-lg px-3 hover:bg-kPrimaryColor hover:text-kWhiteColor"
                  >
                    Archiver
                  </button>
                </MenuItem>
                <MenuItem>
                  <button
                    @click="goToDuplicatePage"
                    class="mt-1 rounded-lg px-3 hover:bg-kPrimaryColor hover:text-kWhiteColor"
                  >
                    Dupliquer
                  </button>
                </MenuItem>
                <MenuItem>
                  <button
                    @click="enableArchiveDeletionModal('supprimer')"
                    class="mt-1 rounded-lg px-3 hover:bg-kPrimaryColor hover:text-kWhiteColor"
                  >
                    Supprimer
                  </button>
                </MenuItem>
              </template>
            </MyMenu>
          </div>

          <div class="flex flex-row items-center gap-x-4">
            <span class="text-sm">num/len</span>
            <div>
              <ChevronLeftIcon class="inline-block h-5 w-5" />
              <ChevronRightIcon class="inline-block h-5 w-5" />
            </div>
          </div>
        </div>

        <!-- modals conditional display -->
        <BaseModal
          :isOpen="isShowArchiveDeletionModal"
          overlay_bg="bg-red-600/70"
          @closeModal="isShowArchiveDeletionModal = false"
        >
          <template #dialog_title>Confirmation</template>
          <template #dialog_content
            >Voulez vous réellement {{ archiveDeletionModalTitle }} ce contact
            ?</template
          >
          <template #dialog_footer>
            <div class="flex flex-row">
              <MyButton
                label="OUI"
                :isOutlined="false"
                @click="
                  archiveDeletionModalTitle === 'supprimer'
                    ? deleteContact
                    : archiveContact
                "
              />
              <MyButton
                label="NON"
                :isOutlined="true"
                @click="isShowArchiveDeletionModal = false"
              />
            </div>
          </template>
        </BaseModal>

        <Card>
          <template #content>
            <div class="my-4">
              <!-- name and photo input -->
              <div class="mb-1 flex w-full flex-row items-end gap-x-12">
                <div class="w-5/6">
                  <span class="mb-2 block text-sm font-medium">
                    Nom du contact
                  </span>
                  <div
                    class="block w-full rounded-lg border bg-kPrimaryColor/25 p-1 text-sm font-bold tracking-wide"
                  >
                    {{ contact.name }}
                  </div>
                </div>
                <div
                  class="dark:bg-kBgColor h-24 w-24 rounded-lg border border-gray-300 bg-kPrimaryColor/25"
                >
                  <span>photo</span>
                </div>
              </div>

              <!-- other input -->
              <div>
                <span for="category" class="mb-2 block text-sm font-medium">
                  Genre
                </span>

                <div
                  class="block w-full rounded-lg border bg-kPrimaryColor/25 p-1 text-sm font-bold tracking-wide"
                >
                  {{ trueGender(contact.gender) }}
                </div>
              </div>
              <div>
                <span for="category" class="mb-2 block text-sm font-medium">
                  Type de contact
                </span>
                <div
                  class="block w-full rounded-lg border bg-kPrimaryColor/25 p-1 text-sm font-bold tracking-wide"
                >
                  {{ trueType(contact.c_type) }}
                </div>
              </div>

              <div>
                <span for="code" class="mb-2 block text-sm font-medium">
                  De l'entreprise
                </span>
                <div
                  class="block h-7 w-full rounded-lg border bg-kPrimaryColor/25 p-1 text-sm font-bold tracking-wide"
                >
                  {{ contact.getCompanyName }}
                </div>
              </div>
            </div>
          </template>
        </Card>
      </div>
    </div>

    <div class="basis-2/5">
      <h3>Historique</h3>

      <div v-if="contactHistory.length" class="w-full pt-5">
        <div
          v-for="(history, idx) in contactHistory"
          :key="idx"
          class="mx-auto mt-2 w-full max-w-md rounded-2xl bg-white"
        >
          <Disclosure v-slot="{ open }">
            <DisclosureButton
              class="flex w-full justify-between rounded-lg bg-kPrimaryColor/30 px-4 py-2 text-left text-sm font-medium text-kPrimaryColor hover:bg-kPrimaryColor/50 focus:outline-none focus-visible:ring focus-visible:ring-purple-500 focus-visible:ring-opacity-75"
            >
              <span>{{ getFormattedTime(history.date) }}</span>
              <ChevronUpIcon
                :class="open ? 'rotate-180 transform' : ''"
                class="h-5 w-5 text-kPrimaryColor"
              />
            </DisclosureButton>
            <DisclosurePanel
              class="max-h-64 overflow-y-auto px-4 pt-4 pb-2 text-sm"
            >
              <div
                v-for="(item, i) in history.items"
                :key="i"
                class="flex items-center"
              >
                <CheckCircleIcon class="mr-2 h-3 w-3 text-emerald-600" />
                <span class="truncate">
                  <span class="font-bold"
                    >{{ parseFloat(item.quantity) }} {{ item.unit }}</span
                  >
                  de
                  {{ item.get_article_name }}
                </span>
              </div>
            </DisclosurePanel>
          </Disclosure>
        </div>
      </div>
    </div>
  </div>
</template>
