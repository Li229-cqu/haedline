<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <h1>新闻内容智能摘要与标题生成系统</h1>
      <el-menu mode="horizontal" :ellipsis="false" router>
        <el-menu-item index="/">新闻处理</el-menu-item>
        <el-menu-item index="/batch">批量处理</el-menu-item>
        <el-menu-item index="/history">历史记录</el-menu-item>
        <el-menu-item index="/statistics">统计分析</el-menu-item>
      </el-menu>
    </el-header>
    <el-main>
      <router-view />
    </el-main>
  </el-container>
</template>
