<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, nextTick } from "vue";
import { useRoute } from "vitepress";
import { useTemplateRef } from "vue";

const route = useRoute();
const dialogRef = useTemplateRef<HTMLDialogElement>("dialogRef");
const svgWrapperRef = useTemplateRef<HTMLDivElement>("svgWrapperRef");
const scale = ref(1);
const translateX = ref(0);
const translateY = ref(0);
const isPanning = ref(false);
const panStart = { x: 0, y: 0 };

let observer: MutationObserver | null = null;

function attachClickHandlers() {
  // Mermaid SVG containers
  const containers = document.querySelectorAll<HTMLElement>(".mermaid");
  for (const container of containers) {
    if (container.dataset.zoomReady) continue;
    const svg = container.querySelector("svg");
    if (!svg) continue;
    container.dataset.zoomReady = "true";
    container.style.cursor = "pointer";
    container.setAttribute("title", "Click to zoom");
    container.addEventListener("click", () => {
      const currentSvg = container.querySelector("svg");
      if (currentSvg) openSvgZoom(currentSvg);
    });
  }

  // Doc images (markdown images + gallery images)
  const images = document.querySelectorAll<HTMLImageElement>(
    ".vp-doc img, .image-gallery img",
  );
  for (const img of images) {
    if (img.dataset.zoomReady) continue;
    // Skip tiny images (icons, badges)
    if (img.naturalWidth > 0 && img.naturalWidth < 64) continue;
    img.dataset.zoomReady = "true";
    img.style.cursor = "pointer";
    img.setAttribute("title", "Click to zoom");
    img.addEventListener("click", (e) => {
      e.preventDefault();
      e.stopPropagation();
      openImageZoom(img.currentSrc || img.src, img.alt);
    });
  }
}

function observeForMermaid() {
  observer?.disconnect();

  const target = document.querySelector(".vp-doc");
  if (!target) return;

  observer = new MutationObserver(() => {
    attachClickHandlers();
  });

  observer.observe(target, { childList: true, subtree: true });

  // Also try immediately in case Mermaid already rendered
  attachClickHandlers();
}

function openSvgZoom(svg: SVGElement) {
  // Clone the live DOM node — avoids XMLSerializer namespace issues and
  // preserves all inline styles, <style> blocks, and <defs> references.
  const clone = svg.cloneNode(true) as SVGElement;

  // Mermaid sets width="100%" on the SVG and controls actual size via
  // max-width in the inline style.  Stripping that style collapses the SVG.
  // Fix: read the viewBox to get the real pixel dimensions, set them as
  // explicit width/height attributes, then strip the inline style.
  clone.removeAttribute("style");

  const viewBox = clone.getAttribute("viewBox");
  if (viewBox) {
    const parts = viewBox.split(/[\s,]+/);
    if (parts.length === 4) {
      clone.setAttribute("width", parts[2]);
      clone.setAttribute("height", parts[3]);
    }
  }

  // Deduplicate the SVG id to avoid clashing with the still-visible original
  const origId = clone.getAttribute("id");
  if (origId) {
    const newId = `${origId}-zoom`;
    clone.setAttribute("id", newId);
    const styleEl = clone.querySelector("style");
    if (styleEl?.textContent) {
      styleEl.textContent = styleEl.textContent.replaceAll(origId, newId);
    }
  }

  const wrapper = svgWrapperRef.value;
  if (wrapper) {
    wrapper.innerHTML = "";
    wrapper.appendChild(clone);
  }

  resetAndShow();
}

function openImageZoom(src: string, alt: string) {
  const wrapper = svgWrapperRef.value;
  if (wrapper) {
    const img = document.createElement("img");
    img.src = src;
    img.alt = alt;
    img.draggable = false;
    wrapper.innerHTML = "";
    wrapper.appendChild(img);
  }

  resetAndShow();
}

function resetAndShow() {
  scale.value = 1;
  translateX.value = 0;
  translateY.value = 0;

  nextTick(() => {
    dialogRef.value?.showModal();
  });
}

function closeZoom() {
  dialogRef.value?.close();
  // Remove the clone so duplicate IDs don't linger
  const wrapper = svgWrapperRef.value;
  if (wrapper) wrapper.innerHTML = "";
}

function onWheel(e: WheelEvent) {
  e.preventDefault();
  const delta = e.deltaY > 0 ? -0.1 : 0.1;
  scale.value = Math.min(Math.max(0.2, scale.value + delta), 5);
}

function onPointerDown(e: PointerEvent) {
  if (e.button !== 0) return;
  isPanning.value = true;
  panStart.x = e.clientX - translateX.value;
  panStart.y = e.clientY - translateY.value;
  (e.target as HTMLElement)?.setPointerCapture?.(e.pointerId);
}

function onPointerMove(e: PointerEvent) {
  if (!isPanning.value) return;
  translateX.value = e.clientX - panStart.x;
  translateY.value = e.clientY - panStart.y;
}

function onPointerUp() {
  isPanning.value = false;
}

function onBackdropClick(e: MouseEvent) {
  if (e.target === dialogRef.value) {
    closeZoom();
  }
}

onMounted(() => {
  observeForMermaid();
});

watch(
  () => route.path,
  () => {
    nextTick(() => {
      observeForMermaid();
    });
  },
);

onUnmounted(() => {
  observer?.disconnect();
});
</script>

<template>
  <dialog
    ref="dialogRef"
    class="mermaid-zoom-dialog"
    @click="onBackdropClick"
    @wheel.prevent="onWheel"
  >
    <div class="mermaid-zoom-container">
      <button
        class="mermaid-zoom-close"
        aria-label="Close"
        @click="closeZoom"
      >
        ✕
      </button>
      <div class="mermaid-zoom-controls">
        <span class="mermaid-zoom-hint">Scroll to zoom · Drag to pan</span>
      </div>
      <div
        ref="svgWrapperRef"
        class="mermaid-zoom-svg"
        :style="{
          transform: `translate(${translateX}px, ${translateY}px) scale(${scale})`,
        }"
        @pointerdown="onPointerDown"
        @pointermove="onPointerMove"
        @pointerup="onPointerUp"
        @pointercancel="onPointerUp"
      />
    </div>
  </dialog>
</template>
