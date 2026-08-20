import axios from 'axios';

const PORT_OPTIONS = ['http://127.0.0.1:5000', 'http://localhost:5000', 'http://127.0.0.1:5001', 'http://localhost:5001'];
let activeBaseUrl = 'http://127.0.0.1:5000';

async function getActiveBaseUrl() {
  for (const url of PORT_OPTIONS) {
    try {
      const res = await axios.get(`${url}/api/health`, { timeout: 1000 });
      if (res.data && (res.data.status === 'ok' || res.data.success)) {
        activeBaseUrl = url;
        return url;
      }
    } catch (e) {}
  }
  return activeBaseUrl;
}

export const api = {
  getHealth: async () => {
    try {
      const url = await getActiveBaseUrl();
      const res = await axios.get(`${url}/api/health`, { timeout: 2000 });
      return res.data;
    } catch (e) {
      return { status: 'offline', success: false };
    }
  },

  getModelInfo: async () => {
    try {
      const url = await getActiveBaseUrl();
      const res = await axios.get(`${url}/model-info`, { timeout: 2000 });
      return res.data;
    } catch (e) {
      return { dataset: 'UNSW-NB15', pca_components: 4, models: ['SVM', 'QSVM', 'VQC'] };
    }
  },

  getStats: async () => {
    try {
      const url = await getActiveBaseUrl();
      const res = await axios.get(`${url}/api/v1/analytics/stats`, { timeout: 2000 });
      return res.data;
    } catch (e) {
      return null;
    }
  },

  predict: async (payload) => {
    const url = await getActiveBaseUrl();
    const res = await axios.post(`${url}/api/v1/predict`, payload, { timeout: 4000 });
    return res.data;
  },

  explain: async (payload) => {
    try {
      const url = await getActiveBaseUrl();
      const res = await axios.post(`${url}/api/v1/xai/explain`, payload, { timeout: 3000 });
      return res.data;
    } catch (e) {
      return null;
    }
  },

  uploadCsv: async (formData) => {
    const url = await getActiveBaseUrl();
    const res = await axios.post(`${url}/api/v1/predict/batch`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 10000
    });
    return res.data;
  }
};
