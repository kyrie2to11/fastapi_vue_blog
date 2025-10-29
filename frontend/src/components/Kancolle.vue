<template>
  <div class="kancolle-container">
    <img 
      src="@/assets/images/kancolle-character.png" 
      alt="Kancolle Character" 
      class="kancolle-character"
    >
    <div class="kancolle-text">
      <p>Hello! I'm your Kancolle companion~</p>
      <button @click="showGreeting">Say Hi</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const showGreeting = () => {
  alert('Nice to meet you!');
};
</script>

<style scoped>
.kancolle-container {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 12px;
  margin: 20px auto;
  max-width: 500px;
}

.kancolle-character {
  width: 120px;
  height: 120px;
  object-fit: cover;
  border-radius: 50%;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.kancolle-text p {
  margin: 0;
  font-size: 16px;
  color: #333;
}

button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #359469;
}
</style>