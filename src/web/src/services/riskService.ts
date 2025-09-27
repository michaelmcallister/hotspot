import { apiRequest } from './api';

export interface RiskData {
  base?: {
    risk_score: number;
    suburb: string;
    postcode: string;
  };
  comparisons?: Array<{
    risk_score: number;
    suburb: string;
    postcode: string;
    distance_km: number;
  }>;
}

export interface TopRiskParams {
  scope?: string;
  order?: string;
  limit?: string;
  [key: string]: string | undefined;
}

export const riskService = {
  getTopRisk: async (params: TopRiskParams = {}): Promise<RiskData[]> => {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) {
        searchParams.append(key, value);
      }
    });
    return apiRequest(`/risk/top?${searchParams.toString()}`);
  },

  compareRisk: async (postcode: string): Promise<RiskData> => apiRequest(`/risk/compare?postcode=${postcode}`),
};
