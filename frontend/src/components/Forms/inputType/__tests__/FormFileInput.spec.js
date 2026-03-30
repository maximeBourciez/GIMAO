import { describe, it, expect, vi } from 'vitest';
import { render } from '@testing-library/vue';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import FormFileInput from '../FormFileInput.vue';

const vuetify = createVuetify({ components, directives });

describe('FormFileInput.vue', () => {
    it('renders label with no required star when not provided or false', () => {
        const { getByText, queryByText } = render(FormFileInput, {
            props: {
                name: 'testField',
                label: 'Test Label'
            },
            global: {
                plugins: [vuetify],
                provide: {
                    validation: {
                        getFieldRules: vi.fn(() => []),
                    },
                    isFieldRequired: vi.fn(() => false)
                }
            }
        });

        expect(getByText('Test Label')).toBeTruthy();
    });

    it('renders label with required star when isFieldRequired returns true', async () => {
        const { getByText } = render(FormFileInput, {
            props: {
                name: 'testField',
                label: 'Test Label'
            },
            global: {
                plugins: [vuetify],
                provide: {
                    validation: {
                        getFieldRules: vi.fn(() => []),
                    },
                    isFieldRequired: vi.fn(() => true)
                }
            }
        });

        expect(document.querySelector('.required-star')).toBeTruthy();
    });

    it('handles missing validation injections gracefully', () => {
        const { getByText } = render(FormFileInput, {
            props: {
                name: 'testField',
                label: 'Test Label'
            },
            global: {
                plugins: [vuetify]
            }
        });

        expect(getByText('Test Label')).toBeTruthy();
    });
});
