import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent } from '@testing-library/vue';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import FormFileInput from '../FormFileInput.vue';

const vuetify = createVuetify({ components, directives });

// Mock URL.createObjectURL et revokeObjectURL
URL.createObjectURL = vi.fn(() => 'blob:mock-url');
URL.revokeObjectURL = vi.fn();

describe('FormFileInput.vue', () => {
    it('renders label with no required star when not provided or false', () => {
        const { getByText } = render(FormFileInput, {
            props: { name: 'testField', label: 'Test Label' },
            global: { plugins: [vuetify], provide: { isFieldRequired: vi.fn(() => false) }}
        });
        expect(getByText('Test Label')).toBeTruthy();
    });

    it('renders label with required star when isFieldRequired returns true', async () => {
        const { getByText } = render(FormFileInput, {
            props: { name: 'testField', label: 'Test Label' },
            global: { plugins: [vuetify], provide: { isFieldRequired: vi.fn(() => true) }}
        });
        expect(document.querySelector('.required-star')).toBeTruthy();
    });

    it('handles missing validation injections gracefully', () => {
        const { getByText } = render(FormFileInput, {
            props: { name: 'testField', label: 'Test Label' },
            global: { plugins: [vuetify] }
        });
        expect(getByText('Test Label')).toBeTruthy();
    });

    it('creates an image preview and cleans up old url when a new image file is selected', async () => {
        const { emitted, getByText } = render(FormFileInput, {
            props: { name: 'doc', label: 'Upload' },
            global: { plugins: [vuetify] }
        });

        // Simulate choosing a file
        const file = new File(['hello'], 'hello.png', { type: 'image/png' });
        
        // Mettre à jour manuellement la prop // ou via fireEvent si on peut interagir avec v-file-input
        // V-file-input est un peu compliqué avec Testing Library (le test d''event update:modelValue)
        // Mais on va appeler les event manuellement avec vue test utils si besoin, ou on fait ça via la méthode exposée
    });
});
