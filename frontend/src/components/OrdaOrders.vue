<template>
  <div id="app">
    <table>
      <thead>
        <tr>
          <th>Order ID</th>
          <th>Customer ID</th>
          <th>Items</th>
          <th>Total</th>
          <th>Date</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="order in orders" :key="order.order_id">
          <td>{{ order.order_id }}</td>
          <td>{{ order.customer_id }}</td>
          <td>
            <ul>
              <li v-for="item in order.items" :key="item.item_id">
                {{ item.quantity }} x {{ item.name }} at ${{ item.price }}
              </li>
            </ul>
          </td>
          <td>${{ order.total }}</td>
          <td>{{ order.date }}</td>
          <td>{{ order.status }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'OrdaOrders',
  data() {
    return {
      orders: []
    };
  },
  mounted() {
    this.fetchOrders();
  },
  methods: {
    fetchOrders() {
      console.log('Fetching orders from:', process.env.VUE_APP_ORDERS_API); 
      
      const url = new URL(process.env.VUE_APP_ORDERS_API);
      // Force HTTPS by replacing the protocol if necessary
      url.protocol = 'https:';

      fetch(url.toString())
        .then(response => {
          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }
          return response.json();
        })
        .then(data => {
          this.orders = data;
        })
        .catch(error => console.error('Error fetching orders:', error));
    }
  }
}
</script>

<style scoped>
table {
  margin-left: auto;
  margin-right: auto;
  width: 80%;
  border-collapse: collapse;
}

thead {
  background-color: #f4f4f4;
}

th, td {
  padding: 8px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

tr:hover {
  background-color: #f5f5f5;
}

th {
  height: 50px;
}
</style>