<script>
export default {
  name: "card-component",
};
</script>

<template>
  <div class="my-4 flex flex-wrap">
    <div class="w-full px-4">
      <div
        class="relative block h-[74vh] flex w-full flex-col break-words rounded shadow-lg dark:shadow-md dark:shadow-kTertiaryColor"
      >
        <div class="mb-0 rounded-t border-0 px-4 py-3">
          <div class="flex flex-wrap items-center">
            <div class="relative w-full max-w-full flex-1 flex-grow">
              <h3 class="text-lg font-semibold">
                <slot name="title"></slot>
              </h3>
            </div>
          </div>
        </div>
        <div class="w-full overflow-x-auto px-4 print:h-auto">
          <slot name="content"></slot>
        </div>

        <slot name="footer"></slot>
      </div>
    </div>
  </div>
</template>
