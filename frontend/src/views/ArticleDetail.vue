<template>
  <div class="article-detail-page">
    <n-page-header
      :title="article.title"
      :description="`作者: ${article.author.username} | 发布于 ${formatDate(article.created_at)}`"
      :style="{ marginBottom: '24px' }"
    />

    <n-card>
      <div class="article-content" v-html="article.content" />
    </n-card>

    <div class="article-meta" style="margin-top: 24px; padding-top: 16px; border-top: 1px solid #e5e7eb;">
      <div class="author-info">
        <n-avatar :src="article.author.avatar || '/default-avatar.png'" size="small" />
        <span style="margin-left: 8px;">{{ article.author.username }}</span>
      </div>
      <div class="publish-time">发布时间: {{ formatDate(article.created_at) }}</div>
      <div class="read-count">阅读量: {{ article.view_count || 0 }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { formatDate } from '@/utils/dateUtils';
import { NPageHeader, NCard, NAvatar } from 'naive-ui';

const route = useRoute();
const router = useRouter();
const article = ref(null);
const loading = ref(true);
const error = ref(null);

// 监听路由变化，重新获取文章
watch(route, async () => {
  loading.value = true;
  await fetchArticle();
});

onMounted(async () => {
  await fetchArticle();
});

const fetchArticle = async () => {
  try {
    const { slug } = route.params;
    if (!slug) {
      throw new Error('文章不存在');
    }
    
    const res = await fetch(`/api/v1/articles/${slug}`);
    if (!res.ok) throw new Error('文章不存在');
    
    article.value = await res.json();
    document.title = `${article.value.title} | 我的博客`;
  } catch (err) {
    error.value = err.message;
    console.error('获取文章失败:', err);
    router.push('/404');
  } finally {
    loading.value = false;
  }
};

onUnmounted(() => {
  // 清理定时器等资源
});
</script>

<style scoped>
.article-detail-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.article-content {
  line-height: 1.8;
  color: #333;
  font-size: 16px;
}

.article-content h2,
.article-content h3,
.article-content h4 {
  margin: 24px 0 16px;
  color: #2c3e50;
  font-weight: 600;
}

.article-content p {
  margin-bottom: 16px;
}

.article-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #666;
  font-size: 0.9rem;
}

.author-info {
  display: flex;
  align-items: center;
}

.publish-time, .read-count {
  display: flex;
  align-items: center;
}

.publish-time::before, .read-count::before {
  content: "|";
  margin: 0 8px;
  color: #ccc;
}
</style>