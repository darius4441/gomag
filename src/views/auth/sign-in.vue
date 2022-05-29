<script setup>
import { useRouter, RouterLink } from "vue-router";
import { useAuthStore } from "../../stores/auth";
import { useProductStore } from "../../stores/product";

import axios from "axios";
import * as zod from "zod";
import { AcademicCapIcon } from "@heroicons/vue/outline";
import { useForm } from "vee-validate";
import { toFormValidator } from "@vee-validate/zod";
import { useToast } from "vue-toast-notification";

import MyInput from "../../components/shared/forms/BaseInput.vue";
import MyButton from "../../components/shared/my-action.vue";

// access to store and router in composition mode
const route = useRouter();
const storeAuth = useAuthStore();
const toast = useToast();
const storeProduct = useProductStore();

const validationSchema = toFormValidator(
  zod.object({
    email: zod
      .string()
      .nonempty("Champ requis")
      .email({ message: "Email non valide" }),
    password: zod
      .string()
      .nonempty("Champ requis")
      .min(6, { message: "Trop court" }),
  })
);

const { handleSubmit, resetForm, errors } = useForm({
  validationSchema,
});

const onSubmit = handleSubmit(async (values) => {
  try {
    await axios
      .post("/api/v1/token/login/", values)
      .then((response) => {
        const token = response.data.auth_token;

        storeAuth.setToken(token);

        axios.defaults.headers.common["Authorization"] = "Token " + token;

        localStorage.setItem("token", token);
      })
      .catch((error) => {
        if (error.response) {
          for (const property in error.response.data) {
            toast.error(`${error.response.data[property]}`, {
              position: "top-right",
            });
          }
        } else if (error.message) {
          toast.error(JSON.stringify(error.message), { position: "top-right" });
        } else {
          toast.error(JSON.stringify(error), { position: "top-right" });
        }
      });

    await axios
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
        resetForm();
        route.push({ name: "Dashboard" });
      })
      .catch((error) => {
        toast.error(JSON.stringify(error.message), { position: "top-right" });
      });
  } catch (err) {
    toast.error("err: " + err + "\nerrors :" + errors, {
      position: "top-right",
    });
  }
});
</script>

<template>
  <div
    class="flex min-h-screen flex-col items-center justify-center bg-gray-100"
  >
    <div class="my-4 bg-white px-8 py-6 text-left shadow-lg">
      <div class="flex justify-center">
        <AcademicCapIcon class="h-20 w-20 text-blue-600" />
      </div>
      <h3 class="text-center text-2xl font-bold">
        Connecter vous à votre compte
      </h3>
      <form @submit.prevent="onSubmit">
        <MyInput
          type="email"
          name="email"
          placeholder="Email"
          wrapperclass="mt-4"
        />
        <MyInput
          type="password"
          name="password"
          placeholder="Mot de passe"
          wrapperclass="mt-4"
        />

        <!-- button group -->
        <div class="mt-4 flex items-baseline justify-between">
          <MyButton type="submit" label="Se connecter" />

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
