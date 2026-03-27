import { computed, onBeforeUnmount, ref, unref, watch } from 'vue';

const PAGINATION_KEYS = new Set(['count', 'next', 'previous', 'results']);

const toSearchValue = (value) => {
  if (typeof value === 'string') {
    return value;
  }

  if (value && typeof value === 'object' && typeof value.target?.value === 'string') {
    return value.target.value;
  }

  return '';
};

const normalizeResponse = (response) => {
  if (Array.isArray(response)) {
    // Compatibilite avec les endpoints encore non pagines : on expose
    // la meme structure cote composant pour eviter des branches partout.
    return {
      items: response,
      totalItems: response.length,
      extra: {},
    };
  }

  const items = Array.isArray(response?.results) ? response.results : [];
  const extra = {};

  if (response && typeof response === 'object') {
    for (const [key, value] of Object.entries(response)) {
      if (!PAGINATION_KEYS.has(key)) {
        extra[key] = value;
      }
    }
  }

  return {
    items,
    totalItems: Number(response?.count || 0),
    extra,
  };
};

export function usePaginatedList({
  api,
  endpoint,
  initialPageSize = 10,
  debounceMs = 300,
  buildParams = () => ({}),
  watchSource = null,
  enabled = true,
  onFetched = null,
}) {
  const items = ref([]);
  const currentPage = ref(1);
  const pageSize = ref(initialPageSize);
  const searchQuery = ref('');
  const totalItems = ref(0);
  const extra = ref({});
  const errorMessage = ref('');

  let searchTimeoutId = null;

  const loading = computed(() => api.loading.value);
  const totalPages = computed(() => {
    if (pageSize.value <= 0) return 1;
    return Math.max(1, Math.ceil(totalItems.value / pageSize.value));
  });

  const resolveEndpoint = () => (typeof endpoint === 'function' ? endpoint() : unref(endpoint));
  const resolveEnabled = () => (typeof enabled === 'function' ? enabled() : unref(enabled));

  const fetchPage = async () => {
    if (!resolveEnabled()) {
      items.value = [];
      totalItems.value = 0;
      extra.value = {};
      return [];
    }

    errorMessage.value = '';

    try {
      const params = {
        page: currentPage.value,
        page_size: pageSize.value,
        ...buildParams({
          currentPage: currentPage.value,
          pageSize: pageSize.value,
          searchQuery: searchQuery.value.trim(),
        }),
      };

      // Si le composant ne fournit pas de mapping custom pour la recherche,
      // on injecte le parametre DRF standard une seule fois ici.
      if (!params.search && searchQuery.value.trim()) {
        params.search = searchQuery.value.trim();
      }

      const response = await api.get(resolveEndpoint(), params);
      const normalized = normalizeResponse(response);

      items.value = normalized.items;
      totalItems.value = normalized.totalItems;
      extra.value = normalized.extra;

      if (typeof onFetched === 'function') {
        onFetched(response, normalized);
      }

      return normalized.items;
    } catch (error) {
      errorMessage.value = error?.response?.data?.error || 'Erreur lors du chargement des données';
      throw error;
    }
  };

  const resetToFirstPageAndFetch = async () => {
    if (currentPage.value !== 1) {
      // Le watcher sur currentPage declenche deja fetchPage ; on evite
      // donc un deuxieme appel reseau quand on force simplement le retour page 1.
      currentPage.value = 1;
      return;
    }

    await fetchPage();
  };

  const handleSearch = (value) => {
    searchQuery.value = toSearchValue(value);

    if (searchTimeoutId) {
      clearTimeout(searchTimeoutId);
    }

    searchTimeoutId = setTimeout(() => {
      resetToFirstPageAndFetch().catch(() => {});
    }, debounceMs);
  };

  watch(currentPage, () => {
    fetchPage().catch(() => {});
  });

  watch(pageSize, () => {
    resetToFirstPageAndFetch().catch(() => {});
  });

  if (watchSource) {
    watch(
      watchSource,
      () => {
        resetToFirstPageAndFetch().catch(() => {});
      },
    );
  }

  onBeforeUnmount(() => {
    if (searchTimeoutId) {
      clearTimeout(searchTimeoutId);
    }
  });

  return {
    items,
    currentPage,
    pageSize,
    searchQuery,
    totalItems,
    totalPages,
    loading,
    extra,
    errorMessage,
    fetchPage,
    handleSearch,
    resetToFirstPageAndFetch,
  };
}
