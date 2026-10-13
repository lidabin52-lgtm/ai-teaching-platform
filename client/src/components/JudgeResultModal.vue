<template>
  <!-- 审判结果弹窗组件 -->
  <el-dialog
    v-model="visible"
    :show-close="false"
    :close-on-click-modal="false"
    width="600px"
    class="judge-result-dialog"
    destroy-on-close
  >
    <div class="result-container">
      <!-- 顶部：获得星数 -->
      <div class="stars-section">
        <h3 class="result-title">审判结果</h3>
        <div class="stars-display">
          <div
            v-for="n in 3"
            :key="n"
            class="star-item"
            :class="{ filled: n <= result.totalStars, animate: showAnimation }"
            :style="{ animationDelay: `${n * 0.2}s` }"
          >
            <svg viewBox="0 0 24 24" class="star-svg">
              <path
                d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
                :fill="n <= result.totalStars ? '#F7BA2A' : '#DCDFE6'"
              />
            </svg>
          </div>
        </div>
        <p class="stars-text">
          获得 {{ result.totalStars }}/3 星
          <span v-if="result.totalStars === 3" class="perfect-badge">完美！</span>
        </p>
      </div>

      <!-- 三维度得分 -->
      <div class="dimensions-section">
        <h4 class="section-title">维度评分</h4>
        <div class="dimension-list">
          <div class="dimension-item">
            <div class="dimension-header">
              <span class="dimension-name">功能实现度</span>
              <span class="dimension-score">{{ result.functionScore }}/3</span>
            </div>
            <div class="dimension-bar">
              <div
                class="dimension-fill"
                :style="{ width: `${(result.functionScore / 3) * 100}%` }"
                :class="getScoreClass(result.functionScore)"
              ></div>
            </div>
          </div>

          <div class="dimension-item">
            <div class="dimension-header">
              <span class="dimension-name">代码规范度</span>
              <span class="dimension-score">{{ result.standardScore }}/3</span>
            </div>
            <div class="dimension-bar">
              <div
                class="dimension-fill"
                :style="{ width: `${(result.standardScore / 3) * 100}%` }"
                :class="getScoreClass(result.standardScore)"
              ></div>
            </div>
          </div>

          <div class="dimension-item">
            <div class="dimension-header">
              <span class="dimension-name">性能与酷炫度</span>
              <span class="dimension-score">{{ result.coolScore }}/3</span>
            </div>
            <div class="dimension-bar">
              <div
                class="dimension-fill"
                :style="{ width: `${(result.coolScore / 3) * 100}%` }"
                :class="getScoreClass(result.coolScore)"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI评语 -->
      <div class="comment-section">
        <h4 class="section-title">AI评语</h4>
        <div class="comment-content">
          <p>{{ result.comment }}</p>
        </div>
        <div v-if="result.hint" class="hint-box">
          <el-icon><Info-Filled /></el-icon>
          <span>{{ result.hint }}</span>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-section">
        <el-button
          v-if="result.totalStars < 3"
          type="primary"
          size="large"
          @click="handleRetry"
        >
          <el-icon><Refresh-Right /></el-icon>
          再试一次
        </el-button>

        <el-button
          v-else
          type="success"
          size="large"
          @click="handleNext"
        >
          <el-icon><Arrow-Right /></el-icon>
          下一关
        </el-button>

        <el-button
          type="info"
          size="large"
          plain
          @click="handleAskMentor"
        >
          <el-icon><Chat-Dot-Square /></el-icon>
          呼叫导师问问
        </el-button>

        <el-button
          size="large"
          plain
          @click="handleClose"
        >
          关闭
        </el-button>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, watch } from 'vue'
import { RefreshRight, ArrowRight, ChatDotSquare, InfoFilled } from '@element-plus/icons-vue'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  },
  result: {
    type: Object,
    default: () => ({
      functionScore: 0,
      standardScore: 0,
      coolScore: 0,
      totalStars: 0,
      comment: '',
      hint: ''
    })
  }
})

const emit = defineEmits(['update:modelValue', 'retry', 'next', 'ask-mentor', 'close'])

const visible = ref(props.modelValue)
const showAnimation = ref(false)

// 监听visible变化
watch(() => props.modelValue, (val) => {
  visible.value = val
  if (val) {
    // 显示时触发动画
    setTimeout(() => {
      showAnimation.value = true
    }, 100)
  } else {
    showAnimation.value = false
  }
})

watch(() => visible.value, (val) => {
  emit('update:modelValue', val)
})

