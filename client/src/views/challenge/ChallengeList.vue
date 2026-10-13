<template>
  <!-- 关卡列表页面 -->
  <div class="challenge-list-page">
    <div class="page-header">
      <h2>技能闯关</h2>
      <p>通过实战闯关，提升前端开发技能</p>
    </div>

    <div class="challenge-content">
      <SkillTree
        :challenges="challengeList"
        @select="handleSelectChallenge"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useChallengeStore } from '@/store/challenge'
import { useRouter } from 'vue-router'
import SkillTree from '@/components/SkillTree.vue'

const store = useChallengeStore()
const router = useRouter()
const { challengeList } = storeToRefs(store)

onMounted(async () => {
  await store.loadChallengeList()
})

const handleSelectChallenge = (challenge) => {
  router.push(`/challenge/${challenge.id}`)
}
</script>

<style scoped lang="scss">
.challenge-list-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;

  h2 {
    font-size: 28px;
    color: #303133;
    margin-bottom: 8px;
  }

  p {
    color: #909399;
    font-size: 14px;
  }
}

.challenge-content {
  min-height: 600px;
}
</style>
