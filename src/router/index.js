import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";

const routes = [
  // ? auth route area
  {
    path: "/register",
    name: "Register",
    component: () => import("../views/auth/sign-up.vue"),
    meta: {
      title: "S'inscrire",
    },
  },

  {
    path: "/login",
    name: "Login",
    component: () => import("../views/auth/sign-in.vue"),
    meta: {
      title: "Se connecter",
    },
  },

  {
    path: "/profile",
    name: "Profile",
    component: () => import("../views/auth/profile-screen.vue"),
    meta: {
      title: "Mon compte",
      requireLogin: true,
    },
  },

  // ? main route area
  {
    path: "/",
    name: "Dashboard",
    component: () => import("../views/dashboard-screen.vue"),
    meta: {
      title: "Tableau de bord",
      requireLogin: true,
    },
  },

  {
    path: "/settings",
    name: "Settings",
    component: () => import("../views/settings-screen.vue"),
    meta: {
      title: "Paramètre de l'entreprise",
      requireLogin: true,
    },
  },

  {
    path: "/ecran-test",
    name: "TestScreen",
    component: () => import("../views/test-screen.vue"),
    meta: {
      title: "Ecran de test",
      requireLogin: false,
    },
  },

  // ? contact route area
  {
    path: "/contacts",
    name: "Contacts",
    component: () => import("../views/contact/contact-list.vue"),
    meta: {
      title: "Contact",
      requireLogin: true,
    },
  },
  {
    path: "/contacts/:id",
    name: "SingleContact",
    component: () => import("../views/contact/SingleContact.vue"),
    meta: {
      title: "Détail Contact",
      requireLogin: true,
    },
  },
  {
    path: "/contacts/:id/edit",
    name: "EditContact",
    component: () => import("../views/contact/EditContact.vue"),
    meta: {
      title: "Mise à jour Contact",
      requireLogin: true,
    },
  },
  {
    path: "/contacts/create",
    name: "CreateContact",
    component: () => import("../views/contact/CreateContact.vue"),
    meta: {
      title: "Nouveau contact",
      requireLogin: true,
    },
  },
  {
    path: "/contacts/create",
    name: "DuplicateContact",
    component: () => import("../views/contact/DuplicateContact.vue"),
    meta: {
      title: "Nouveau contact",
      requireLogin: true,
    },
  },
  {
    path: "/contacts/employee",
    name: "Employee",
    component: () => import("../views/contact/employee-list.vue"),
    meta: {
      title: "Employé",
      requireLogin: true,
    },
  },

  // ? operation route area
  {
    path: "/operations",
    name: "Operations",
    component: () => import("../views/operations/operation-list.vue"),
    meta: {
      title: "Entrées - Sorties",
      requireLogin: true,
    },
  },
  {
    path: "/operations/:id",
    name: "SingleOps",
    component: () => import("../views/operations/SingleOps.vue"),
    meta: {
      title: "Détail Opération",
      requireLogin: true,
    },
  },
  {
    path: "/operations/:id/edit",
    name: "EditOps",
    component: () => import("../views/operations/EditOps.vue"),
    meta: {
      title: "Mise à jour Opération",
      requireLogin: true,
    },
  },
  {
    path: "/operations/create",
    name: "CreateOps",
    component: () => import("../views/operations/CreateOps.vue"),
    meta: {
      title: "Nouvelle Opération",
      requireLogin: true,
    },
  },

  // ? inventory route area
  {
    path: "/stock",
    name: "Stock",
    component: () => import("../views/stock/Stock.vue"),
    meta: {
      title: "Votre stock",
      requireLogin: true,
    },
  },
  {
    path: "/stock/inventory",
    name: "Inventory",
    component: () => import("../views/stock/Inventory.vue"),
    meta: {
      title: "Espace inventaire",
      requireLogin: true,
    },
  },
  {
    path: "/stock/inventory/create",
    name: "CreateInventory",
    component: () => import("../views/stock/CreateInventory.vue"),
    meta: {
      title: "Nouveau inventaire",
      requireLogin: true,
    },
  },
  {
    path: "/stock/inventory/:id",
    name: "SingleInv",
    component: () => import("../views/stock/SingleInventory.vue"),
    meta: {
      title: "Détail Inventaire",
      requireLogin: true,
    },
  },

  // ? product route area
  {
    path: "/stock/products",
    name: "Products",
    component: () => import("../views/stock/product-list.vue"),
    meta: {
      title: "Liste des produits",
      requireLogin: true,
    },
  },
  {
    path: "/stock/products/:id",
    name: "SingleProduct",
    component: () => import("../views/stock/SingleProduct.vue"),
    meta: {
      title: "Détail Produit",
      requireLogin: true,
    },
  },
  {
    path: "/stock/products/create",
    name: "CreateProduct",
    component: () => import("../views/stock/CreateProduct.vue"),
    meta: {
      title: "Création de produit",
      requireLogin: true,
    },
  },
  {
    path: "/stock/products/duplicate",
    name: "DuplicateProduct",
    component: () => import("../views/stock/duplicate-product-screen.vue"),
    meta: {
      title: "Création de produit",
      requireLogin: true,
    },
  },
  {
    path: "/stock/products/create-multiple",
    name: "CreateMultipleProducts",
    component: () => import("../views/stock/CreateMultipleProducts.vue"),
    meta: {
      title: "Création multiple de produits",
      requireLogin: true,
    },
  },
  {
    path: "/stock/products/:id/edit",
    name: "EditProduct",
    component: () => import("../views/stock/edit-product.vue"),
    meta: {
      title: "Mise à jour Produit",
      requireLogin: true,
    },
  },

  // ? pos route area
  {
    path: "/pos",
    name: "POS",
    component: () => import("../views/pos/pos-screen.vue"),
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
