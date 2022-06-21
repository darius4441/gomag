<script setup>
import { FilterMatchMode } from "primevue/api";
import Dialog from "primevue/dialog";
import FileUpload from "primevue/fileupload";
import { useToast } from "primevue/usetoast";
import { ref } from "vue-demi";
import { useRouter } from "vue-router";
import { useEmployees } from "../../composables";

const router = useRouter();

const toast = useToast();

const dt = ref();
const selectAll = ref();
const selectedEmployees = ref();
const skEmployees = ref(new Array(50));
const totalRecords = ref();
const employee = ref({});
const submitted = ref(false);
const { employees, isLoading } = useEmployees();
const employeeDialog = ref(false);
const deleteEmployeeDialog = ref(false);
const deleteEmployeesDialog = ref(false);

function goToCreatePage() {
  router.push({ name: "CreateEmployee" });
}

const confirmDeleteSelected = () => {
  deleteEmployeesDialog.value = true;
};

const deleteSelectedEmployees = () => {
  employees.value = employees.value.filter(
    (val) => !selectedEmployees.value.includes(val)
  );
  deleteEmployeesDialog.value = false;
  selectedEmployees.value = null;

  toast.add({
    severity: "success",
    summary: "Suppression",
    detail: "Les employés selectionnés ont ete supprimé avec succès",
    life: 3000,
  });
};

const openNew = () => {
  employee.value = {};
  submitted.value = false;
  employeeDialog.value = true;
};

const hideDialog = () => {
  employeeDialog.value = false;
  submitted.value = false;
};

const saveEmployee = () => {
  submitted.value = true;
  if (employee.value.name.trim()) {
    if (employee.value.id) {
      employee.value.inventoryStatus = employee.value.inventoryStatus.value
        ? employee.value.inventoryStatus.value
        : employee.value.inventoryStatus;
      employees.value[findIndexById(employee.value.id)] = employee.value;

      toast.add({
        severity: "success",
        summary: "Modification",
        detail: "Employé modifié avec succès",
        life: 3000,
      });
    } else {
      employee.value.id = createId();
      employee.value.code = createId();
      employee.value.image = "employee-placeholder.svg";
      employee.value.inventoryStatus = employee.value.inventoryStatus
        ? employee.value.inventoryStatus.value
        : "INSTOCK";
      employees.value.push(employee.value);

      toast.add({
        severity: "success",
        summary: "Création",
        detail: "Employé créée avec succès",
        life: 3000,
      });
    }
    employeeDialog.value = false;
    employee.value = {};
  }
};

const editEmployee = (prod) => {
  employee.value = { ...prod };
  employeeDialog.value = true;
};

const confirmDeleteEmployee = (prod) => {
  employee.value = prod;
  deleteEmployeeDialog.value = true;
};

const deleteEmployee = () => {
  employees.value = employees.value.filter(
    (val) => val.id !== employee.value.id
  );
  deleteEmployeeDialog.value = false;
  employee.value = {};

  toast.add({
    severity: "success",
    summary: "Suppression",
    detail: "Employé supprimer avec succès",
    life: 3000,
  });
};

const findIndexById = (id) => {
  let index = -1;
  for (let i = 0; i < employees.value.length; i++) {
    if (employees.value[i].id === id) {
      index = i;
      break;
    }
  }
  return index;
};

const createId = () => {
  let id = "";
  var chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  for (var i = 0; i < 5; i++) {
    id += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return id;
};

const onSelectAllChange = (event) => {
  const selectAllClick = event.checked;

  if (selectAllClick) {
    selectAll.value = true;
    selectedEmployees.value = employees.value;
  } else {
    selectAll.value = false;
    selectedEmployees.value = [];
  }
};

const onRowSelect = () => {
  selectAll.value = selectedEmployees.value.length === totalRecords.value;
};

const onRowUnselect = () => {
  selectAll.value = false;
};

const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  username: { value: null, matchMode: FilterMatchMode.CONTAINS },
  first_name: { value: null, matchMode: FilterMatchMode.CONTAINS },
  last_name: { value: null, matchMode: FilterMatchMode.CONTAINS },
  phone: { value: null, matchMode: FilterMatchMode.EQUALS },
  email: { value: null, matchMode: FilterMatchMode.EQUALS },
});

const exportCSV = () => {
  dt.value.exportCSV();
};

function goToSingleEmployee(id, isNewTab) {
  if (isNewTab ?? false) {
    const routeData = router.resolve({
      name: "SingleEmployee",
      params: { id: id },
    });

    window.open(routeData.href, "blank");
  } else {
    router.push({ name: "SingleEmployee", params: { id: id } });
  }
}
</script>

