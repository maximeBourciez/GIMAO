<template>

</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import BaseForm from '@/components/common/BaseForm.vue';
import { useApi } from '@/composables/useApi';
import { useFormValidation } from '@/composables/useFormValidation';
import { getFailureLevelColor } from '@/utils/helpers';
import { API_BASE_URL } from '@/utils/constants';
import '@/assets/css/global.css';
</script>
