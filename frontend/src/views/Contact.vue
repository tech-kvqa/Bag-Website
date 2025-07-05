<template>
  <v-container>
    <h2>Contact Us</h2>
    <v-form>
      <v-text-field label="Your Name" v-model="name" required></v-text-field>
      <v-text-field label="Email" v-model="email" required></v-text-field>
      <v-textarea label="Message" v-model="message" required></v-textarea>
      <v-btn color="primary" @click="submitForm">Submit</v-btn>
    </v-form>
  </v-container>
</template>

<script>
export default {
  name: 'Contact',
  data() {
    return {
      name: '',
      email: '',
      message: ''
    }
  },
  methods: {
    submitForm() {
      alert("Message submitted successfully.")
      this.name = this.email = this.message = ''
    }
  }
}
</script>
