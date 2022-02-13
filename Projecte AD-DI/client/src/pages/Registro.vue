<template>
  <q-page class="bg-light-blue window-height window-width row justify-center items-center">
    <div class="column">
      <div class="row">
        <h5 class="text-h5 text-white q-my-md">Register</h5>
      </div>
      <div class="row">
        <q-card square bordered class="q-pa-lg shadow-1">
          <q-card-section>
            <q-form class="q-gutter-md">
              <q-input square filled clearable v-model="nombre" type="text" label="Nombre Completo" :rules="[val => !!val || 'Nombre Completo is missing']"/>
              <q-input square filled clearable v-model="dni" type="text" label="DNI" :rules="[val => !!val || 'DNI is missing']"/>
              <q-input square filled clearable v-model="email" type="email" label="Username" :rules="[val => !!val || 'Email is missing']"/>
              <q-input square filled clearable v-model="password" type="password" label="Password" :rules="[val => !!val || 'Password is missing']"/>
            </q-form>
          </q-card-section>
          <q-card-actions class="q-px-md">
            <q-btn unelevated color="light-blue-7" size="lg" class="full-width" label="LOGIN" />
          </q-card-actions>
          <q-card-section class="text-center q-pa-none">
            <p class="text-grey-6">Torna al <a href="http://localhost:8080/#/"> Login </a> </p>
          </q-card-section>
        </q-card>
      </div>
    </div>
  </q-page>
</template>

<script>
export default {
  name: 'Register',
  data () {
    return {
      nombre: '',
      dni: '',
      email: '',
      password: ''
    }
  }
}
</script>
