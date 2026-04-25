import DefaultTheme from "vitepress/theme";
import MermaidZoom from "./MermaidZoom.vue";
import ImageGallery from "./ImageGallery.vue";
import "./mermaid-zoom.css";

import type { Theme } from "vitepress";
import { h } from "vue";

export default {
  extends: DefaultTheme,
  Layout() {
    return h(DefaultTheme.Layout, null, {
      "layout-bottom": () => h(MermaidZoom),
    });
  },
  enhanceApp({ app }) {
    app.component("ImageGallery", ImageGallery);
  },
} satisfies Theme;
