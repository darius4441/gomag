import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";

import Register from "../views/auth/sign-up.vue";
import Login from "../views/auth/sign-in.vue";
import Profile from "../views/auth/profile-screen.vue";

import Dashboard from "../views/dashboard-screen.vue";

import TestScreen from "../views/test-screen.vue";

import Settings from "../views/settings-screen.vue";

import Contacts from "../views/contact/contact-list.vue";
import SingleContact from "../views/contact/SingleContact.vue";
import EditContact from "../views/contact/EditContact.vue";
import CreateContact from "../views/contact/CreateContact.vue";
import DuplicateContact from "../views/contact/DuplicateContact.vue";

import Operations from "../views/operations/operation-list.vue";
import CreateOps from "../views/operations/CreateOps.vue";
import SingleOps from "../views/operations/SingleOps.vue";
import EditOps from "../views/operations/EditOps.vue";

import Stock from "../views/stock/Stock.vue";
import Products from "../views/stock/product-list.vue";
import SingleProduct from "../views/stock/SingleProduct.vue";
import CreateProduct from "../views/stock/CreateProduct.vue";
import DuplicateProduct from "../views/stock/duplicate-product-screen.vue";
import CreateMultipleProducts from "../views/stock/CreateMultipleProducts.vue";
import EditProduct from "../views/stock/edit-product.vue";

import Inventory from "../views/stock/Inventory.vue";
import CreateInventory from "../views/stock/CreateInventory.vue";
import SingleInv from "../views/stock/SingleInventory.vue";

import POS from "../views/pos/pos-screen.vue";

const routes = [
  // ? auth route area
  {
    path: "/register",
    name: "Register",
    component: Register,
    meta: {
      title: "S'inscrire",
    },
  },

  {
    path: "/login",
    name: "Login",
    component: Login,
    meta: {
      title: "Se connecter",
    },
  },

  {
    path: "/profile",
    name: "Profile",
    component: Profile,
    meta: {
      title: "Mon compte",
      requireLogin: true,
    },
  },

  // ? main route area
  {
    path: "/",
    name: "Dashboard",
    component: Dashboard,
    meta: {
      title: "Tableau de bord",
      requireLogin: true,
    },
  },

  {
    path: "/settings",
    name: "Settings",
    component: Settings,
    meta: {
      title: "Paramètre de l'entreprise",
      requireLogin: true,
    },
  },

  {
    path: "/ecran-test",
    name: "TestScreen",
    component: TestScreen,
    meta: {
      title: "Ecran de test",
      requireLogin: false,
    },
  },

  // ? contact route area
  {
    path: "/contacts",
    name: "Contacts",
    component: Contacts,
    meta: {
      title: "Contact",
      requireLogin: true,
    },
  },
  {
    path: "/contacts/:id",
    name: "SingleContact",
    component: SingleContact,
    meta: {
      title: "Détail Contact",
      requireLogin: true,
    },
  },
  {
    path: "/contacts/:id/edit",
    name: "EditContact",
    component: EditContact,
    meta: {
      title: "Mise à jour Contact",
      requireLogin: true,
    },
  },
  {
    path: "/contacts/create",
    name: "CreateContact",
    component: CreateContact,
    meta: {
      title: "Nouveau contact",
      requireLogin: true,
    },
  },
  {
    path: "/contacts/create",
    name: "DuplicateContact",
    component: DuplicateContact,
    meta: {
      title: "Nouveau contact",
      requireLogin: true,
    },
  },

  // ? operation route area
  {
    path: "/operations",
    name: "Operations",
    component: Operations,
    meta: {
      title: "Entrées - Sorties",
      requireLogin: true,
    },
  },
  {
    path: "/operations/:id",
    name: "SingleOps",
    component: SingleOps,
    meta: {
      title: "Détail Opération",
      requireLogin: true,
    },
  },
  {
    path: "/operations/:id/edit",
    name: "EditOps",
    component: EditOps,
    meta: {
      title: "Mise à jour Opération",
      requireLogin: true,
    },
  },
  {
    path: "/operations/create",
    name: "CreateOps",
    component: CreateOps,
    meta: {
      title: "Nouvelle Opération",
      requireLogin: true,
    },
  },

  // ? inventory route area
  {
    path: "/stock",
    name: "Stock",
    component: Stock,
    meta: {
      title: "Votre stock",
      requireLogin: true,
    },
  },
  {
    path: "/stock/inventory",
    name: "Inventory",
    component: Inventory,
    meta: {
      title: "Espace inventaire",
      requireLogin: true,
    },
  },
  {
    path: "/stock/inventory/create",
    name: "CreateInventory",
    component: CreateInventory,
    meta: {
      title: "Nouveau inventaire",
      requireLogin: true,
    },
  },
  {
    path: "/stock/inventory/:id",
    name: "SingleInv",
    component: SingleInv,
    meta: {
      title: "Détail Inventaire",
      requireLogin: true,
    },
  },

  // ? product route area
  {
    path: "/stock/products",
    name: "Products",
    component: Products,
    meta: {
      title: "Liste des produits",
      requireLogin: true,
    },
  },
  {
    path: "/stock/products/:id",
    name: "SingleProduct",
    component: SingleProduct,
    meta: {
      title: "Détail Produit",
      requireLogin: true,
    },
  },
  {
    path: "/stock/products/create",
    name: "CreateProduct",
    component: CreateProduct,
    meta: {
      title: "Création de produit",
      requireLogin: true,
    },
  },
  {
    path: "/stock/products/create",
    name: "DuplicateProduct",
    component: DuplicateProduct,
    meta: {
      title: "Création de produit",
      requireLogin: true,
    },
  },
  {
    path: "/stock/products/create-multiple",
    name: "CreateMultipleProducts",
    component: CreateMultipleProducts,
    meta: {
      title: "Création multiple de produits",
      requireLogin: true,
    },
  },
  {
    path: "/stock/products/:id/edit",
    name: "EditProduct",
    component: EditProduct,
    meta: {
      title: "Mise à jour Produit",
      requireLogin: true,
    },
  },

  // ? pos route area
  {
    path: "/pos",
    name: "POS",
    component: POS,
    meta: {
      title: "POS",
      requireLogin: true,
    },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  document.title = `${to.meta.title} | GoMag`;
  const store = useAuthStore();

  if (
    to.matched.some((record) => record.meta.requireLogin) &&
    !store.isAuthenticated
  ) {
    next({ name: "Login" });
  } else {
    next();
  }
});

export default router;
