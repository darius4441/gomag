<script setup>
import { AcademicCapIcon } from "@heroicons/vue/outline";
import { toFormValidator } from "@vee-validate/zod";
import axios from "axios";
import { useToast } from "primevue/usetoast";
import { useField, useForm } from "vee-validate";
import { useRouter } from "vue-router";
import * as zod from "zod";
import { useAuthStore } from "../../stores/auth";
import { useProductStore } from "../../stores/product";

// access to store and router in composition mode
const route = useRouter();
const storeAuth = useAuthStore();
const toast = useToast();
const storeProduct = useProductStore();

const validationSchema = toFormValidator(
  zod.object({
    email: zod.string().email("Email non valide"),
    password: zod.string({ required_error: "Champ requis" }),
  })
);

// Create a form context with the validation schema
const { handleSubmit } = useForm({
  validationSchema: validationSchema,
});

const { value: email, errorMessage: emailError } = useField("email");
const { value: password, errorMessage: passwordError } = useField("password");

const submitForm = handleSubmit(async () => {
  const formData = { email: email.value, password: password.value };
  try {
    await axios
      .post("/api/v1/token/login/", formData)
      .then((response) => {
        const token = response.data.auth_token;

        storeAuth.setToken(token);

        axios.defaults.headers.common["Authorization"] = "Token " + token;

        localStorage.setItem("token", token);

        axios
          .get("/api/v1/users/me")
          .then((response) => {
            storeAuth.setUser({
              id: response.data.id,
              email: response.data.email,
              username: response.data.username,
              firstName: response.data.first_name,
              lastName: response.data.last_name,
              phoneNumber: response.data.phone,
            });

            localStorage.setItem("userid", response.data.id);
            localStorage.setItem("email", response.data.email);
            localStorage.setItem("username", response.data.username);
            localStorage.setItem("firstName", response.data.first_name);
            localStorage.setItem("lastName", response.data.last_name);
            localStorage.setItem("phoneNumber", response.data.phone);

            storeProduct.getProducts;

            // Reset form data and go to Dashboard
            route.push({ name: "Dashboard" });
          })
          .catch((error) => {
            throw error.message;
          });
      })
      .catch((error) => {
        if (error.response) {
          for (const property in error.response.data) {
            throw `${error.response.data[property]}`;
          }
        } else if (error.message) {
          throw JSON.stringify(error.message);
        } else {
          JSON.stringify(error);
        }
      });
  } catch (err) {
    toast.add({
      severity: "error",
      summary: "Une erreur s'est produite",
      detail: "err: " + err + "\nerrors :" + err,
      life: 3000,
    });
  }
});
</script>

<template>
  <div
    class="flex min-h-screen flex-col items-center justify-center bg-gray-100"
  >
    <PrimeToast />

    <div class="my-4 bg-white px-8 py-6 text-left shadow-lg">
      <div class="flex justify-center">
        <AcademicCapIcon class="h-20 w-20 text-blue-600" />
      </div>
      <h3 class="text-center text-2xl font-bold">
        Connecter vous à votre compte
      </h3>
      <form>
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
            @keydown.enter="submitForm"
            class="w-full"
            :class="{ 'p-invalid': passwordError }"
          />

          <label for="password" class="text-md text-slate-700"
            >Mot de passe</label
          >
        </span>

        <!-- button group -->
        <div class="mt-4 flex items-baseline justify-between">
          <PrimeButton
            label="Se connecter"
            @click="submitForm"
            class="p-button-info"
          />

          <div class="flex flex-col">
            <RouterLink
              :to="{ name: 'Dashboard' }"
              class="cursor-pointer text-sm text-blue-600 hover:underline"
            >
              Mot de passe oublié
            </RouterLink>
            <p class="my-2 text-xs tracking-tighter">ou</p>
            <RouterLink
              :to="{ name: 'Register' }"
              class="cursor-pointer text-sm text-blue-600 hover:underline"
            >
              s'inscrire ici
            </RouterLink>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>
