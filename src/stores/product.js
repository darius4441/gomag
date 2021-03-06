import { useLocalStorage } from "@vueuse/core";
import axios from "axios";
import { defineStore } from "pinia";

export const useProductStore = defineStore({
  id: "product",
  state: () => ({
    products: useLocalStorage("vueUseProducts", []),
    product: {},
  }),

  actions: {
    async getProducts() {
      await axios
        .get("/api/v1/stock/products/")
        .then((response) => {
          this.products = response.data;
        })
        .catch((error) => {
          console.log(JSON.stringify(error));
        });
    },

    async getProduct(id) {
      await axios
        .get(`/api/v1/stock/products/${id}`)
        .then((response) => {
          this.product = response.data;
        })
        .catch((error) => {
          console.log(JSON.stringify(error));
        });
    },
  },
});
