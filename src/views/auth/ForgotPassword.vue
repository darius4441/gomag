<template>
  <div class="flex h-screen w-11/12 items-center justify-center lg:w-full">
    <form class="login">
      <p class="login-register">
        Don't have an account?
        <RouterLink :to="{ name: 'Register' }">Register</RouterLink>
      </p>
      <h2>Login to FireBlogs</h2>
      <div class="inputs">
        <div class="input">
          <input type="text" placeholder="Email" v-model="email" />
          <email class="icon" />
        </div>
        <div class="input">
          <input type="password" placeholder="Password" v-model="password" />
          <password class="icon" />
        </div>
        <div v-show="error" class="error">{{ this.errorMsg }}</div>
      </div>
      <RouterLink class="forgot-password" :to="{ name: 'ForgotPassword' }"
        >Forgot your password?</RouterLink
      >
      <button @click.prevent="signIn">Sign In</button>
      <div class="angle"></div>
    </form>
    <div class="background"></div>
  </div>
</template>

<script>
import { ref } from "vue-demi";
import { RouterLink } from "vue-router";
import firebase from "firebase/app";
import "firebase/auth";

export default {
  components: { RouterLink },

  setup() {
    // Create data / vars
    const email = ref(null);
    const error = ref(null);
    const errorMsg = ref(null);

    // Create Register function
    const resetPassword = async () => {
      if (email.value == "") {
        error.value = true;
        errorMsg.value = "Email requis";
        return;
      }
      await firebase
        .auth()
        .sendPasswordResetEmail(this.email)
        .then(() => {
          // this.modalMessage = "If your account exists, you will receive a email";
          // this.loading = false;
          // this.modalActive = true;
        })
        .catch((err) => {
          // this.modalMessage = err.message;
          // this.loading = false;
          // this.modalActive = true;
          error.value = true;
          errorMsg.value = err.message;
        });
    };

    return { email, resetPassword };
  },
};
</script>
