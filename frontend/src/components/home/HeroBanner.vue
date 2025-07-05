<!-- <template>
  <v-carousel hide-delimiter-background>
    <v-carousel-item
      v-for="(item, i) in items"
      :key="i"
      :src="item.src"
    >
      <v-container class="fill-height d-flex align-center justify-center">
        <div class="text-center white--text">
          <h1 class="display-2 font-weight-bold">{{ item.title }}</h1>
          <p class="headline">{{ item.subtitle }}</p>
        </div>
      </v-container>
    </v-carousel-item>
  </v-carousel>
</template>

<script>
export default {
  name: 'HeroBanner',
  data() {
    return {
      items: [
        {
          src: require('@/assets/banner1.png'),
          title: 'Backpacks for Every Journey',
          subtitle: 'Stylish, rugged, and reliable.',
        },
        {
          src: require('@/assets/banner2.png'),
          title: 'Travel Light, Pack Smart',
          subtitle: 'Explore our luggage collection.',
        },
      ],
    }
  },
}
</script>

<style scoped>
.v-carousel-item {
  height: 600px;
}
</style> -->


<!-- <template>
  <v-carousel>
    <v-carousel-item v-for="(item, i) in items" :key="i" :src="item.src">
      <v-container class="fill-height d-flex align-center justify-center">
        <div ref="title" class="text-center white--text">
          <h1 class="display-2 font-weight-bold">{{ item.title }}</h1>
          <p class="headline">{{ item.subtitle }}</p>
        </div>
      </v-container>
    </v-carousel-item>
  </v-carousel>
</template>

<script>
import { gsap } from 'gsap'

export default {
  name: 'HeroBanner',
  data() {
    return {
      items: [
        { src: require('@/assets/banner1.png'), title: 'Backpacks', subtitle: 'For every journey' },
        { src: require('@/assets/banner2.png'), title: 'Travel Smart', subtitle: 'Light & reliable' },
      ],
    }
  },
  mounted() {
    // Animate title container when mounted
    gsap.from(this.$refs.title, {
      opacity: 0,
      y: -50,
      duration: 1.5,
      ease: 'power2.out'
    })
  },
}
</script> -->


<template>
  <v-carousel
    hide-delimiter-background
    height="100vh"
    show-arrows-on-hover
  >
    <v-carousel-item
      v-for="(item, i) in items"
      :key="i"
    >
      <v-img
        :src="item.src"
        height="100vh"
        cover
      >
        <v-container class="fill-height d-flex align-center justify-center">
          <div ref="title" class="text-center white--text">
            <h1 class="display-2 font-weight-bold">{{ item.title }}</h1>
            <p class="headline">{{ item.subtitle }}</p>
          </div>
        </v-container>
      </v-img>
    </v-carousel-item>
  </v-carousel>
</template>

<script>
import { gsap } from 'gsap'

export default {
  name: 'HeroBanner',
  data() {
    return {
      items: [
        { src: require('@/assets/banner1.png'), title: 'Backpacks', subtitle: 'For every journey' },
        { src: require('@/assets/banner2.png'), title: 'Travel Smart', subtitle: 'Light & reliable' },
      ],
    }
  },
  mounted() {
    gsap.from(this.$refs.title, {
      opacity: 0,
      y: -50,
      duration: 1.5,
      ease: 'power2.out'
    })
  },
}
</script>

<style scoped>
.v-carousel-item {
  height: 100vh;
}

.v-img {
  object-fit: cover;
}
</style>
