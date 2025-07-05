<template>
  <v-container fluid>
    <HeroBanner />
    <FeaturedCategories />
  </v-container>
</template>

<script>
import HeroBanner from '@/components/home/HeroBanner.vue'
import FeaturedCategories from '@/components/home/FeaturedCategories.vue'

export default {
  name: 'Home',
  components: {
    HeroBanner,
    FeaturedCategories
  }
}
</script>
