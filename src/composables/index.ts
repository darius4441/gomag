import axios from "axios";
import { useQuery } from "vue-query";

//? ***************** products query space *******************
interface Product {
  id: Number;
  name: String;
  prod_type: String;
  isArchived: String;
  category: Number;
  code: String;
  description: String;
  providers: String;
  uom: String;
  slug: String;
  alert_stock: Number;
  optimal_stock: Number;
  real_quantity: Number;
  virtual_quantity: Number;
  unit_price: Number;
  semi_wholesale_price: Number;
  wholesale_price: Number;
  unit_cost: Number;
  created_at: Date;
  created_by: Number;
  modified_at: Date;
  modified_by: Number;
  getReplenish: String;
  getUom: String;
  get_category: String;
}

const getProduct = async (id: number) => {
  const response = await axios
    .get(`/api/v1/stock/products/${id}`)
    .then((res) => res.data);

  return response;
};

const getProducts = async () => {
  const response = await axios.get("api/v1/stock/products").then((res) => {
    var productList: Product[] = [];

    res.data.forEach((el: Product) => {
      el.created_at = new Date(el.created_at);
      el.modified_at = new Date(el.modified_at);

      productList.push(el);
    });

    return productList;
  });

  return response;
};

export function useProduct(id: number) {
  const {
    data: product,
    isLoading,
    refetch,
  } = useQuery(["product", id], async () => await getProduct(id), {
    staleTime: 120 * 1000,
  });

  return {
    product,
    isLoading,
    refetch,
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

//? ***************** operations query space *******************
interface Operation {
  id: Number;
  contact: Number;
  m_type: String;
  date: Date;
  annexe: String;
  state: String;
  items: Product[];
  getContactName: String;
}

const getOperation = async (id: number) => {
  const response = await axios
    .get(`/api/v1/operations/${id}`)
    .then((res) => res.data);

  return response;
};

const getOperations = async () => {
  const response = await axios.get("api/v1/operations").then((res) => res.data);

  return response;
};

export function useOperation(id: number) {
  const {
    data: operation,
    isLoading,
    refetch,
  } = useQuery(["operation", id], async () => await getOperation(id), {
    staleTime: 120 * 1000,
  });

  return {
    operation,
    isLoading,
    refetch,
  };
}

export function useOperations() {
  const { data: operations, isLoading } = useQuery(
    "operations",
    async () => await getOperations(),
    {
      staleTime: 120 * 1000,
    }
  );

  return {
    operations,
    isLoading,
  };
}
