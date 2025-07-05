<!-- <template>
  <v-app>
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    //
  }),
}
</script> -->


<template>
  <v-app>
    <AppNavigation />

    <v-main>
      <router-view />
    </v-main>
    
  </v-app>
</template>

<script>
import AppNavigation from '@/components/layout/AppNavigation.vue'

export default {
  name: 'App',
  components: {
    AppNavigation
  }
}
</script>

