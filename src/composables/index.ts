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
  isAlert: Boolean;
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
  let existProvider: String[] = [];

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
    staleTime: 300 * 1000,
  });

  return {
    product,
    isLoading,
    refetch,
  };
}

export function useProducts() {
  const {
    data: products,
    isLoading,
    refetch,
  } = useQuery("products", async () => await getProducts(), {
    staleTime: 300 * 1000,
  });

  return {
    products,
    isLoading,
    refetch,
  };
}

//? ***************** operations query space *******************

interface Item {
  id: Number;
  article: Number;
  quantity: Number;
  unit: String;
  old_qty: Number;
  cost: Number | undefined | null;
  get_article_name: String;
  get_article_available_qty: Number;
}
interface Operation {
  id: Number;
  getContactName: String;
  m_type: String;
  annexe: String | undefined | null;
  date: Date;
  state: String;
  items: Item[];
}

const getOperation = async (id: number) => {
  const response = await axios
    .get(`/api/v1/operations/${id}`)
    .then((res) => res.data);

  return response;
};

const getOperations = async () => {
  const response = await axios.get("api/v1/operations").then((res) => {
    var operationList: Operation[] = [];

    res.data.forEach((el: Operation) => {
      el.date = new Date(el.date);
      operationList.push(el);
    });

    return operationList;
  });

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

//? ***************** staff query space *******************
interface Employee {
  id: Number;
  username: String;
  first_name: String;
  last_name: String;
  phone: String;
  email: String;
}

const getEmployee = async (id: number) => {
  const response = await axios
    .get(`/api/v1/users/${id}`)
    .then((res) => res.data);

  return response;
};

const getEmployees = async () => {
  const response = await axios.get("api/v1/users").then((res) => {
    return res.data;
  });

  return response;
};

export function useEmployee(id: number) {
  const {
    data: employee,
    isLoading,
    refetch,
  } = useQuery(["employee", id], async () => await getEmployee(id), {
    staleTime: 120 * 1000,
  });

  return {
    employee,
    isLoading,
    refetch,
  };
}

export function useEmployees() {
  const { data: employees, isLoading } = useQuery(
    "employees",
    async () => await getEmployees(),
    {
      staleTime: 10 * 60 * 1000, // min * second * millisecond
    }
  );

  return {
    employees,
    isLoading,
  };
}
