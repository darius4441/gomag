import { ref } from "vue-demi";
import { useQuery } from "vue-query";
import axios from "axios";

export function useProducts(page: number, search: string) {
  const {
    data: products,
    isLoading,
    refetch,
  } = useQuery(
    "products",
    async () =>
      await axios
        .get(`/api/v1/stock/products/?page=${page}&search=${search}`)
        .then((response) => response.data),
    { staleTime: 60 * 1000 }
  );

  return { products, isLoading, refetch };
}