// 获取分数对应的样式类
const getScoreClass = (score) => {
  if (score >= 3) return 'excellent'
  if (score >= 2) return 'good'
  return 'normal'
}

// 处理再试一次
const handleRetry = () => {
  visible.value = false
  emit('retry')
}

// 处理下一关
const handleNext = () => {
  visible.value = false
  emit('next')
}

// 处理呼叫导师
const handleAskMentor = () => {
  visible.value = false
  emit('ask-mentor')
}

// 处理关闭
const handleClose = () => {
  visible.value = false
  emit('close')
}
</script>

<style scoped lang="scss">
.judge-result-dialog {
  :deep(.el-dialog__header) {
    display: none;
  }

  :deep(.el-dialog__body) {
    padding: 0;
  }
}

.result-container {
  padding: 30px;
}

// 星数展示区域
.stars-section {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 25px;
  border-bottom: 1px solid #EBEEF5;
}

.result-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 20px 0;
}

.stars-display {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 15px;
}

.star-item {
  width: 60px;
  height: 60px;
  opacity: 0.3;
  transform: scale(0.8);
  transition: all 0.5s ease;

  &.filled {
    opacity: 1;
    transform: scale(1);
  }

  &.animate {
    animation: starPop 0.6s ease forwards;
  }
}

@keyframes starPop {
  0% {
    transform: scale(0) rotate(-180deg);
    opacity: 0;
  }
  50% {
    transform: scale(1.2) rotate(10deg);
  }
  100% {
    transform: scale(1) rotate(0deg);
    opacity: 1;
  }
}

.star-svg {
  width: 100%;
  height: 100%;
  filter: drop-shadow(0 2px 4px rgba(247, 186, 42, 0.3));
}

.stars-text {
  font-size: 16px;
  color: #606266;
  margin: 0;

  .perfect-badge {
    display: inline-block;
    margin-left: 10px;
    padding: 2px 10px;
    background: linear-gradient(135deg, #F7BA2A, #FF6B6B);
    color: #fff;
    font-size: 12px;
    font-weight: 600;
    border-radius: 10px;
    animation: pulse 1.5s ease infinite;
  }
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

// 维度评分区域
.dimensions-section {
  margin-bottom: 25px;
}

.section-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 15px 0;
}

.dimension-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.dimension-item {
  background: #F5F7FA;
  padding: 12px 15px;
  border-radius: 8px;
}

.dimension-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.dimension-name {
  font-size: 13px;
  color: #606266;
}

.dimension-score {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.dimension-bar {
  height: 8px;
  background: #DCDFE6;
  border-radius: 4px;
  overflow: hidden;
}

.dimension-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 1s ease;

  &.excellent {
    background: linear-gradient(90deg, #67C23A, #85CE61);
  }

  &.good {
    background: linear-gradient(90deg, #E6A23C, #EBB563);
  }

  &.normal {
    background: linear-gradient(90deg, #909399, #A6A9AD);
  }
}

// 评语区域
.comment-section {
  margin-bottom: 25px;
}

.comment-content {
  background: #F5F7FA;
  padding: 15px;
  border-radius: 8px;
  border-left: 4px solid #409EFF;

  p {
    margin: 0;
    font-size: 14px;
    color: #606266;
    line-height: 1.8;
  }
}

.hint-box {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-top: 12px;
  padding: 10px 12px;
  background: #FDF6EC;
  border: 1px solid #F5DAB1;
  border-radius: 6px;

  .el-icon {
    color: #E6A23C;
    font-size: 16px;
    margin-top: 2px;
  }

  span {
    font-size: 13px;
    color: #8C6B3D;
    line-height: 1.5;
  }
}

// 操作按钮区域
.action-section {
  display: flex;
  justify-content: center;
  gap: 12px;
  padding-top: 20px;
  border-top: 1px solid #EBEEF5;

  .el-button {
    min-width: 120px;

    .el-icon {
      margin-right: 6px;
    }
  }
}

/* 响应式适配 */
@media (max-width: 1366px) {
  .result-container {
    padding: 20px;
  }

  .star-item {
    width: 50px;
    height: 50px;
  }

  .action-section {
    flex-wrap: wrap;

    .el-button {
      min-width: 100px;
    }
  }
}

@media (max-width: 768px) {
  .judge-result-dialog {
    :deep(.el-dialog) {
      width: 90% !important;
      margin: 10vh auto;
    }
  }

  .action-section {
    flex-direction: column;

    .el-button {
      width: 100%;
    }
  }
}
</style>
