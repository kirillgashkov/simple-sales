<script setup>
import { ref, reactive, onMounted } from "vue";

import axios from "../api/axios";
import router from "../router";
import { useUsersStore } from "../stores/users";
import { getEmployeeTypeChoices, getCityChoices, Choice } from "../api/choices";

const loaded = ref(false);
const employeeTypeOptions = ref([]);
const cityOptions = ref([]);

onMounted(async () => {
  employeeTypeOptions.value = [
    new Choice({ id: null, displayName: "" }), ...(await getEmployeeTypeChoices())
  ];
  cityOptions.value = [
    new Choice({ id: null, displayName: "" }), ...(await getCityChoices())
  ];

  loaded.value = true;
})

const userData = reactive({
  username: "",
  password: "",
  employee: {
    employee_type: {
      id: null,
    },
    first_name: "",
    middle_name: "",
    last_name: "",
    city: {
      id: null,
    },
  },
});
const passwordConfirmation = ref("")
const errorMessage = ref("");

function getErrorMessageIfFormError() {
  if (!userData.username) {
    return "Имя пользователя не может быть пустым";
  }

  if (!userData.employee.employee_type.id) {
    return "Тип сотрудника не может быть пустым";
  }

  if (!userData.employee.first_name) {
    return "Имя не может быть пустым";
  }

  if (!userData.employee.last_name) {
    return "Фамилия не может быть пустой";
  }

  if (!userData.employee.city.id) {
    return "Город не может быть пустым";
  }

  if (!userData.password) {
    return "Пароль не может быть пустым";
  }

  if (userData.password !== passwordConfirmation.value) {
    return "Пароли не совпадают";
  }

  return null;
}

async function signInReturningErrorMessageIfAny() {
  const sessions_url = "/sessions"
  const sessions_payload = {}
  const sessions_config = {
    // Authorization: Basic
    auth: {
      username: userData.username,
      password: userData.password,
    }
  }

  try {
    await axios.post(sessions_url, sessions_payload, sessions_config)

    const usersStore = useUsersStore();

    try {
      await usersStore.loadUser()
      if (!usersStore.user) {
        return "Неизвестная ошибка";
      }
      router.push({ name: "home" });
    } catch (error) {
      console.error(error)
      return "Неизвестная ошибка";
    }
  } catch (error) {
    console.error(error)
    return "Неизвестная ошибка";
  }

  return null;
}


function getErrorMessageFromSignUpError(error) {
  if (!error.response) {
    return "Неизвестная ошибка";
  }

  if (error.response.status === 400) {
    if (!error.response.data) {
      return "Неизвестная ошибка";
    }
    if (error.response.data.detail === "Referenced city does not exist") {
      return "Не получилось создать пользователя с выбранным городом, попробуйте перезагрузить страницу";
    }
    if (error.response.data.detail === "Referenced employee type does not exist") {
      return "Не получилось создать пользователя с выбранным типом сотрудника, попробуйте перезагрузить страницу";
    }
  }

  if (error.response.status === 409) {
    return "Имя пользователя уже занято";
  }

  return "Неизвестная ошибка";
}

async function signUp() {
  errorMessage.value = ""

  errorMessage.value = getErrorMessageIfFormError()
  if (errorMessage.value) {
    return;
  }

  if (!userData.employee.middle_name.trim()) {
    userData.employee.middle_name = null;
  }

  try {
    await axios.post("/users", userData);

    errorMessage.value = await signInReturningErrorMessageIfAny()
    if (errorMessage.value) {
      return;
    }

    router.push({ name: "home" });
  } catch (error) {
    errorMessage.value = getErrorMessageFromSignUpError(error);
    return
  }
}
</script>

<template>
  <template v-if="loaded">
    <main class="container">
      <section class="section">
        <div class="columns is-centered">
          <div class="column is-half">
            <h1 class="title has-text-centered">Регистрация</h1>

            <form class="box" @submit.prevent="signUp">
              <div class="field">
                <label class="label">Имя пользователя</label>
                <div class="control">
                  <input class="input" type="text" placeholder="ivanov" v-model="userData.username" />
                </div>
              </div>

              <div class="field">
                <label class="label">Тип сотрудника</label>
                <div class="control">
                  <div class="select">
                    <select v-model="userData.employee.employee_type.id">
                      <option v-for="employeeTypeOption in employeeTypeOptions" :key="employeeTypeOption.id"
                        :value="employeeTypeOption.id">
                        {{ employeeTypeOption.displayName }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>

              <div class="field">
                <label class="label">Фамилия</label>
                <div class="control">
                  <input class="input" type="text" placeholder="Иванов" v-model="userData.employee.last_name" />
                </div>
              </div>

              <div class="field">
                <label class="label">Имя</label>
                <div class="control">
                  <input class="input" type="text" placeholder="Иван" v-model="userData.employee.first_name" />
                </div>
              </div>

              <div class="field">
                <label class="label">Отчество (если есть)</label>
                <div class="control">
                  <input class="input" type="text" placeholder="Иванович" v-model="userData.employee.middle_name" />
                </div>
              </div>

              <div class="field">
                <label class="label">Город</label>
                <div class="control">
                  <div class="select">
                    <select v-model="userData.employee.city.id">
                      <option v-for="cityOption in cityOptions" :key="cityOption.id" :value="cityOption.id">
                        {{ cityOption.displayName }}
                      </option>
                    </select>
                  </div>
                </div>
              </div>

              <div class="field">
                <label class="label">Пароль</label>
                <div class="control">
                  <input class="input" type="password" placeholder="********" v-model="userData.password" />
                </div>
              </div>

              <div class="field">
                <label class="label">Подтверждение пароля</label>
                <div class="control">
                  <input class="input" type="password" placeholder="********" v-model="passwordConfirmation" />
                </div>
              </div>

              <div class="field">
                <div class="control">
                  <div class="has-text-danger" v-if="errorMessage">
                    {{ errorMessage }}
                  </div>
                </div>
              </div>

              <div class="field">
                <div class="control">
                  <button class="button is-primary is-fullwidth">
                    <strong>Зарегистрироваться</strong>
                  </button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </section>
    </main>
  </template>
</template>
