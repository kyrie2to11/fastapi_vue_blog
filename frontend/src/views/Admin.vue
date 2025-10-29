<template>
  <div class="admin-page">
    <n-layout has-sider style="min-height: 100vh;">
      <n-layout-sider bordered>
        <div class="admin-header">
          <n-avatar src="/logo.png" size="large" />
          <span class="admin-title">管理后台</span>
        </div>
        <n-menu :default-active="activeKey" class="admin-menu">
          <n-menu-item key="articles">
            <template #icon>
              <n-icon><ArticleIcon /></n-icon>
            </template>
            文章管理
          </n-menu-item>
          <n-menu-item key="categories">
            <template #icon>
              <n-icon><FolderIcon /></n-icon>
            </template>
            分类管理
          </n-menu-item>
          <n-menu-item key="profile">
            <template #icon>
              <n-icon><UserIcon /></n-icon>
            </template>
            个人资料
          </n-menu-item>
          <n-menu-item key="logout" @click="handleLogout">
            <template #icon>
              <n-icon><LogOutIcon /></n-icon>
            </template>
            退出登录
          </n-menu-item>
        </n-menu>
      </n-layout-sider>
      <n-layout>
        <n-layout-header style="background: #fff; padding: 0 24px; box-shadow: 0 1px 4px rgba(0, 0, 0, 0.12);">
          <div class="header-right">
            <n-dropdown trigger="click" placement="bottom-right">
              <n-avatar src="/user-avatar.png" size="small" />
              <template #content>
                <n-dropdown-menu>
                  <n-dropdown-item>编辑资料</n-dropdown-item>
                  <n-dropdown-item divided>退出登录</n-dropdown-item>
                </n-dropdown-menu>
              </template>
            </n-dropdown>
          </div>
        </n-layout-header>
        <n-layout-content style="padding: 24px;">
          <n-card>
            <AdminContent />
          </n-card>
        </n-layout-content>
      </n-layout>
    </n-layout>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useMessage } from 'naive-ui';
import { ArticleIcon, FolderIcon, UserIcon, LogOutIcon } from '@/components/Icons';
import AdminContent from '@/components/AdminContent.vue';

const router = useRouter();
const message = useMessage();
const activeKey = ref('articles');
const adminContentMap = {
  articles: '文章管理',
  categories: '分类管理',
  profile: '个人资料'
};

const handleLogout = () => {
  // 清除本地存储的token
  localStorage.removeItem('token');
  message.success('退出成功');
  router.push('/login');
};
</script>

<style scoped>
.admin-page {
  min-height: 100vh;
}

.admin-header {
  display: flex;
  align-items: center;
  padding: 16px 24px;
  background: #f0f2f5;
  border-bottom: 1px solid #e8e8e8;
}

.admin-title {
  margin-left: 12px;
  font-weight: 600;
  font-size: 18px;
}

.admin-menu {
  border-right: none !important;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}
</style>