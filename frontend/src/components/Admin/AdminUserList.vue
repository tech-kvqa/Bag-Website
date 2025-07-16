<!-- <template>
  <v-container>
    <h2>Manage Users</h2>

    <v-table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Email</th>
          <th>Phone</th>
          <th>Address</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.phone }}</td>
          <td>{{ user.address }}</td>
          <td>
            <v-btn small color="error" @click="deleteUser(user.id)">Delete</v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </v-container>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'AdminUserList',
  data() {
    return {
      users: []
    }
  },
  mounted() {
    this.loadUsers()
  },
  methods: {
    loadUsers() {
      api.get('/admin/users')
        .then(res => {
          this.users = res.data
        })
        .catch(err => console.error(err))
    },
    deleteUser(id) {
      if (confirm('Are you sure you want to delete this user?')) {
        api.delete(`/admin/users/${id}`)
          .then(() => this.loadUsers())
          .catch(err => console.error(err))
      }
    }
  }
}
</script> -->


<template>
  <v-container>
    <h2>Manage Users</h2>

    <v-text-field
      v-model="search"
      label="Search by name or email"
      prepend-icon="mdi-magnify"
      class="mb-4"
    ></v-text-field>

    <v-data-table>
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Phone</th>
          <th>Address</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="user in filteredUsers" :key="user.id">
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.phone }}</td>
          <td>{{ user.address }}</td>
          <td>
            <v-btn small color="error" @click="deleteUser(user.id)">Delete</v-btn>
          </td>
        </tr>
      </tbody>
    </v-data-table>
  </v-container>
</template>

<script>
import api from '@/utils/api'

export default {
  name: 'AdminUserList',
  data() {
    return {
      users: [],
      search: ''
    }
  },
  computed: {
    filteredUsers() {
      const s = this.search.toLowerCase()
      return this.users.filter(user =>
        user.name.toLowerCase().includes(s) ||
        user.email.toLowerCase().includes(s)
      )
    }
  },
  mounted() {
    this.loadUsers()
  },
  methods: {
    loadUsers() {
      api.get('/admin/users')
        .then(res => {
          this.users = res.data
        })
        .catch(err => console.error(err))
    },
    deleteUser(id) {
      if (confirm('Are you sure you want to delete this user?')) {
        api.delete(`/admin/users/${id}`)
          .then(() => this.loadUsers())
          .catch(err => console.error(err))
      }
    }
  }
}
</script>
