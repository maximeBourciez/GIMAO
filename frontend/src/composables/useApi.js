import { ref } from "vue";
import api from "@/composables/http";

export function useApi() {
  const data = ref(null);
  const loading = ref(false);
  const error = ref(null);

  const request = async (config) => {
    loading.value = true;
    error.value = null;

    try {
      const response = await api(config);
      data.value = response.data;
      return response.data;
    } catch (err) {
      error.value = err.response?.data || err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const get = (url, params = {}) =>
    request({ url, method: "GET", params });

  const post = (url, data = {}) =>
    request({ url, method: "POST", data });

  const put = (url, data = {}) =>
    request({ url, method: "PUT", data });

  const patch = (url, data = {}) =>
    request({ url, method: "PATCH", data });

  const remove = (url) =>
    request({ url, method: "DELETE" });

  return {
    data,
    loading,
    error,
    get,
    post,
    put,
    patch,
    remove,
  };
}