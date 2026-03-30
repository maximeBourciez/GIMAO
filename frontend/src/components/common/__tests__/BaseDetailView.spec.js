import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent } from '@testing-library/vue';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import BaseDetailView from '../BaseDetailView.vue';
import { createRouter, createWebHistory } from 'vue-router';

const vuetify = createVuetify({ components, directives });

const router = createRouter({
  history: createWebHistory(),
  routes: [{ path: '/', component: { template: '<div>Home</div>' } }]
});
router.go = vi.fn();
router.push = vi.fn();

describe('BaseDetailView.vue', () => {
    it('renders the title and back button', async () => {
        const { getByText } = render(BaseDetailView, {
            props: {
                title: 'D�tails du test',
                showBackButton: true,
            },
            global: {
                plugins: [vuetify, router]
            }
        });

        expect(getByText('D�tails du test')).toBeTruthy();
        const backBtn = getByText('Retour');
        expect(backBtn).toBeTruthy();

        await fireEvent.click(backBtn);
        expect(router.go).toHaveBeenCalledWith(-1);
    });
});
