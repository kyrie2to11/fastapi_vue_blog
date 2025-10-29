# API 路由结构文档

## 基础信息
- **API 基础路径**: `/api/v1`
- **数据库**: PostgreSQL
- **认证方式**: JWT Token

## 认证相关接口

### 用户注册
- **URL**: `/api/v1/auth/register`
- **方法**: POST
- **请求体**:
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **响应**:
  ```json
  {
    "id": "number",
    "username": "string",
    "email": "string",
    "token": "string"
  }
  ```

### 用户登录
- **URL**: `/api/v1/auth/login`
- **方法**: POST
- **请求体**:
  ```json
  {
    "email": "string",
    "password": "string"
  }
  ```
- **响应**:
  ```json
  {
    "id": "number",
    "username": "string",
    "email": "string",
    "token": "string"
  }
  ```

## 文章相关接口

### 获取文章列表
- **URL**: `/api/v1/articles`
- **方法**: GET
- **查询参数**:
  - `page`: 页码 (默认 1)
  - `limit`: 每页数量 (默认 10)
  - `category`: 分类筛选 (可选)
- **响应**:
  ```json
  {
    "total": "number",
    "pages": "number",
    "current_page": "number",
    "articles": [
      {
        "id": "number",
        "title": "string",
        "slug": "string",
        "summary": "string",
        "author": {
          "id": "number",
          "username": "string"
        },
        "created_at": "datetime"
      }
    ]
  }
  ```

### 获取文章详情
- **URL**: `/api/v1/articles/{slug}`
- **方法**: GET
- **响应**:
  ```json
  {
    "id": "number",
    "title": "string",
    "slug": "string",
    "content": "string",
    "summary": "string",
    "author": {
      "id": "number",
      "username": "string"
    },
    "category": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
  }
  ```

### 创建文章
- **URL**: `/api/v1/articles`
- **方法**: POST
- **请求头**: `Authorization: Bearer {token}`
- **请求体**:
  ```json
  {
    "title": "string",
    "content": "string",
    "summary": "string",
    "category_id": "number"
  }
  ```
- **响应**:
  ```json
  {
    "id": "number",
    "title": "string",
    "slug": "string",
    "content": "string",
    "summary": "string",
    "category_id": "number",
    "created_at": "datetime"
  }
  ```

### 更新文章
- **URL**: `/api/v1/articles/{id}`
- **方法**: PUT
- **请求头**: `Authorization: Bearer {token}`
- **请求体**:
  ```json
  {
    "title": "string",
    "content": "string",
    "summary": "string",
    "category_id": "number"
  }
  ```
- **响应**:
  ```json
  {
    "id": "number",
    "title": "string",
    "slug": "string",
    "content": "string",
    "summary": "string",
    "category_id": "number",
    "updated_at": "datetime"
  }
  ```

### 删除文章
- **URL**: `/api/v1/articles/{id}`
- **方法**: DELETE
- **请求头**: `Authorization: Bearer {token}`
- **响应**: 204 No Content