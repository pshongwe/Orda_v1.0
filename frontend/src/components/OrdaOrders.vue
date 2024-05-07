<template>
  <div>
    <button @click="fetchData" class="fetch-button">Fetch Data</button>
    <p>{{ orders }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      orders: {}
    };
  },
  methods: {
    fetchData() {
      axios.get('http://localhost:5000/api/v1/orders')
        .then(response => {
          this.orders = response.data;
        })
        .catch(error => {
          console.error('There was an error!', error);
        });
    }
  }
}
</script>
