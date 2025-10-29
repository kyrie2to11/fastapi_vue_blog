<template>
  <div class="home-page">
    <div class="hero-section">
      <h1>欢迎来到我的博客</h1>
      <p>分享技术心得与生活感悟</p>
    </div>
    
    <div class="articles-container">
      <h2>最新文章</h2>
      <div class="articles-list">
        <article-card 
          v-for="article in articles" 
          :key="article.id" 
          :article="article" 
          @click="goToDetail(article.slug)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ArticleCard from '@/components/ArticleCard.vue';

const router = useRouter();
const articles = ref([]);

onMounted(async () => {
  try {
    const res = await fetch('/api/v1/articles?limit=6');
    const data = await res.json();
    articles.value = data.articles;
  } catch (err) {
    console.error('获取文章失败:', err);
  }
});

const goToDetail = (slug) => {
  router.push(`/articles/${slug}`);
};
</script>

<style scoped>
.home-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.hero-section {
  text-align: center;
  padding: 40px 0;
  background-color: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 40px;
}

.hero-section h1 {
  font-size: 2.5rem;
  margin-bottom: 10px;
  color: #333;
}

.hero-section p {
  font-size: 1.2rem;
  color: #666;
}

.articles-container h2 {
  margin-bottom: 20px;
  color: #333;
}

.articles-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}
</style>