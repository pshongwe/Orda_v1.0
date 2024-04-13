<template>
  <div>
    <button @click="fetchData">Fetch Data</button>
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
