<template>
  <div>
    <button @click="fetchData" class="fetch-button">Fetch Data</button>
    <p>{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: ''
    };
  },
  methods: {
    fetchData() {
      axios.get('http://localhost:5001/api/data')
        .then(response => {
          this.message = response.data.message;
        })
        .catch(error => {
          console.error('There was an error!', error);
        });
    }
  }
}
</script>

<style scoped>
.fetch-button {
  background-color: #4CAF50; /* Green */
  color: white;
  border: none;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.fetch-button:hover {
  background-color: #45a049;
}
</style>
