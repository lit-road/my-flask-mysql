import { unheadVueComposablesImports } from '@unhead/vue'
import vue                             from '@vitejs/plugin-vue'
import { fileURLToPath, URL }          from 'node:url'
import AutoImport                      from 'unplugin-auto-import/vite'
import Components                      from 'unplugin-vue-components/vite'
// 使用了element-plus 第三方库
import { ElementPlusResolver }         from 'unplugin-vue-components/resolvers'
import { defineConfig }                from 'vite'
import { version as pkgVersion }       from './package.json'

process.env.VITE_APP_VERSION = pkgVersion
if (process.env.NODE_ENV === 'production') {
  process.env.VITE_APP_BUILD_EPOCH = new Date().getTime().toString()
}

export default defineConfig({
  plugins: [
    vue(),
    AutoImport({
      imports: [
        'vue',
        'vue-router',
        'pinia',
        {
          '@/store': ['useStore'],
        },
        unheadVueComposablesImports,
      ],
      dts: 'auto-imports.d.ts',
      vueTemplate: true,
      eslintrc: {
        enabled: true,
      },
      resolvers: [ElementPlusResolver()],
    }),
    Components({
      resolvers: [ElementPlusResolver()],
      dts: 'components.d.ts',
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    cors: true,
  },
})
