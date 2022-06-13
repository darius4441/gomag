<script setup>
import { AcademicCapIcon } from "@heroicons/vue/outline";
import { toFormValidator } from "@vee-validate/zod";
import axios from "axios";
import { useField, useForm } from "vee-validate";
import { ref } from "vue-demi";
import { RouterLink, useRouter } from "vue-router";
import * as zod from "zod";

// access to store and router in composition mode
const route = useRouter();

const isLoading = ref(false);

const validationSchema = toFormValidator(
  zod.object({
    first_name: zod.string("champ obligatoire"),
    last_name: zod.string("champ obligatoire"),
    phone: zod.string("champ obligatoire").length(10),
    username: zod.string("champ obligatoire"),
    email: zod.string("Champ requis").email({ message: "Email non valide" }),
    password: zod.string("Champ requis").min(6, { message: "Trop court" }),
    // passwordForm: zod
    //   .object({
    //     password: zod.string("Champ requis").min(6, { message: "Trop court" }),
    //     confirm: zod.string(),
    //   })
    //   .refine((data) => data.password === data.confirm, {
    //     message: "Le mot de passe ne correspond pas !",
    //     path: ["confirm"],
    //   }),
  })
);

// Create a form context with the validation schema
const { handleSubmit, resetForm } = useForm({
  validationSchema: validationSchema,
});

const { value: first_name, errorMessage: f_nameError } = useField("first_name");
const { value: last_name, errorMessage: l_nameError } = useField("last_name");
const { value: phone, errorMessage: phoneError } = useField("phone");
const { value: username, errorMessage: usernameError } = useField("username");
const { value: email, errorMessage: emailError } = useField("email");
const { value: password, errorMessage: passwordError } = useField("password");

// Create Register function
const submitForm =
  isLoading.value == true
    ? null
    : handleSubmit(async () => {
        isLoading.value == true;

        const formData = {
          first_name: first_name.value,
          last_name: last_name.value,
          phone: phone.value,
          username: username.value,
          email: email.value,
          password: password.value,
        };

        try {
          await axios
            .post("/api/v1/usssaers/", formData)
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

        isLoading.value == false;
      });
</script>

<template>
  <div class="flex min-h-screen items-center justify-center bg-gray-100">
    <div class="mt-4 bg-white px-8 py-6 text-left shadow-lg">
      <div class="flex justify-center">
        <AcademicCapIcon class="h-20 w-20 text-blue-600" />
      </div>
      <h3 class="text-center text-2xl font-bold">Créer un nouveau compte</h3>
      <form>
        <div class="flex flex-row items-center justify-between gap-x-3">
          <span class="p-float-label mt-10 text-md text-slate-700">
            <PrimeInputText
              type="text"
              id="first-name"
              v-model:model-value="first_name"
              class="w-full"
              :class="{ 'p-invalid': f_nameError }"
            />

            <label for="first-name" class="text-md text-slate-700">Nom</label>
          </span>

          <span class="p-float-label mt-10 text-md text-slate-700">
            <PrimeInputText
              type="text"
              id="last-name"
              v-model:model-value="last_name"
              class="w-full"
              :class="{ 'p-invalid': l_nameError }"
            />

            <label for="last-name" class="text-md text-slate-700">Prenom</label>
          </span>
        </div>

        <span class="p-float-label mt-10 text-md text-slate-700">
          <PrimeInputMask
            type="text"
            id="phone"
            :unmask="true"
            mask="99 99 99 9999"
            autoClear
            v-model:model-value="phone"
            class="w-full"
            :class="{ 'p-invalid': phoneError }"
          />

          <label for="phone" class="text-md text-slate-700"
            >Numero de téléphone</label
          >
        </span>

        <span class="p-float-label mt-10 text-md text-slate-700">
          <PrimeInputText
            type="text"
            id="username"
            v-model:model-value="username"
            class="w-full"
            :class="{ 'p-invalid': usernameError }"
          />

          <label for="username" class="text-md text-slate-700"
            >Identifiant</label
          >
        </span>

        <span class="p-float-label mt-10 text-md text-slate-700">
          <PrimeInputText
            type="email"
            id="email"
            v-model:model-value="email"
            class="w-full"
            :class="{ 'p-invalid': emailError }"
          />

          <label for="email" class="text-md text-slate-700">Email</label>
        </span>

        <span class="p-float-label mt-10 text-md text-slate-700">
          <PrimeInputText
            type="password"
            id="password"
            v-model:model-value="password"
            class="w-full"
            :class="{ 'p-invalid': passwordError }"
          />

          <label for="password" class="text-md text-slate-700"
            >Mot de passe</label
          >
        </span>

        <!-- 
        <span class="p-float-label mt-10 text-md text-slate-700">
          <PrimeInputText
            type="password"
            id="confirm-password"
            v-model:model-value="confirmPassword"
            class="w-full"
            :class="{ 'p-invalid': confirmPasswordError }"
          />

          <label for="confirm-password" class="text-md text-slate-700"
            >Confirmer le mot de passe</label
          >
        </span>
 -->

        <div class="mt-4 flex items-baseline justify-between">
          <PrimeButton
            label="S'inscrire"
            @click="submitForm"
            class="p-button-info"
          />

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
