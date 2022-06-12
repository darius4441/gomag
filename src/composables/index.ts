import axios from "axios";
import { useQuery } from "vue-query";

const getProduct = async (id: number) => {
  const response = await axios
    .get(`/api/v1/stock/products/${id}`)
    .then((res) => res.data);

  return response;
};

const getProducts = async () => {
  const response = await axios
    .get("api/v1/stock/products")
    .then((res) => res.data);

  return response;
};

export function useProduct(id: number) {
  const { data: product, isLoading } = useQuery(
    ["product", id],
    async () => await getProduct(id),
    {
      staleTime: 120 * 1000,
    }
  );

  return {
    product,
    isLoading,
  };
}

export function useProducts() {
  const { data: products, isLoading } = useQuery(
    "products",
    async () => await getProducts(),
    {
      staleTime: 120 * 1000,
    }
  );

  return {
    products,
    isLoading,
  };
}