<template>
  <div>
    <PrimeCard v-if="isLoading" class="p-4">
      <template #content>
        <div class="flex justify-between mb-4">
          <PrimeSkeleton width="9rem" height="3rem" />
          <div class="flex">
            <PrimeSkeleton width="3rem" height="3rem" class="mr-2" />
            <PrimeSkeleton width="20rem" height="3rem" />
          </div>
        </div>

        <PrimeDataTable
          :value="skEmployees"
          responsiveLayout="scroll"
          paginatorTemplate="FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
          currentPageReportTemplate="({last} sur {totalRecords})"
          class="cursor-pointer h-[60vh] p-datatable-sm"
          scrollHeight="50vh"
          :rowHover="true"
          :scrollable="true"
          filterDisplay="menu"
        >
          <PrimeColumn
            field="first_name"
            header="Nom"
            style="min-width: 15rem"
            class="text-sm truncate"
          >
            <template #body> <PrimeSkeleton /> </template>
          </PrimeColumn>
        </PrimeDataTable>
      </template>
    </PrimeCard>

    <template v-else>
      <PrimeCard>
        <template #header>
          <PrimeToolbar>
            <template #start>
              <PrimeButton
                label="Nouveau"
                icon="pi pi-plus"
                class="p-button-outlined p-button-success p-button-sm mr-2"
                @click="openNew"
              />
              <PrimeButton
                label="Supprimer"
                icon="pi pi-trash"
                class="p-button-outlined p-button-danger p-button-sm mr-2"
                @click="confirmDeleteSelected"
                :disable="!selectedEmployees || !selectedEmployees.length"
              />
            </template>

            <template #end>
              <FileUpload
                mode="basic"
                accept="image/*"
                :maxFileSize="100000"
                label="Importer"
                class="p-button-sm p-button-outlined"
                @click="openNew"
              />
              <PrimeButton
                icon="pi pi-upload p-button-sm p-button-help"
                class="p-button-text mr-3"
                @click="exportCSV($event)"
              />
            </template>
          </PrimeToolbar>
        </template>
        <template #content>
          <PrimeDataTable
            ref="dt"
            :rows="50"
            scrollable
            dataKey="id"
            :rowHover="true"
            stateStorage="session"
            stateKey="employees-state"
            :value="employees"
            :paginator="true"
            scrollHeight="60vh"
            filterDisplay="row"
            :selectAll="selectAll"
            v-model:filters="filters"
            @row-select="onRowSelect"
            @row-unselect="onRowUnselect"
            v-model:selection="selectedEmployees"
            @select-all-change="onSelectAllChange"
            @row-click="goToSingleEmployee($event.data.id)"
            currentPageReportTemplate="({last} sur {totalRecords})"
            :globalFilterFields="[
              'username',
              'first_name',
              'last_name',
              'phone',
              'email',
            ]"
            paginatorTemplate="FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink"
            class="cursor-pointer h-[72vh] p-datatable-sm"
          >
            <template #empty> Aucun produits trouvé. </template>

            <template #loading>
              Chargement des produits. Veillez patienter.
            </template>

            <PrimeColumn
              selectionMode="multiple"
              headerStyle="width: 2rem"
              :exportable="false"
            />

            <PrimeColumn
              field="first_name"
              style="min-width: 15rem"
              header="Nom"
              class="text-sm truncate"
            >
              <template #body="{ data }">
                {{ data.first_name }} {{ data.last_name }}
              </template>

              <template #filter="{ filterModel, filterCallback }">
                <PrimeInputText
                  type="text"
                  v-model="filterModel.value"
                  @keydown.enter="filterCallback()"
                  class="p-column-filter"
                  placeholder="Trier par nom"
                  v-tooltip.top.focus="'Appuyer sur une touche pour filter'"
                />
              </template>
            </PrimeColumn>

            <PrimeColumn
              field="phone"
              style="min-width: 12rem"
              header="Téléphone"
              class="text-sm truncate"
            >
              <template #body="{ data }">
                {{ data.phone }}
              </template>

              <template #filter="{ filterModel, filterCallback }">
                <PrimeInputText
                  type="text"
                  v-model="filterModel.value"
                  @keydown.enter="filterCallback()"
                  class="p-column-filter"
                  placeholder="Trier par téléphone"
                  v-tooltip.top.focus="'Appuyer sur une touche pour filter'"
                />
              </template>
            </PrimeColumn>

            <PrimeColumn
              field="email"
              style="min-width: 15rem"
              header="Email"
              class="text-sm truncate"
            >
              <template #body="{ data }">
                {{ data.email }}
              </template>

              <template #filter="{ filterModel, filterCallback }">
                <PrimeInputText
                  type="text"
                  v-model="filterModel.value"
                  @keydown.enter="filterCallback()"
                  class="p-column-filter"
                  placeholder="Trier par email"
                  v-tooltip.top.focus="'Appuyer sur une touche pour filter'"
                />
              </template>
            </PrimeColumn>

            <PrimeColumn
              field="username"
              style="min-width: 15rem"
              header="Identifiant"
              class="text-sm truncate"
            >
              <template #body="{ data }">
                {{ data.username }}
              </template>

              <template #filter="{ filterModel, filterCallback }">
                <PrimeInputText
                  type="text"
                  v-model="filterModel.value"
                  @keydown.enter="filterCallback()"
                  class="p-column-filter"
                  placeholder="Trier par identifiant"
                  v-tooltip.top.focus="'Appuyer sur une touche pour filter'"
                />
              </template>
            </PrimeColumn>

            <PrimeColumn :exportable="false" class="min-width:8rem">
              <template #body="slotProps">
                <PrimeButton
                  icon="pi pi-pencil"
                  class="p-button-rounded p-button-outlined p-button-success p-button-sm mr-2"
                  @click="editEmployee(slotProps.data)"
                />
                <PrimeButton
                  icon="pi pi-trash"
                  class="p-button-rounded p-button-outlined p-button-danger p-button-sm"
                  @click="confirmDeleteEmployee(slotProps.data)"
                />
              </template>
            </PrimeColumn>
          </PrimeDataTable>
        </template>
      </PrimeCard>

      <Dialog
        v-model:visible="employeeDialog"
        :style="{ width: '450px' }"
        header="Detail de l'employée"
        :modal="true"
        class="p-fluid"
      >
        <div class="flex justify-between gap-x-4 flex-row">
          <div class="field mt-4">
            <label for="first_name">Nom</label>
            <PrimeInputText
              id="first_name"
              v-model.trim="employee.first_name"
              required="true"
              autofocus
              :class="{ 'p-invalid': submitted && !employee.first_name }"
            />
            <small class="p-error" v-if="submitted && !employee.first_name"
              >Nom requis</small
            >
          </div>

          <div class="field mt-4">
            <label for="last_name">Prenom</label>
            <PrimeInputText
              id="last_name"
              v-model.trim="employee.last_name"
              required="true"
              :class="{ 'p-invalid': submitted && !employee.last_name }"
            />
            <small class="p-error" v-if="submitted && !employee.last_name"
              >Prenom requis</small
            >
          </div>
        </div>

        <div class="field mt-4">
          <label for="phone">Téléphone</label>
          <PrimeInputMask
            id="phone"
            :unmask="true"
            mask="99 99 99 9999"
            v-model.trim="employee.phone"
            required="true"
            :class="{ 'p-invalid': submitted && !employee.phone }"
          />
          <small class="p-error" v-if="submitted && !employee.phone">
            Téléphone requis
          </small>
        </div>

        <div class="field mt-4">
          <label for="email">Email</label>
          <PrimeInputText
            id="email"
            v-model.trim="employee.email"
            required="true"
            :class="{ 'p-invalid': submitted && !employee.email }"
          />
          <small class="p-error" v-if="submitted && !employee.email">
            Email requis
          </small>
        </div>

        <div class="field mt-4">
          <label for="username">Identifiant</label>
          <PrimeInputText
            id="username"
            v-model.trim="employee.username"
            required="true"
            :class="{ 'p-invalid': submitted && !employee.username }"
          />
          <small class="p-error" v-if="submitted && !employee.username">
            Identifiant requis
          </small>
        </div>

        <template #footer>
          <PrimeButton
            label="Annuler"
            icon="pi pi-times"
            class="p-button-text"
            @click="hideDialog"
          />

          <PrimeButton
            label="Sauver"
            icon="pi pi-check"
            class="p-button-text"
            @click="saveEmployee"
          />
        </template>
      </Dialog>

      <Dialog
        v-model:visible="deleteEmployeeDialog"
        :style="{ width: '450px' }"
        header="Confirm"
        :modal="true"
      >
        <div class="confirmation-content">
          <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
          <span v-if="employee"
            >Voulez-vous supprimer
            <b>{{ employee.first_name }} {{ employee.last_name }}</b
            >?</span
          >
        </div>
        <template #footer>
          <PrimeButton
            label="No"
            icon="pi pi-times"
            class="p-button-text"
            @click="deleteEmployeeDialog = false"
          />
          <PrimeButton
            label="Yes"
            icon="pi pi-check"
            class="p-button-text"
            @click="deleteEmployee"
          />
        </template>
      </Dialog>

      <Dialog
        v-model:visible="deleteEmployeesDialog"
        :style="{ width: '450px' }"
        header="Confirm"
        :modal="true"
      >
        <div class="confirmation-content">
          <i class="pi pi-exclamation-triangle mr-3" style="font-size: 2rem" />
          <span v-if="employee"
            >Voulez-vous supprimer les employées selectionner?</span
          >
        </div>
        <template #footer>
          <PrimeButton
            label="No"
            icon="pi pi-times"
            class="p-button-text"
            @click="deleteEmployeesDialog = false"
          />
          <PrimeButton
            label="Yes"
            icon="pi pi-check"
            class="p-button-text"
            @click="deleteSelectedEmployees"
          />
        </template>
      </Dialog>
    </template>
  </div>
</template>

<style scoped>
.table-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  @media screen and (max-width: 960px) {
    align-items: start;
  }
}
.employee-image {
  width: 50px;
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
}
.p-dialog .employee-image {
  width: 50px;
  margin: 0 auto 2rem auto;
  display: block;
}
.confirmation-content {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
