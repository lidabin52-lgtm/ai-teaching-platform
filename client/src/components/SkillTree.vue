<template>
  <!-- 技能树/闯关进度地图组件 -->
  <div class="skill-tree">
    <div class="tree-header">
      <h3 class="tree-title">技能闯关地图</h3>
      <div class="legend">
        <div class="legend-item">
          <span class="legend-dot completed"></span>
          <span>已通关</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot current"></span>
          <span>当前挑战</span>
        </div>
        <div class="legend-item">
          <span class="legend-dot locked"></span>
          <span>未解锁</span>
        </div>
      </div>
    </div>

    <div class="tree-content">
      <!-- 段位分组 -->
      <div v-for="group in groupedChallenges" :key="group.difficulty" class="difficulty-group">
        <div class="difficulty-header" :style="{ borderColor: group.color }">
          <span class="difficulty-badge" :style="{ backgroundColor: group.color }">
            {{ group.label }}
          </span>
          <span class="difficulty-progress">
            {{ group.completedCount }}/{{ group.challenges.length }}
          </span>
        </div>

        <div class="challenge-nodes">
          <div
            v-for="(challenge, index) in group.challenges"
            :key="challenge.id"
            class="node-wrapper"
          >
            <!-- 连接线 -->
            <div
              v-if="index > 0"
              class="node-connector"
              :class="{ active: challenge.status !== 'locked' }"
            ></div>

            <!-- 节点 -->
            <div
              class="challenge-node"
              :class="[
                challenge.status,
                { 'is-current': challenge.id === currentChallengeId }
              ]"
              :style="{ borderColor: getNodeColor(challenge) }"
              @click="handleNodeClick(challenge)"
            >
              <!-- 节点内容 -->
              <div class="node-content">
                <span class="node-number">{{ challenge.orderNum }}</span>
                <span class="node-title" :title="challenge.title">
                  {{ truncateTitle(challenge.title) }}
                </span>
              </div>

              <!-- 星数显示 -->
              <div v-if="challenge.status === 'completed'" class="node-stars">
                <span
                  v-for="n in 3"
                  :key="n"
                  class="star"
                  :class="{ filled: n <= (challenge.bestStars || 0) }"
                >
                  ★
                </span>
              </div>

              <!-- 锁定图标 -->
              <div v-if="challenge.status === 'locked'" class="node-lock">
                <el-icon><Lock /></el-icon>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Lock } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'

const props = defineProps({
  challenges: {
    type: Array,
    default: () => []
  },
  currentChallengeId: {
    type: Number,
    default: null
  }
})

const emit = defineEmits(['select'])
const router = useRouter()

// 段位配置
const difficultyConfig = {
  bronze: { label: '青铜', color: '#CD7F32', order: 1 },
  silver: { label: '白银', color: '#C0C0C0', order: 2 },
  gold: { label: '黄金', color: '#FFD700', order: 3 },
  diamond: { label: '钻石', color: '#B9F2FF', order: 4 },
  king: { label: '王者', color: '#FF6B6B', order: 5 }
}

// 按段位分组
const groupedChallenges = computed(() => {
  const groups = {}

  props.challenges.forEach(challenge => {
    const diff = challenge.difficulty || 'bronze'
    if (!groups[diff]) {
      groups[diff] = {
        difficulty: diff,
        label: difficultyConfig[diff]?.label || diff,
        color: difficultyConfig[diff]?.color || '#999',
        order: difficultyConfig[diff]?.order || 99,
        challenges: [],
        completedCount: 0
      }
    }
    groups[diff].challenges.push(challenge)
    if (challenge.status === 'completed') {
      groups[diff].completedCount++
    }
  })

  // 按段位顺序排序
  return Object.values(groups).sort((a, b) => a.order - b.order)
})

// 获取节点颜色
const getNodeColor = (challenge) => {
  if (challenge.status === 'completed') {
    return '#67C23A'
  }
  if (challenge.status === 'unlocked') {
    return difficultyConfig[challenge.difficulty]?.color || '#409EFF'
  }
  return '#909399'
}

// 截断标题
const truncateTitle = (title) => {
  if (title.length > 8) {
    return title.substring(0, 8) + '...'
  }
  return title
}

// 处理节点点击
const handleNodeClick = (challenge) => {
  if (challenge.status === 'locked') {
    return
  }

  emit('select', challenge)
  router.push(`/challenge/${challenge.id}`)
}
</script>

<style scoped lang="scss">
.skill-tree {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.tree-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #EBEEF5;
}

.tree-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.legend {
  display: flex;
  gap: 16px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #606266;
}

.legend-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;

  &.completed {
    background-color: #67C23A;
  }

  &.current {
    background-color: #409EFF;
    border: 2px solid #409EFF;
  }

  &.locked {
    background-color: #C0C4CC;
  }
}

.tree-content {
  flex: 1;
  overflow-y: auto;
}

.difficulty-group {
  margin-bottom: 24px;

  &:last-child {
    margin-bottom: 0;
  }
}

.difficulty-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  padding-left: 8px;
  border-left: 4px solid;
}

.difficulty-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  color: #fff;
}

.difficulty-progress {
  font-size: 13px;
  color: #909399;
}

.challenge-nodes {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  padding-left: 20px;
}

.node-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.node-connector {
  width: 20px;
  height: 2px;
  background-color: #DCDFE6;
  transition: background-color 0.3s;

  &.active {
    background-color: #67C23A;
  }
}

.challenge-node {
  position: relative;
  width: 100px;
  padding: 12px 8px;
  border: 2px solid;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  background: #fff;

  &:hover:not(.locked) {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  &.completed {
    background-color: #F0F9EB;
    border-color: #67C23A;
  }

  &.unlocked {
    background-color: #ECF5FF;
    border-color: #409EFF;

    &:hover {
      background-color: #D9ECFF;
    }
  }

  &.locked {
    background-color: #F5F7FA;
    border-color: #C0C4CC;
    cursor: not-allowed;
    opacity: 0.7;
  }

  &.is-current {
    box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.3);
  }
}

.node-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.node-number {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
}

.node-title {
  font-size: 11px;
  color: #606266;
  text-align: center;
  line-height: 1.3;
}

.node-stars {
  display: flex;
  justify-content: center;
  gap: 2px;
  margin-top: 6px;

  .star {
    font-size: 10px;
    color: #DCDFE6;

    &.filled {
      color: #F7BA2A;
    }
  }
}

.node-lock {
  position: absolute;
  top: 4px;
  right: 4px;
  color: #909399;
  font-size: 12px;
}

/* 响应式适配 */
@media (max-width: 1366px) {
  .skill-tree {
    padding: 15px;
  }

  .tree-title {
    font-size: 16px;
  }

  .legend {
    gap: 12px;
  }

  .challenge-node {
    width: 85px;
    padding: 10px 6px;
  }

  .node-title {
    font-size: 10px;
  }
}

@media (max-width: 1200px) {
  .challenge-nodes {
    padding-left: 10px;
  }

  .challenge-node {
    width: 75px;
    padding: 8px 4px;
  }

  .node-number {
    font-size: 12px;
  }

  .node-title {
    font-size: 9px;
  }
}
</style>
