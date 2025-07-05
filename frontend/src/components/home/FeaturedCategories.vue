<template>
  <v-container class="mt-8">
    <h2 class="text-center mb-6">Featured Categories</h2>
    <v-row>
      <v-col
        v-for="(category, i) in categories"
        :key="i"
        cols="12"
        md="4"
      >
        <v-card
          class="mx-auto"
          max-width="344"
          elevation="4"
          @click="$router.push({ name: 'shop', query: { category: category.name } })"
        >
          <v-img :src="category.image" height="200px"></v-img>
          <v-card-title>{{ category.name }}</v-card-title>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'FeaturedCategories',
  data() {
    return {
      categories: [
        {
          name: 'Backpacks',
          image: require('@/assets/backpack.png'),
        },
        {
          name: 'School Bags',
          image: require('@/assets/schoolbag.png'),
        },
        // {
        //   name: 'Luggage',
        //   image: require('@/assets/luggage.jpg'),
        // },
      ],
    }
  },
}
</script>
