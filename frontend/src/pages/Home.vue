<script setup lang="ts">
import {
  Badge,
  Button,
  ErrorMessage,
  PageHeader,
  PageHeaderTitle,
  useCall,
  useColorScheme,
} from 'frappe-ui'

const { resolvedColorScheme, toggleColorScheme } = useColorScheme()

const bootUser = window.user

// This built-in GET endpoint is safe for the development smoke and does not
// need a logged-in user or product data.
const backendPing = useCall<string>({
  url: '/api/v2/method/frappe.ping',
})
</script>

<template>
  <PageHeader>
    <PageHeaderTitle title="Service Hub System" />
    <div class="flex items-center gap-2">
      <Button
        :icon="resolvedColorScheme === 'dark' ? 'lucide-sun' : 'lucide-moon'"
        :tooltip="resolvedColorScheme === 'dark' ? 'Light mode' : 'Dark mode'"
        aria-label="Switch light and dark mode"
        @click="toggleColorScheme"
      />
      <Button icon-left="lucide-layout-grid" label="Open Desk" href="/app" />
    </div>
  </PageHeader>

  <div class="mx-auto max-w-[770px] space-y-6 px-3 pb-10 pt-8 sm:px-5">
    <div class="space-y-2">
      <h1 class="text-2xl-semibold text-ink-gray-9">Your frontend is ready</h1>
      <p class="text-p-base text-ink-gray-7">
        Edit
        <code class="rounded-1 bg-surface-gray-2 px-1 py-0.5 font-mono text-sm"
          >src/pages/Home.vue</code
        >
        to start building. The checks below show that the page can talk to your
        site.
      </p>
    </div>

    <div
      class="divide-y divide-outline-gray-1 rounded-6 border border-outline-gray-1"
    >
      <div class="flex items-center gap-3 px-4 py-3">
        <span
          class="lucide-file-json size-4 shrink-0 text-ink-gray-6"
          aria-hidden="true"
        />
        <div class="min-w-0 flex-1">
          <p class="text-base-medium text-ink-gray-8">Boot data</p>
          <p class="mt-1.5 truncate text-sm text-ink-gray-5">
            {{
              bootUser
                ? `Signed in as ${bootUser}`
                : 'Only a production build has boot data'
            }}
          </p>
        </div>
        <Badge
          :theme="bootUser ? 'green' : 'gray'"
          :label="bootUser ? 'Loaded' : 'Dev server'"
        />
      </div>

      <div class="flex items-center gap-3 px-4 py-3">
        <span
          class="lucide-server size-4 shrink-0 text-ink-gray-6"
          aria-hidden="true"
        />
        <div class="min-w-0 flex-1">
          <p class="text-base-medium text-ink-gray-8">Backend smoke</p>
          <ErrorMessage
            v-if="backendPing.error"
            class="mt-1.5"
            :message="backendPing.error"
          />
          <p v-else class="mt-1.5 truncate text-sm text-ink-gray-5">
            {{
              backendPing.data
                ? `frappe.ping returned ${backendPing.data}`
                : 'Calling frappe.ping…'
            }}
          </p>
        </div>
        <Badge v-if="backendPing.data" theme="green" label="Working" />
        <Badge v-else-if="backendPing.error" theme="red" label="Failed" />
        <Button
          icon="lucide-refresh-cw"
          tooltip="Call again"
          aria-label="Call again"
          :loading="backendPing.loading"
          @click="backendPing.reload()"
        />
      </div>
    </div>
  </div>
</template>
