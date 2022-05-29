import { defineStore } from "pinia";

export const useTempStore = defineStore({
  id: "temporary",
  state: () => ({
    pageName: "",
  }),

  getters: {
    updatePageName: (state) => {
      return (name) => {
        state.pageName = name;
      };
    },
  },
});
