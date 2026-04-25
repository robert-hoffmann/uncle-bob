import { withMermaid } from "vitepress-plugin-mermaid";

const base = "/uncle-bob/";
const githubUrl = "https://github.com/robert-hoffmann/uncle-bob";

export default withMermaid({
  title       : "Uncle Bob",
  description :
    "Workflow-first AI coding skills and custom agents for planning, quality, governance, authoring, and implementation work.",

  base,
  outDir     : "../dist",
  srcExclude : [
    "AGENTS.md",
  ],

  head   : [
    [
      "link",
      {
        rel   : "icon",
        type  : "image/png",
        sizes : "32x32",
        href  : `${base}brand/uncle-bob.png`,
      },
    ],
  ],

  themeConfig : {
    siteTitle : "Uncle Bob",

    nav : [
      {
        text : "Install",
        link : "/install",
      },
      {
        text : "Concepts",
        link : "/guide/skill-system",
      },
      {
        text : "Skills",
        link : "/skills/",
      },
      {
        text : "Deep Dives",
        link : "/deep-dives/ub-workflow",
      },
    ],

    sidebar : [
      {
        text  : "Start",
        items : [
          {
            text : "Overview",
            link : "/",
          },
          {
            text : "Install",
            link : "/install",
          },
        ],
      },
      {
        text  : "Concepts",
        items : [
          {
            text : "Skill System",
            link : "/guide/skill-system",
          },
          {
            text : "Core Stack",
            link : "/guide/core-stack",
          },
          {
            text : "Routing Model",
            link : "/guide/routing-model",
          },
          {
            text : "References And Disclosure",
            link : "/guide/references-progressive-disclosure",
          },
          {
            text : "Portability Model",
            link : "/guide/portability-model",
          },
        ],
      },
      {
        text  : "Skills",
        items : [
          {
            text : "Skill Catalog",
            link : "/skills/",
          },
          {
            text : "UB Quality",
            link : "/skills/ub-quality",
          },
          {
            text : "UB Authoring",
            link : "/skills/ub-authoring",
          },
          {
            text : "UB Workflow",
            link : "/skills/ub-workflow",
          },
          {
            text : "UB Governance",
            link : "/skills/ub-governance",
          },
          {
            text : "UB Customizations",
            link : "/skills/ub-customizations",
          },
          {
            text : "UB Python",
            link : "/skills/ub-python",
          },
          {
            text : "UB TypeScript",
            link : "/skills/ub-ts",
          },
          {
            text : "UB Vue",
            link : "/skills/ub-vuejs",
          },
          {
            text : "UB Nuxt",
            link : "/skills/ub-nuxt",
          },
          {
            text : "UB CSS",
            link : "/skills/ub-css",
          },
          {
            text : "UB Tailwind",
            link : "/skills/ub-tailwind",
          },
        ],
      },
      {
        text  : "Deep Dives",
        items : [
          {
            text : "UB Workflow",
            link : "/deep-dives/ub-workflow",
          },
          {
            text : "UB Governance",
            link : "/deep-dives/ub-governance",
          },
          {
            text : "Workflow + Governance",
            link : "/deep-dives/workflow-governance",
          },
        ],
      },
    ],

    socialLinks : [
      {
        icon : "github",
        link : githubUrl,
      },
    ],

    search : {
      provider : "local",
    },

    editLink : {
      pattern : `${githubUrl}/edit/main/docs/:path`,
      text    : "Edit this page on GitHub",
    },

    footer : {
      message   : "Uncle Bob skill system documentation",
      copyright : "© 2026 Robert Hoffmann",
    },
  },

  mermaid : {
    // Theme is auto-detected from dark mode
  },
});
