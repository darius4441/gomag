import { defineStore } from "pinia";
import { useLocalStorage } from "@vueuse/core";
import axios from "axios";

export const useOperationStore = defineStore({
  id: "operation",
  state: () => ({
    operations: [],
    operation: useLocalStorage("vueUseOperation", {}),
  }),

  actions: {
    async getOperations() {
      await axios
        .get("/api/v1/operations/")
        .then((response) => {
          for (let i = 0; i < response.data.length; i++) {
            this.operations.push(response.data[i]);
          }
        })
        .catch((error) => {
          console.log(JSON.stringify(error));
        });
    },

    async getOperation(id) {
      await axios
        .get(`/api/v1/operations/${id}`)
        .then((response) => {
          this.operation = response.data;
        })
        .catch((error) => {
          console.log(JSON.stringify(error));
        });
    },
  },
});
