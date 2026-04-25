<script setup lang="ts">
defineProps<{
  images: Array<{ src: string; alt: string }>;
  columns?: number;
}>();
</script>

<template>
  <div class="image-gallery" :style="{ '--cols': columns ?? 2 }">
    <figure v-for="img in images" :key="img.src" class="image-gallery-item">
      <img :src="img.src" :alt="img.alt" loading="lazy" />
      <figcaption v-if="img.alt">{{ img.alt }}</figcaption>
    </figure>
  </div>
</template>

<style scoped>
.image-gallery {
  display: grid;
  grid-template-columns: repeat(var(--cols, 2), 1fr);
  gap: 16px;
  margin: 24px 0;
}

@media (max-width: 640px) {
  .image-gallery {
    grid-template-columns: 1fr;
  }
}

.image-gallery-item {
  margin: 0;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
  transition: border-color 0.2s ease;
}

.image-gallery-item:hover {
  border-color: var(--vp-c-brand-1);
}

.image-gallery-item img {
  width: 100%;
  height: auto;
  display: block;
  cursor: pointer;
}

.image-gallery-item figcaption {
  padding: 8px 12px;
  font-size: 13px;
  color: var(--vp-c-text-2);
  text-align: center;
}
</style>
