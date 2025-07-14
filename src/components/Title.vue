<template>
    <div class="head-container">
        <div class="icon">
            <img src="@/assets/logo.png" alt="logo" height="100%">
        </div>
        <div class="title">
            VisMimic
        </div>
    </div>
</template>

<script>
export default {
    name: 'Title',
};
</script>

<style scoped>
.head-container {
    /* 保持长宽比 345：52 */
    aspect-ratio: 345 / 52;
    /* 自适应宽度 */
    /* width: 100%; */
    /* height: 100%; */
    /* 布局 */
    display: flex;
    /* 交叉轴 */
    align-items: center;
    /* 主轴 */
    justify-content: flex-start;
    gap: 15px; /* 图标和标题之间的间距 */
    /* 样式 */
    background-color: #F3F3F3;
    padding: 5px; /* 内边距 */
    padding-left: 10px;
    box-sizing: border-box;
}

.icon {
    max-height: 100%; /* 图片最大高度为容器高度 */
    height: 100%; /* 保持宽高比 */
}

.title {
    font-size: 1.5em; /* 标题字体大小 */
    font-weight: bold;
    color: #2E4051
}
</style>