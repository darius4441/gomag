import { defineStore } from "pinia";

export const useAuthStore = defineStore({
  id: "auth",
  state: () => ({
    user: {
      id: "",
      email: "",
      username: "",
      firstName: "",
      lastName: "",
      phoneNumber: "",
    },

    isAuthenticated: false,
    token: "",
  }),

  getters: {
    initializeStore: (state) => {
      if (localStorage.getItem("token")) {
        state.token = localStorage.getItem("token");
        state.isAuthenticated = true;

        state.user.email = localStorage.getItem("email");
        state.user.username = localStorage.getItem("username");
        state.user.id = localStorage.getItem("userid");
        state.user.firstName = localStorage.getItem("firstName");
        state.user.lastName = localStorage.getItem("lastName");
        state.user.phoneNumber = localStorage.getItem("phoneNumber");
      } else {
        state.user.id = "";
        state.user.email = "";
        state.user.username = "";
        state.user.firstName = "";
        state.user.lastName = "";
        state.user.phoneNumber = "";

        state.token = "";
        state.isAuthenticated = false;
      }
    },

    setToken: (state) => {
      return (token) => {
        state.token = token;
        state.isAuthenticated = true;
      };
    },

    removeToken: (state) => {
      state.user.id = "";
      state.user.email = "";
      state.user.username = "";
      state.user.firstName = "";
      state.user.lastName = "";
      state.user.phoneNumber = "";

      state.token = "";
      state.isAuthenticated = false;
    },

    setUser: (state) => {
      return (user) => {
        state.user = user;
      };
    },
  },
});
