<!-- <template>
  <v-card max-width="344" class="mx-auto my-4" outlined>
    <v-img :src="product.image_url" height="200px"></v-img>
    <v-card-title>{{ product.name }}</v-card-title>
    <v-card-subtitle>₹ {{ product.price }}</v-card-subtitle>
    <v-card-text>{{ product.description }}</v-card-text>
    <v-card-actions>
      <v-btn color="primary" @click="$emit('add-to-cart', product)">Add to Cart</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'ProductCard',
  props: ['product']
}
</script> -->


<template>
  <v-card
    max-width="344"
    class="mx-auto my-4"
    outlined
    :to="{ name: 'product-details', params: { id: product.id } }"
    link
  >
    <v-img :src="product.image_url" height="200px"></v-img>
    <v-card-title>{{ product.name }}</v-card-title>
    <v-card-subtitle>₹ {{ product.price }}</v-card-subtitle>
    <v-card-text>{{ product.description }}</v-card-text>
    <v-card-actions>
      <v-btn color="primary" @click.stop="$emit('add-to-cart', product)">Add to Cart</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
export default {
  name: 'ProductCard',
  props: ['product']
}
</script>
