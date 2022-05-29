<script setup>
import { ref, onMounted, onUnmounted } from "vue-demi";
import { useTempStore } from "../../stores/temp";
import { useRouter } from "vue-router";

import axios from "axios";
import * as zod from "zod";
import { toFormValidator } from "@vee-validate/zod";
import { useForm } from "vee-validate";
import { useToast } from "vue-toast-notification";

import MyButton from "../../components/shared/my-action.vue";
import MyInput from "../../components/shared/forms/BaseInput.vue";
import Card from "../../components/shared/card-component.vue";

// init utils composables to variables
const pageStore = useTempStore();
const router = useRouter();
const toast = useToast();

// declare vars/consts
const contact = JSON.parse(localStorage.getItem("vueUseContact"));

const genderOptions = ref([
  { value: "mr", label: "Monsieur" },
  { value: "mme", label: "Madame" },
]);

const typeOptions = ref([
  { value: "company", label: "Entreprise" },
  { value: "deliver", label: "Livreur" },
  { value: "client", label: "Client" },
]);

const validationSchema = toFormValidator(
  zod.object({
    name: zod
      .string({
        required_error: "le nom est obligatoire",
      })
      .min(3, { message: "le nom doit avoir 3 charactère minimum" }),
    gender: zod.string({
      required_error: "le genre est obligatoire",
    }),
    company: zod.number().nullish(),
    c_type: zod.string({
      required_error: "le type de contact est obligatoire",
    }),
  })
);

const { handleSubmit, resetForm } = useForm({
  validationSchema: validationSchema,

  initialValues: {
    name: contact.name,
    gender: contact.gender,
    c_type: contact.c_type,
    company: contact.company,
  },
});

// declare functions
function onInvalidSubmit({ errors }) {
  Object.entries(errors).forEach((item) => {
    toast.error(item[1], {
      position: "top-right",
    });
  });
}

const onSubmit = handleSubmit(async (values) => {
  try {
    await axios
      .patch(`/api/v1/contacts/${contact.id}/`, values)
      .then(() => {
        resetForm();

        toast.success("Contact modifié avec succès", {
          position: "top-right",
        });

        router.push({
          name: "SingleContact",
          params: { id: contact.id },
        });
      })
      .catch((e) => {
        throw e;
      });
  } catch (error) {
    toast.error(error.message, {
      position: "top-right",
    });
  }
}, onInvalidSubmit);

onMounted(async () => {
  pageStore.updatePageName("Contacts");
});

onUnmounted(() => {
  localStorage.removeItem("vueUseContact");
});
</script>

<template>
  <div>
    <!-- Header -->
    <div class="mx-auto w-full px-4">
      <div class="flex w-full flex-row items-center">
        <MyButton label="Sauver" @click="onSubmit" />
        <MyButton label="Annuler" to="Contacts" :isOutlined="true" />
      </div>
    </div>

    <Card>
      <template #title>
        <h1>
          Modification du contact
          <span class="underline">{{ contact.name }}</span>
        </h1>
      </template>

      <template #content>
        <form class="py-6">
          <MyInput type="text" name="name" label="Nom complet" class="mt-4" />
          <MyInput
            type="select"
            name="gender"
            label="Genre"
            :options="genderOptions"
            class="mt-4"
          />
          <MyInput
            type="select"
            name="c_type"
            label="Type de contact"
            :options="typeOptions"
            class="mt-4"
          />
          <MyInput type="text" name="company" label="Entreprise" class="mt-4" />
        </form>
      </template>
    </Card>
  </div>
</template>
