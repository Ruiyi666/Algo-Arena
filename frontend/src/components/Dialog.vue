<template>
     <dialog ref="dialog" class="modal modal-bottom sm:modal-middle">
        <form method="dialog" class="modal-box">
            <h3 class="text-lg font-bold">{{ dialog_title }}</h3>
            <p class="py-4">{{ dialog_content }}</p>
            <div class="modal-action">
                <!-- if there is a button in form, it will close the modal -->
                <button class="btn">Close</button>
            </div>
        </form>
    </dialog>
</template>

<script setup>
import { ref } from 'vue';

const dialog = ref(null)
const dialog_title = ref(null)
const dialog_content = ref(null)

function showModal(title, content) {
    dialog_title.value = title
    dialog_content.value = content
    dialog.value.showModal()
}

defineExpose({ showModal })
</script>

<style lang="scss" scoped>

</style>