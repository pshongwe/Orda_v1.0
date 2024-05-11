<template>
  <img src="@/assets/logo.png" alt="OrdaSys Logo" class="logo" @mouseover="hover = true" @mouseleave="hover = false">
  <OrdaOrders />
</template>

<script>
import OrdaOrders from './components/OrdaOrders.vue';
// import Restaurant from './components/OrdaRestaurant.vue'

export default {
  name: 'App',
  components: {
    // Restaurant,
    OrdaOrders
  }
}
</script>

<style>
.logo {
  transition: transform 0.5s ease;
  transform: scale(0.5);
  opacity: 0.5;
}
.logo:hover {
  transform: scale(1.1); /* Scale up the logo on hover */
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
body {
    margin: 0;
    font-family: 'Open Sans', sans-serif;
}

main > section.items h4 {
    text-align: center;
    margin-top: 0;
    width: 100%;
}
main {
    display: flex;
    justify-content: center;
    align-items:flex-start;
    flex-wrap: wrap;
    padding-top: 20px;
}

main > section.items {
    display: flex;
    flex-wrap: wrap;
    border: 1px solid lightgrey;
    padding: 20px;
    max-width: 500px;
    min-width: 300px;
    justify-content: center;
    
}

section.items .product {
    border: 1px solid lightgrey;
    margin: 6px;
    flex: 0 0 calc(33.333% - 24px);
    cursor: pointer;
    text-align: center;
}

section.items .product.selected {
    border: 2px solid rgb(29, 134, 233);

}

section.items .photo img {
    max-width: 90px;
}

section.items .description {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    font-size: 11px;
    line-height: 15px;
}

section.items  .description .price {
    font-weight: bold;
    margin: 4px auto;
}

section.items  .description .quantity-area {
    margin: 8px auto;
    height: 14px;
}

section.items  .description .quantity-area button {
    width: 16px;
    height: 16px;
    display: inline-flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
}

section.items  .description .quantity-area .quantity {
    font-weight: bold;
    margin: 0 4px;
}


section.summary {
    background-color: rgb(245, 245, 245);
    padding: 20px;
    min-height: 200px;
    min-width: 200px;
    text-align: center;
}

section.summary table {
    width: 100%;
    padding-top: 12px;
    font-size: 11px;
    margin: auto;
}

section.summary table tbody tr:last-of-type th {
    border-top: 1px solid black;
    padding-top: 4px;
}


</style>
