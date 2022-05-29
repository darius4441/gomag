<script setup>
import { useRouter, RouterLink } from "vue-router";
import axios from "axios";
import * as zod from "zod";
import { AcademicCapIcon } from "@heroicons/vue/outline";
import { useForm } from "vee-validate";
import { toFormValidator } from "@vee-validate/zod";

import MyInput from "../../components/shared/forms/BaseInput.vue";
import MyButton from "../../components/shared/my-action.vue";

// access to store and router in composition mode
const route = useRouter();

const validationSchema = toFormValidator(
  zod.object({
    first_name: zod.string().nonempty("champ obligatoire"),
    last_name: zod.string().nonempty("champ obligatoire"),
    phone: zod.string().nonempty("champ obligatoire").length(10),
    username: zod.string().nonempty("champ obligatoire"),
    email: zod
      .string()
      .nonempty("Champ requis")
      .email({ message: "Email non valide" }),

    passwordForm: zod
      .object({
        password: zod
          .string()
          .nonempty("Champ requis")
          .min(6, { message: "Trop court" }),
        confirm: zod.string(),
      })
      .refine((data) => data.password === data.confirm, {
        message: "Le mot de passe ne correspond pas !",
        path: ["confirm"],
      }),
  })
);

// Create a form context with the validation schema
const { handleSubmit, resetForm } = useForm({
  validationSchema: validationSchema,
});

// Create Register function
const onSubmit = handleSubmit(async (values) => {
  try {
    await axios
      .post("/api/v1/users/", values)
      .then(() => {
        resetForm();
        route.push({ name: "Login" });
      })
      .catch((error) => {
        throw error;
      });
  } catch (err) {
    console.log(JSON.stringify(err));
  }
});
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-100">
    <div class="mt-4 bg-white px-8 py-6 text-left shadow-lg">
      <div class="flex justify-center">
        <AcademicCapIcon class="h-20 w-20 text-blue-600" />
      </div>
      <h3 class="text-center text-2xl font-bold">Créer un nouveau compte</h3>
      <form @submit.prevent="onSubmit">
        <div class="flex flex-row items-center justify-between gap-x-3">
          <!-- firstname field -->
          <MyInput
            type="text"
            placeholder="Nom"
            name="first_name"
            wrapperclass="mt-4"
          />

          <!-- lastname field -->
          <MyInput
            type="text"
            placeholder="Prenom"
            name="last_name"
            wrapperclass="mt-4"
          />
        </div>

        <!-- phone number field -->
        <MyInput
          type="text"
          placeholder="Numero de téléphone"
          name="phone"
          wrapperclass="mt-4"
        />

        <!-- username field -->
        <MyInput
          type="text"
          placeholder="Identifiant"
          name="username"
          wrapperclass="mt-4"
        />

        <!-- email field -->
        <MyInput
          type="email"
          placeholder="Email"
          name="email"
          wrapperclass="mt-4"
        />

        <!-- password field -->
        <MyInput
          type="password"
          placeholder="Mot de passe"
          name="password"
          wrapperclass="mt-4"
        />

        <!-- confirmPassword field -->
        <MyInput
          type="password"
          placeholder="Repeter le mot de passe"
          name="confirm_password"
          wrapperclass="mt-4"
        />

        <!-- button group -->
        <div class="mt-4 flex items-baseline justify-between">
          <MyButton type="submit" label="S'inscrire" />
          <RouterLink
            :to="{ name: 'Login' }"
            class="text-sm text-blue-600 hover:underline"
          >
            Connectez-vous ici
          </RouterLink>
        </div>
      </form>
    </div>
  </div>
</template>
